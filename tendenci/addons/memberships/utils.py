import os
import csv
from datetime import datetime, date, timedelta
import dateutil.parser as dparser

from django.http import Http404, HttpResponseServerError
from django.conf import settings
from django.utils import simplejson
from django.contrib.auth.models import User
from django.template import loader
from django.template.defaultfilters import slugify
from django.db.models import Q
from django.core.files.storage import default_storage

from tendenci.core.perms.utils import has_perm
from tendenci.addons.memberships.models import (App,
                                                AppField,
                                                AppEntry,
                                                Membership,
                                                MembershipType,
                                                MembershipDefault)
from tendenci.core.base.utils import normalize_newline
from tendenci.apps.profiles.models import Profile
from tendenci.core.imports.utils import get_unique_username
from tendenci.core.payments.models import PaymentMethod
from tendenci.apps.entities.models import Entity


def get_default_membership_fields(use_for_corp=False):
    json_file_path = os.path.join(settings.TENDENCI_ROOT,
        'addons/memberships/fixtures/default_membership_application_fields.json')
    json_file = open(json_file_path, 'r')
    data = ''.join(json_file.read())
    json_file.close()

    field_list = simplejson.loads(data)

    # add default fields for corp. individuals
    if use_for_corp:
        corp_field_list = get_default_membership_corp_fields()
    else:
        corp_field_list = None

    if field_list:
        if corp_field_list:
            field_list = field_list + corp_field_list
    else:
        field_list = corp_field_list

    return field_list


def get_default_membership_corp_fields():
    json_file_path = os.path.join(settings.TENDENCI_ROOT,
        'addons/memberships/fixtures/default_membership_application_fields_for_corp.json')
    json_file = open(json_file_path, 'r')
    data = ''.join(json_file.read())
    json_file.close()

    corp_field_list = simplejson.loads(data)

    return corp_field_list


def edit_app_update_corp_fields(app):
    """
    Update the membership application's corporate membership fields (corporate_membership_id)
    when editing a membership application.
    """
    if app:
        try:
            app_field = AppField.objects.get(app=app, field_type='corporate_membership_id')
            if not app.use_for_corp:
                if not hasattr(app, 'corp_app'):
                    app_field.delete()
                else:
                    app.use_for_corp = 1
                    app.save()
        except AppField.DoesNotExist:
            if app.use_for_corp:
                field_list = get_default_membership_corp_fields()
                for field in field_list:
                    field.update({'app': app})
                    AppField.objects.create(**field)


def get_corporate_membership_choices():
    cm_list = [(0, 'SELECT ONE')]
    from django.db import connection
    # use the raw sql because we cannot import CorporateMembership
    # in the memberships app
    cursor = connection.cursor()
    cursor.execute(
        """SELECT id, name
        FROM corporate_memberships_corporatemembership
        WHERE status=True AND status_detail='active'
        ORDER BY name"""
    )

    for row in cursor.fetchall():
        cm_list.append((row[0], row[1]))

    return cm_list


def has_null_byte(file_path):
    f = default_storage.open(file_path, 'r')
    data = f.read()
    f.close()
    return ('\0' in data)


def csv_to_dict(file_path, **kwargs):
    """
    Returns a list of dicts. Each dict represents record.
    """
    machine_name = kwargs.get('machine_name', False)

    # null byte; assume xls; not csv
    if has_null_byte(file_path):
        return []
    
    normalize_newline(file_path)
    csv_file = csv.reader(default_storage.open(file_path, 'rU'))
    colnames = csv_file.next()  # row 1;

    if machine_name:
        colnames = [slugify(c).replace('-', '') for c in colnames]
        
    cols = xrange(len(colnames))
    lst = []
    
    # make sure colnames are unique
    duplicates = {}
    for i in cols:
        for j in cols:
            # compare with previous and next fields
            if i != j and colnames[i] == colnames[j]:
                number = duplicates.get(colnames[i], 0) + 1
                duplicates[colnames[i]] = number
                colnames[j] = colnames[j] + "-" + str(number)
    
    for row in csv_file:
        entry = {}
        rows = len(row) - 1
        for col in cols:
            if col > rows:
                break  # go to next row
            entry[colnames[col]] = row[col]
        lst.append(entry)

    return lst  # list of dictionaries


