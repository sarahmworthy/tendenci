from datetime import datetime
import traceback

from django.core.management.base import BaseCommand
from django.shortcuts import get_object_or_404
from django.contrib.auth.models import User


class Command(BaseCommand):
    """
    Import MembershipDefault.

    Usage:
        python manage.py import_membership_defaults [mimport_id] [request.user.id]

        example:
        python manage.py import_membership_defaults 10 1
    """

    def handle(self, *args, **options):
        from tendenci.addons.memberships.models import MembershipImport
        from tendenci.addons.memberships.utils import memb_import_parse_csv
        from tendenci.addons.memberships.utils import ImportMembDefault

        mimport = get_object_or_404(MembershipImport,
                                        pk=args[0])
        request_user = User.objects.get(pk=args[1])

        fieldnames, data_list = memb_import_parse_csv(mimport)

        imd = ImportMembDefault(request_user, mimport, dry_run=False)

        for memb_data in data_list:
            # catch any error
            try:
                imd.process_default_membership(memb_data)
            except Exception, e:
                # mimport.status = 'error'
                # TODO: add a field to log the error
                # mimport.save()
                # raise  Exception(traceback.format_exc())
                print e

            mimport.num_processed += 1
            # save the status
            summary = 'insert:%d,update:%d,update_insert:%d,invalid:%d' % (
                                        imd.summary_d['insert'],
                                        imd.summary_d['update'],
                                        imd.summary_d['update_insert'],
                                        imd.summary_d['invalid']
                                        )
            mimport.summary = summary
            mimport.save()

        mimport.status = 'completed'
        mimport.complete_dt = datetime.now()
        mimport.save()