def is_import_valid(file_path):
    """
    Returns a 2-tuple containing a booelean and list of errors

    The import file must be of type .csv and and include
    a membership type column.
    """
    errs = []
    ext = os.path.splitext(file_path)[1]

    if ext != '.csv':
        errs.append("Pleaes make sure you're importing a .csv file.")
        return False, errs

    if has_null_byte(file_path):
        errs.append('This .csv file has null characters, try re-saving it.')
        return False, errs

    # get header column
    f = default_storage.open(file_path, 'r')
    row = f.readline()
    f.close()

    headers = [slugify(r).replace('-', '') for r in row.split(',')]

    required = ('membershiptype',)
    requirements_met = [r in headers for r in required]

    if all(requirements_met):
        return True, []
    else:
        return False, ['Please make sure there is a membership type column.']


def count_active_memberships(date):
    """
    Counts all active memberships in a given date
    """
    return Membership.objects.active(
        create_dt__lte=date, expire_dt__gt=date).count()


def prepare_chart_data(days, height=300):
    """
    Creates a list of tuples of a day and membership count per day.
    """

    data = []
    max_count = 0

    #append mem count per day
    for day in days:
        count = count_active_memberships(day)
        if count > max_count:
            max_count = count
        data.append({
            'day': day,
            'count': count,
        })

    # normalize height
    try:
        kH = height * 1.0 / max_count
    except Exception:
        kH = 1.0
    for d in data:
        d['height'] = int(d['count'] * kH)

    return data


def month_days(year, month):
    "Returns iterator for days in selected month"
    day = date(year, month, 1)
    while day.month == month:
        yield day
        day += timedelta(days=1)


def get_days(request):
    "returns a list of days in a month"
    now = date.today()
    year = int(request.GET.get('year') or str(now.year))
    month = int(request.GET.get('month') or str(now.month))
    days = list(month_days(year, month))
    return days


def has_app_perm(user, perm, obj=None):
    """
    Wrapper for perm's has_perm util.
    This consider's the app's status_detail
    """
    allow = has_perm(user, perm, obj)
    if user.profile.is_superuser:
        return allow
    if obj.status_detail != 'published':
        return allow
    else:
        return False


def get_over_time_stats():
    """
    Returns membership statistics over time.
        Last Month
        Last 3 Months
        Last 6 Months
        Last 9 Months
        Last 12 Months
        Year to Date
    """
    today = date.today()
    year = datetime(day=1, month=1, year=today.year)
    times = [
        ("Last Month", months_back(1), 1),
        ("Last 3 Months", months_back(3), 2),
        ("Last 6 Months", months_back(6), 3),
        ("Last 9 Months", months_back(9), 4),
        ("Last 12 Months", months_back(12), 5),
        ("Year to Date", year, 5),
    ]

    stats = []
    for time in times:
        start_dt = time[1]
        d = {}
        active_mems = Membership.objects.active(expire_dt__gt=start_dt)
        d['new'] = active_mems.filter(subscribe_dt__gt=start_dt).count()  # just joined in that time period
        d['renewing'] = active_mems.filter(renewal=True).count()
        d['active'] = active_mems.count()
        d['time'] = time[0]
        d['start_dt'] = start_dt
        d['end_dt'] = today
        d['order'] = time[2]
        stats.append(d)

    return sorted(stats, key=lambda x: x['order'])


def months_back(n):
    """Return datetime minus n months"""
    from dateutil.relativedelta import relativedelta

    return date.today() + relativedelta(months=-n)


def get_status_filter(status):
    if status == "pending":
        return Q(is_approved=None)
    elif status == "approved":
        return Q(is_approved=True)
    elif status == "disapproved":
        return Q(is_approved=False)
    else:
        return Q()


def get_app_field_labels(app):
    """Get a list of field labels for this app.
    """
    labels_list = []
    fields = app.fields.all().order_by('position')
    for field in fields:
        labels_list.append(field.label)

    return labels_list


def get_notice_token_help_text(notice=None):
    """Get the help text for how to add the token in the email content,
        and display a list of available token.
    """
    help_text = ''
    if notice and notice.membership_type:
        membership_types = [notice.membership_type]
    else:
        membership_types = MembershipType.objects.filter(status=True, status_detail='active')

    # get a list of apps from membership types
    apps_list = []
    for mt in membership_types:
        apps = App.objects.filter(membership_types=mt)
        if apps:
            apps_list.extend(apps)

    apps_list = set(apps_list)
    apps_len = len(apps_list)

    # render the tokens
    help_text += '<div style="margin: 1em 10em;">'
    help_text += """
                <div style="margin-bottom: 1em;">
                You can use tokens to display member info or site specific information.
                A token is composed of a field label or label lower case with underscore (_)
                instead of spaces, wrapped in
                {{ }} or [ ]. <br />
                For example, token for "First Name" field: {{ first_name }}
                </div>
                """

    help_text += '<div id="toggle_token_view"><a href="javascript:;">Click to view available tokens</a></div>'
    help_text += '<div id="notice_token_list">'
    if apps_list:
        for app in apps_list:
            if apps_len > 1:
                help_text += '<div style="font-weight: bold;">%s</div>' % app.name
            labels_list = get_app_field_labels(app)
            help_text += "<ul>"
            for label in labels_list:
                help_text += '<li>{{ %s }}</li>' % slugify(label).replace('-', '_')
            help_text += "</ul>"
    else:
        help_text += '<div>No field tokens because there is no applications.</div>'

    other_labels = ['membernumber',
                    'membershiptype',
                    'membershiplink',
                    'renewlink',
                    'expirationdatetime',
                    'sitecontactname',
                    'sitecontactemail',
                    'sitedisplayname',
                    'timesubmitted'
                    ]
    help_text += '<div style="font-weight: bold;">Non-field Tokens</div>'
    help_text += "<ul>"
    for label in other_labels:
        help_text += '<li>{{ %s }}</li>' % label
    help_text += "</ul>"
    help_text += "</div>"
    help_text += "</div>"

    help_text += """
                <script>
                    $(document).ready(function() {
                        $('#notice_token_list').hide();
                         $('#toggle_token_view').click(function () {
                        $('#notice_token_list').toggle();
                         });
                    });
                </script>
                """

    return help_text


def spawn_username(*args):
    """
    Join arguments to create username [string].
    Find similiar usernames; auto-increment newest username.
    Return new username [string].
    """
    if not args:
        raise Exception('spawn_username() requires atleast 1 argument; 0 were given')

    import re

    max_length = 8

    un = ' '.join(args)             # concat args into one string
    un = re.sub('\s+', '_', un)       # replace spaces w/ underscores
    un = re.sub('[^\w.-]+', '', un)   # remove non-word-characters
    un = un.strip('_.- ')           # strip funny-characters from sides
    un = un[:max_length].lower()    # keep max length and lowercase username

    others = []  # find similiar usernames
    for u in User.objects.filter(username__startswith=un):
        if u.username.replace(un, '0').isdigit():
            others.append(int(u.username.replace(un, '0')))

    if others and 0 in others:
        # the appended digit will compromise the username length
        # there would have to be more than 99,999 duplicate usernames
        # to kill the database username max field length
        un = '%s%s' % (un, str(max(others) + 1))

    return un.lower()


def get_user(**kwargs):
    """
    Returns first user that matches filters.
    If no user is found then a non type object is returned.
    """
    try:
        user = User.objects.get(**kwargs)
    except User.MultipleObjectsReturned:
        user = User.objects.filter(**kwargs)[0]
    except User.DoesNotExist:
        user = None

    return user


def get_membership_stats():
    now = datetime.now()
    summary = []
    types = MembershipType.objects.all()
    total_active = 0
    total_pending = 0
    total_expired = 0
    total_total = 0
    for mem_type in types:
        mems = Membership.objects.filter(membership_type=mem_type)
        active = mems.filter(status_detail='active', expire_dt__gt=now)
        expired = mems.filter(status_detail='active', expire_dt__lte=now)
        pending = AppEntry.objects.filter(app__membership_types=mem_type, is_approved__isnull=True)
        total_all = active.count() + pending.count() + expired.count()
        total_active += active.count()
        total_pending += pending.count()
        total_expired += expired.count()
        total_total += total_all
        summary.append({
            'type': mem_type,
            'active': active.count(),
            'pending': pending.count(),
            'expired': expired.count(),
            'total': total_all,
        })

    return (sorted(summary, key=lambda x: x['type'].name),
        (total_active, total_pending, total_expired, total_total))


def make_csv(**kwargs):
    """
    Make a CSV file
    """
    from django.template.defaultfilters import slugify
    from tendenci.core.imports.utils import render_excel

    slug = kwargs.get('slug')

    if not slug:
        raise Http404

    try:
        app = App.objects.get(slug=slug)
    except App.DoesNotExist, App.MultipleObjectsReturned:
        raise Http404

    file_name = "%s.csv" % slugify(app.name)

    exclude_params = (
        'horizontal-rule',
        'header',
    )

    fields = AppField.objects.filter(app=app, exportable=True).exclude(field_type__in=exclude_params).order_by('position')
    labels = [field.label for field in fields]

    extra_labels = [
        'User Name',
        'Member Number',
        'Join Date',
        'Renew Date',
        'Expiration Date',
        'Status',
        'Status Detail',
        'Invoice Number',
        'Invoice Amount',
        'Invoice Balance'
    ]
    labels.extend(extra_labels)
    return render_excel(file_name, labels, [], '.csv')


class NoMembershipTypes(Exception):
    pass


def render_to_max_types(*args, **kwargs):
    if not isinstance(args,list):
        args = []
        args.append('memberships/max_types.html')

    httpresponse_kwargs = {'mimetype': kwargs.pop('mimetype', None)}

    response = HttpResponseServerError(loader.render_to_string(*args, **kwargs), **httpresponse_kwargs)
    
    return response


def memb_import_parse_csv(mimport):
    normalize_newline(mimport.upload_file.name)
    csv_reader = csv.reader(
        default_storage.open(mimport.upload_file.name, 'rb'))
    fieldnames = csv_reader.next()
    # clean up the fieldnames
    # ex: change First Name to first_name
    for i in range(0, len(fieldnames)):
        fieldnames[i] = fieldnames[i].lower().replace(' ', '_')

    data_list = []

    for row in csv_reader:
        data_list.append(dict(zip(fieldnames, row)))

    return fieldnames, data_list


def process_default_membership(request_user, memb_data, mimport,
                               dry_run=True, **kwargs):
    """
    Check if it's insert or update. If dry_run is False,
    do the import to the membership_default.

    :param memb_data: a dictionary that includes the info of a membership
    :param mimport: a instance of MembershipImport
    :param dry_run: if True, do everything except updating the database.
    """
    #fieldnames = memb_data.keys()
    user = None
    memb = None
    user_display = {}
    user_display['error'] = ''
    user_display['user'] = None
    missing_fields = []
    summary_d = kwargs.get('summary_d')
    user_filters = None
    profile_filters = None
    key = mimport.key

    key_value_dict = {}
    key_list = key.split(',')
    for k in key_list:
        key_value_dict[k] = memb_data[k]
        if not key_value_dict[k]:
            missing_fields.append(k)

    # it's okay if we have one of the required fields
    if key == 'email,member_number' and len(missing_fields) == 1:
        missing_fields = None

    # don't process if we have missing value of required fields
    if missing_fields:
        if key == 'email,member_number':
            user_display['error'] = 'Missing required field(s) %s' % (
                                        ' or '.join(missing_fields))
        else:
            user_display['error'] = 'Missing required field(s) %s' % (
                                        ' and '.join(missing_fields))
        user_display['action'] = 'skip'
        if not dry_run:
            summary_d['invalid'] += 1
    else:
        if key == 'email':
            user_filters = Q(email=key_value_dict['email'])
        elif key == 'username':
            user_filters = Q(username=key_value_dict['username'])
        elif key == 'member_number':
            profile_filters = Q(member_number=key_value_dict['member_number'])
        elif key == 'email,member_number':
            if key_value_dict['email']:
                user_filters = Q(email=key_value_dict['email'])
            if key_value_dict['member_number']:
                profile_filters = Q(member_number=key_value_dict['member_number'])
        elif key == 'first_name,last_name,email':
            user_filters = Q(first_name=key_value_dict['first_name']
                             ) & Q(last_name=key_value_dict['last_name']
                                   ) & Q(email=key_value_dict['email'])
        elif key == 'first_name,last_name,phone':
            profile_filters = Q(user__first_name=key_value_dict['first_name']
                            ) & Q(
                            user__last_name=key_value_dict['last_name']
                            ) & Q(
                            phone=key_value_dict['phone'])
        elif key == 'first_name,last_name,company':
            profile_filters = Q(user__first_name=key_value_dict['first_name']
                            ) & Q(
                            user__last_name=key_value_dict['last_name']
                            ) & Q(
                            company=key_value_dict['company'])

        if user_filters:
            [user] = User.objects.filter(user_filters).order_by(
                            '-is_active', '-is_superuser', '-is_staff'
                                )[:1] or [None]
            if not user and key == 'email,member_number':
                [profile] = Profile.objects.filter(
                                        profile_filters)[:1] or [None]
                if profile:
                    user = profile.user
        if profile_filters and key != 'email,member_number':
            [profile] = Profile.objects.filter(profile_filters)[:1] or [None]
            if profile:
                user = profile.user

        if user:
            user_display['user_action'] = 'update'
            user_display['user'] = user
            [memb] = MembershipDefault.objects.filter(user=user).exclude(
                      status_detail='archive'
                            )[:1] or [None]
            if memb:
                user_display['memb_action'] = 'update'
                user_display['action'] = 'update'
            else:
                user_display['memb_action'] = 'insert'
                user_display['action'] = 'mixed'
        else:
            user_display['user_action'] = 'insert'
            user_display['memb_action'] = 'insert'
            user_display['action'] = 'insert'

        if not dry_run:
            if all([
                    user_display['user_action'] == 'insert',
                    user_display['memb_action'] == 'insert'
                    ]):
                summary_d['insert'] += 1
            elif all([
                    user_display['user_action'] == 'update',
                    user_display['memb_action'] == 'update'
                    ]):
                summary_d['update'] += 1
            else:
                summary_d['update_insert'] += 1

            # now do the update or insert
            do_import_membership_default(request_user, mimport,
                                         user, memb, memb_data,
                                         user_display)
            return

    user_display.update({
                        'first_name': memb_data.get('first_name', ''),
                        'last_name': memb_data.get('last_name', ''),
                        'email': memb_data.get('email', ''),
                        'username': memb_data.get('username', ''),
                        'member_number': memb_data.get('member_number', ''),
                        'phone': memb_data.get('phone', ''),
                        'company': memb_data.get('company', ''),
                         })
    return user_display


def do_import_membership_default(request_user, mimport,
                                 user, memb, memb_data,
                                 action_info):
    """
    Database import here - insert or update
    """
    # handle user
    if not user:
        user = User()

    field_names = memb_data.keys()
    # exclude user
    if 'user' in field_names:
        field_names.remove('user')

    assign_import_values_from_dict(user, mimport, memb_data,
                            field_names, action_info['user_action'])

    # make sure username is unique.
    if action_info['user_action'] == 'insert':
        user.username = get_unique_username(user)

    if 'password' in field_names and mimport.override and user.password:
        user.set_password(user.password)

    if not user.password:
        user.set_password(User.objects.make_random_password(length=8))

    user.is_active = True

    user.save()

    # process profile
    try:  # get or create
        profile = user.get_profile()
    except Profile.DoesNotExist:
        profile = Profile.objects.create(user=user,
           creator=request_user,
           creator_username=request_user.username,
           owner=request_user,
           owner_username=request_user.username,
        )
    assign_import_values_from_dict(profile, mimport, memb_data,
                        field_names, action_info['user_action'])

    profile.save()

    # membership
    if not memb:
        memb = MembershipDefault(
                user=user,
                creator=request_user,
                creator_username=request_user.username,
                owner=request_user,
                owner_username=request_user.username,
                                 )

    assign_import_values_from_dict(memb, mimport, memb_data,
                        field_names, action_info['memb_action'])
    if memb.status == None:
        memb.status = True
    if not memb.status_detail:
        memb.status_detail = 'active'

    # membership type
    if not hasattr(memb, "membership_type"):
        membership_type = None
        if 'membership_type' in field_names:
            membership_type = get_membership_type_by_value(
                        memb_data['membership_type'])
        if not membership_type:
            # last resort - assign a default membership type
            membership_type = MembershipType.objects.filter(
                                            status=True,
                                            status_detail='active')[0]
        memb.membership_type = membership_type

    # prevent the not-null constraint violations
    # join_dt
    if not hasattr(memb, 'join_dt') or not memb.join_dt:
        memb.join_dt = datetime.now()
    # exire_dt
    if not hasattr(memb, 'expire_dt') or not memb.expire_dt:
        memb.expire_dt = datetime.now() + timedelta(days=365)
    # renew_dt
    if not hasattr(memb, 'renew_dt') or not memb.renew_dt:
        memb.renew_dt = datetime.now()
    # application_abandoned_dt
    if not hasattr(memb, 'application_abandoned_dt') or \
        not memb.application_abandoned_dt:
        memb.application_abandoned_dt = datetime.now()
    # application_abandoned_user_id
    if not hasattr(memb, 'application_abandoned_user') or \
        not memb.application_abandoned_user:
        memb.application_abandoned_user = request_user
    # application_complete_dt
    if not hasattr(memb, 'application_complete_dt') or \
        not memb.application_complete_dt:
        memb.application_complete_dt = datetime.now()
    # application_complete_user_id
    if not hasattr(memb, 'application_complete_user') or \
        not memb.application_complete_user:
        memb.application_complete_user = request_user
    # application_approved_dt
    if not hasattr(memb, 'application_approved_dt') or \
        not memb.application_approved_dt:
        memb.application_approved_dt = datetime.now()
    # application_approved_user_id
    if not hasattr(memb, 'application_approved_user') or \
        not memb.application_approved_user:
        memb.application_approved_user = request_user
    # action_taken_dt
    if not hasattr(memb, 'action_taken_dt') or \
        not memb.action_taken_dt:
        memb.action_taken_dt = datetime.now()
    # action_taken_user_id
    if not hasattr(memb, 'action_taken_user') or \
        not memb.action_taken_user:
        memb.action_taken_user = request_user
    # bod_dt
    if not hasattr(memb, 'bod_dt') or \
        not memb.bod_dt:
        memb.bod_dt = datetime.now()
    # personnel_notified_dt
    if not hasattr(memb, 'personnel_notified_dt') or \
        not memb.personnel_notified_dt:
        memb.personnel_notified_dt = datetime.now()
    # payment_received_dt
    if not hasattr(memb, 'payment_received_dt') or \
        not memb.payment_received_dt:
        memb.payment_received_dt = datetime.now()
    # payment_method_id
    if not hasattr(memb, 'payment_method') or \
        not memb.payment_method:
        memb.payment_method = PaymentMethod.objects.all()[0]
    # override_price
    if memb.override_price == None:
        memb.override_price = 0
    # application_approved_denied_dt
    if not hasattr(memb, 'application_approved_denied_dt') or \
        not memb.application_approved_denied_dt:
        memb.application_approved_denied_dt = datetime.now()
    # application_approved_denied_user_id
    if not hasattr(memb, 'application_approved_denied_user') or \
        not memb.application_approved_denied_user:
        memb.application_approved_denied_user = request_user
    # organization_entity_id
    if not hasattr(memb, 'organization_entity') or \
        not memb.organization_entity:
        memb.organization_entity = Entity.objects.all()[0]
    # corporate_entity_id
    if not hasattr(memb, 'corporate_entity') or \
        not memb.corporate_entity:
        memb.corporate_entity = Entity.objects.all()[0]
    # corporate_membership_id
    if not hasattr(memb, 'corporate_membership_id') or \
        not memb.corporate_membership_id:
        memb.corporate_membership_id = 0

    memb.save()

    # member_number
    # TODO: create a function to assign a member number
    if not memb.member_number:
        if memb.status and memb.status_detail == 'active':
            memb.member_number = 5100 + memb.pk
    if memb.member_number:
        if not profile.member_number:
            profile.member_number = memb.member_number
            profile.save()
        else:
            if profile.member_number != memb.member_number:
                profile.member_number = memb.member_number
                profile.save()
    else:
        if profile.member_number:
            profile.member_number = ''
            profile.save()

    # group associated to membership type
    params = {'creator_id': request_user.pk,
              'creator_username': request_user.username,
              'owner_id': request_user.pk,
              'owner_username': request_user.username}
    memb.membership_type.group.add_user(memb.user, **params)


def assign_import_values_from_dict(instance, mimport, memb_data,
                            field_names, action):
    for field_name in field_names:
        if hasattr(instance, field_name):
            # parse the datetime
            if field_name in ['create_dt', 'update_dt',
                              'dob_dt', 'dob_dt',
                              'join_dt', 'expire_dt',
                              'application_abandoned_dt',
                              'application_complete_dt',
                              'application_approved_dt', 'bod_dt',
                              'personnel_notified_dt', 'payment_received_dt',
                              'application_approved_denied_dt', 'renew_dt',
                              'action_taken_dt',
                              ]:
                value = dparser.parse(memb_data[field_name])
            else:
                # TODO: take care of foreign keys
                value = memb_data[field_name]
                if field_name == 'membership_type':
                    value = get_membership_type_by_value(value)

            if action == 'insert':
                setattr(instance, field_name, value)
            else:
                if mimport.override or (getattr(instance, field_name) == '' \
                                        or getattr(instance, field_name) == None):
                    setattr(instance, field_name, value)


def get_membership_type_by_value(value):
    if value and value.isdigit():
        value = int(value)
    if isinstance(value, int):
        return get_membership_type_by_id(value)
    elif isinstance(value, str):
        return get_membership_type_by_name(value)


def get_membership_type_by_id(pk):
    try:
        memb_type = MembershipType.objects.get(pk=pk)
    except MembershipType.DoesNotExist:
        memb_type = None
    return memb_type


def get_membership_type_by_name(name):
    try:
        memb_type = MembershipType.objects.get(name=name)
    except MembershipType.DoesNotExist:
        memb_type = None
    return memb_type
