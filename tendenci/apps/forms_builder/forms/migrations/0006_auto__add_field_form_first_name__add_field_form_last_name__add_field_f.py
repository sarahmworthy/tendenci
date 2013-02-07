# encoding: utf-8
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models

class Migration(SchemaMigration):

    def forwards(self, orm):
        
        # Adding field 'Form.first_name'
        db.add_column('forms_form', 'first_name', self.gf('django.db.models.fields.BooleanField')(default=False), keep_default=False)

        # Adding field 'Form.last_name'
        db.add_column('forms_form', 'last_name', self.gf('django.db.models.fields.BooleanField')(default=False), keep_default=False)

        # Adding field 'Form.email'
        db.add_column('forms_form', 'email', self.gf('django.db.models.fields.BooleanField')(default=False), keep_default=False)

        # Adding field 'Form.position_title'
        db.add_column('forms_form', 'position_title', self.gf('django.db.models.fields.BooleanField')(default=False), keep_default=False)

        # Adding field 'Form.url'
        db.add_column('forms_form', 'url', self.gf('django.db.models.fields.BooleanField')(default=False), keep_default=False)

        # Adding field 'Form.comments'
        db.add_column('forms_form', 'comments', self.gf('django.db.models.fields.BooleanField')(default=False), keep_default=False)

        # Adding field 'Form.address'
        db.add_column('forms_form', 'address', self.gf('django.db.models.fields.BooleanField')(default=False), keep_default=False)

        # Adding field 'Form.city'
        db.add_column('forms_form', 'city', self.gf('django.db.models.fields.BooleanField')(default=False), keep_default=False)

        # Adding field 'Form.state'
        db.add_column('forms_form', 'state', self.gf('django.db.models.fields.BooleanField')(default=False), keep_default=False)

        # Adding field 'Form.zipcode'
        db.add_column('forms_form', 'zipcode', self.gf('django.db.models.fields.BooleanField')(default=False), keep_default=False)

        # Adding field 'Form.country'
        db.add_column('forms_form', 'country', self.gf('django.db.models.fields.BooleanField')(default=False), keep_default=False)

        # Adding field 'Form.phone'
        db.add_column('forms_form', 'phone', self.gf('django.db.models.fields.BooleanField')(default=False), keep_default=False)

        # Adding field 'Form.company_name'
        db.add_column('forms_form', 'company_name', self.gf('django.db.models.fields.BooleanField')(default=False), keep_default=False)

        # Adding field 'Form.company_address'
        db.add_column('forms_form', 'company_address', self.gf('django.db.models.fields.BooleanField')(default=False), keep_default=False)

        # Adding field 'Form.company_city'
        db.add_column('forms_form', 'company_city', self.gf('django.db.models.fields.BooleanField')(default=False), keep_default=False)

        # Adding field 'Form.company_state'
        db.add_column('forms_form', 'company_state', self.gf('django.db.models.fields.BooleanField')(default=False), keep_default=False)

        # Adding field 'Form.company_zipcode'
        db.add_column('forms_form', 'company_zipcode', self.gf('django.db.models.fields.BooleanField')(default=False), keep_default=False)

        # Adding field 'Form.company_country'
        db.add_column('forms_form', 'company_country', self.gf('django.db.models.fields.BooleanField')(default=False), keep_default=False)

        # Adding field 'Form.company_phone'
        db.add_column('forms_form', 'company_phone', self.gf('django.db.models.fields.BooleanField')(default=False), keep_default=False)

        # Adding field 'FormEntry.first_name'
        db.add_column('forms_formentry', 'first_name', self.gf('django.db.models.fields.CharField')(default='', max_length=200, blank=True), keep_default=False)

        # Adding field 'FormEntry.last_name'
        db.add_column('forms_formentry', 'last_name', self.gf('django.db.models.fields.CharField')(default='', max_length=200, blank=True), keep_default=False)

        # Adding field 'FormEntry.email'
        db.add_column('forms_formentry', 'email', self.gf('django.db.models.fields.CharField')(default='', max_length=200, blank=True), keep_default=False)

        # Adding field 'FormEntry.position_title'
        db.add_column('forms_formentry', 'position_title', self.gf('django.db.models.fields.CharField')(default='', max_length=500, blank=True), keep_default=False)

        # Adding field 'FormEntry.url'
        db.add_column('forms_formentry', 'url', self.gf('django.db.models.fields.URLField')(default='', max_length=200, blank=True), keep_default=False)

        # Adding field 'FormEntry.comments'
        db.add_column('forms_formentry', 'comments', self.gf('django.db.models.fields.TextField')(default='', blank=True), keep_default=False)

        # Adding field 'FormEntry.address'
        db.add_column('forms_formentry', 'address', self.gf('django.db.models.fields.CharField')(default='', max_length=100, blank=True), keep_default=False)

        # Adding field 'FormEntry.city'
        db.add_column('forms_formentry', 'city', self.gf('django.db.models.fields.CharField')(default='', max_length=100, blank=True), keep_default=False)

        # Adding field 'FormEntry.state'
        db.add_column('forms_formentry', 'state', self.gf('django.db.models.fields.CharField')(default='', max_length=100, blank=True), keep_default=False)

        # Adding field 'FormEntry.zipcode'
        db.add_column('forms_formentry', 'zipcode', self.gf('django.db.models.fields.CharField')(default='', max_length=100, blank=True), keep_default=False)

        # Adding field 'FormEntry.country'
        db.add_column('forms_formentry', 'country', self.gf('django.db.models.fields.CharField')(default='', max_length=100, blank=True), keep_default=False)

        # Adding field 'FormEntry.phone'
        db.add_column('forms_formentry', 'phone', self.gf('django.db.models.fields.CharField')(default='', max_length=50, blank=True), keep_default=False)

        # Adding field 'FormEntry.company_name'
        db.add_column('forms_formentry', 'company_name', self.gf('django.db.models.fields.CharField')(default='', max_length=500, blank=True), keep_default=False)

        # Adding field 'FormEntry.company_address'
        db.add_column('forms_formentry', 'company_address', self.gf('django.db.models.fields.CharField')(default='', max_length=100, blank=True), keep_default=False)

        # Adding field 'FormEntry.company_city'
        db.add_column('forms_formentry', 'company_city', self.gf('django.db.models.fields.CharField')(default='', max_length=100, blank=True), keep_default=False)

        # Adding field 'FormEntry.company_state'
        db.add_column('forms_formentry', 'company_state', self.gf('django.db.models.fields.CharField')(default='', max_length=100, blank=True), keep_default=False)

        # Adding field 'FormEntry.company_zipcode'
        db.add_column('forms_formentry', 'company_zipcode', self.gf('django.db.models.fields.CharField')(default='', max_length=100, blank=True), keep_default=False)

        # Adding field 'FormEntry.company_country'
        db.add_column('forms_formentry', 'company_country', self.gf('django.db.models.fields.CharField')(default='', max_length=100, blank=True), keep_default=False)

        # Adding field 'FormEntry.company_phone'
        db.add_column('forms_formentry', 'company_phone', self.gf('django.db.models.fields.CharField')(default='', max_length=50, blank=True), keep_default=False)


    def backwards(self, orm):
        
        # Deleting field 'Form.first_name'
        db.delete_column('forms_form', 'first_name')

        # Deleting field 'Form.last_name'
        db.delete_column('forms_form', 'last_name')

        # Deleting field 'Form.email'
        db.delete_column('forms_form', 'email')

        # Deleting field 'Form.position_title'
        db.delete_column('forms_form', 'position_title')

        # Deleting field 'Form.url'
        db.delete_column('forms_form', 'url')

        # Deleting field 'Form.comments'
        db.delete_column('forms_form', 'comments')

        # Deleting field 'Form.address'
        db.delete_column('forms_form', 'address')

        # Deleting field 'Form.city'
        db.delete_column('forms_form', 'city')

        # Deleting field 'Form.state'
        db.delete_column('forms_form', 'state')

        # Deleting field 'Form.zipcode'
        db.delete_column('forms_form', 'zipcode')

        # Deleting field 'Form.country'
        db.delete_column('forms_form', 'country')

        # Deleting field 'Form.phone'
        db.delete_column('forms_form', 'phone')

        # Deleting field 'Form.company_name'
        db.delete_column('forms_form', 'company_name')

        # Deleting field 'Form.company_address'
        db.delete_column('forms_form', 'company_address')

        # Deleting field 'Form.company_city'
        db.delete_column('forms_form', 'company_city')

        # Deleting field 'Form.company_state'
        db.delete_column('forms_form', 'company_state')

        # Deleting field 'Form.company_zipcode'
        db.delete_column('forms_form', 'company_zipcode')

        # Deleting field 'Form.company_country'
        db.delete_column('forms_form', 'company_country')

        # Deleting field 'Form.company_phone'
        db.delete_column('forms_form', 'company_phone')

        # Deleting field 'FormEntry.first_name'
        db.delete_column('forms_formentry', 'first_name')

        # Deleting field 'FormEntry.last_name'
        db.delete_column('forms_formentry', 'last_name')

        # Deleting field 'FormEntry.email'
        db.delete_column('forms_formentry', 'email')

        # Deleting field 'FormEntry.position_title'
        db.delete_column('forms_formentry', 'position_title')

        # Deleting field 'FormEntry.url'
        db.delete_column('forms_formentry', 'url')

        # Deleting field 'FormEntry.comments'
        db.delete_column('forms_formentry', 'comments')

        # Deleting field 'FormEntry.address'
        db.delete_column('forms_formentry', 'address')

        # Deleting field 'FormEntry.city'
        db.delete_column('forms_formentry', 'city')

        # Deleting field 'FormEntry.state'
        db.delete_column('forms_formentry', 'state')

        # Deleting field 'FormEntry.zipcode'
        db.delete_column('forms_formentry', 'zipcode')

        # Deleting field 'FormEntry.country'
        db.delete_column('forms_formentry', 'country')

        # Deleting field 'FormEntry.phone'
        db.delete_column('forms_formentry', 'phone')

        # Deleting field 'FormEntry.company_name'
        db.delete_column('forms_formentry', 'company_name')

        # Deleting field 'FormEntry.company_address'
        db.delete_column('forms_formentry', 'company_address')

        # Deleting field 'FormEntry.company_city'
        db.delete_column('forms_formentry', 'company_city')

        # Deleting field 'FormEntry.company_state'
        db.delete_column('forms_formentry', 'company_state')

        # Deleting field 'FormEntry.company_zipcode'
        db.delete_column('forms_formentry', 'company_zipcode')

        # Deleting field 'FormEntry.company_country'
        db.delete_column('forms_formentry', 'company_country')

        # Deleting field 'FormEntry.company_phone'
        db.delete_column('forms_formentry', 'company_phone')


    models = {
        'auth.group': {
            'Meta': {'object_name': 'Group'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '80'}),
            'permissions': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['auth.Permission']", 'symmetrical': 'False', 'blank': 'True'})
        },
        'auth.permission': {
            'Meta': {'ordering': "('content_type__app_label', 'content_type__model', 'codename')", 'unique_together': "(('content_type', 'codename'),)", 'object_name': 'Permission'},
            'codename': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'content_type': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['contenttypes.ContentType']"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '50'})
        },
        'auth.user': {
            'Meta': {'object_name': 'User'},
            'date_joined': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime(2013, 2, 5, 12, 25, 24, 812183)'}),
            'email': ('django.db.models.fields.EmailField', [], {'max_length': '75', 'blank': 'True'}),
            'first_name': ('django.db.models.fields.CharField', [], {'max_length': '30', 'blank': 'True'}),
            'groups': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['auth.Group']", 'symmetrical': 'False', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'is_active': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'is_staff': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'is_superuser': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'last_login': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime(2013, 2, 5, 12, 25, 24, 812093)'}),
            'last_name': ('django.db.models.fields.CharField', [], {'max_length': '30', 'blank': 'True'}),
            'password': ('django.db.models.fields.CharField', [], {'max_length': '128'}),
            'user_permissions': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['auth.Permission']", 'symmetrical': 'False', 'blank': 'True'}),
            'username': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '30'})
        },
        'contenttypes.contenttype': {
            'Meta': {'ordering': "('name',)", 'unique_together': "(('app_label', 'model'),)", 'object_name': 'ContentType', 'db_table': "'django_content_type'"},
            'app_label': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'model': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100'})
        },
        'entities.entity': {
            'Meta': {'ordering': "('entity_name',)", 'object_name': 'Entity'},
            'admin_notes': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            'allow_anonymous_edit': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'allow_anonymous_view': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'allow_member_edit': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'allow_member_view': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'allow_user_edit': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'allow_user_view': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'contact_name': ('django.db.models.fields.CharField', [], {'max_length': '200', 'blank': 'True'}),
            'create_dt': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'creator': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'entity_creator'", 'null': 'True', 'to': "orm['auth.User']"}),
            'creator_username': ('django.db.models.fields.CharField', [], {'max_length': '50'}),
            'email': ('django.db.models.fields.CharField', [], {'max_length': '120', 'blank': 'True'}),
            'entity_name': ('django.db.models.fields.CharField', [], {'max_length': '200', 'blank': 'True'}),
            'entity_parent': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'related_name': "'entity_children'", 'null': 'True', 'to': "orm['entities.Entity']"}),
            'entity_type': ('django.db.models.fields.CharField', [], {'max_length': '200', 'blank': 'True'}),
            'fax': ('django.db.models.fields.CharField', [], {'max_length': '50', 'blank': 'True'}),
            'guid': ('django.db.models.fields.CharField', [], {'max_length': '40'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'notes': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            'owner': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'entity_owner'", 'null': 'True', 'to': "orm['auth.User']"}),
            'owner_username': ('django.db.models.fields.CharField', [], {'max_length': '50'}),
            'phone': ('django.db.models.fields.CharField', [], {'max_length': '50', 'blank': 'True'}),
            'status': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'status_detail': ('django.db.models.fields.CharField', [], {'default': "'active'", 'max_length': '50'}),
            'summary': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            'update_dt': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'blank': 'True'}),
            'website': ('django.db.models.fields.CharField', [], {'max_length': '300', 'blank': 'True'})
        },
        'forms.field': {
            'Meta': {'ordering': "('position',)", 'object_name': 'Field'},
            'choices': ('django.db.models.fields.CharField', [], {'max_length': '1000', 'blank': 'True'}),
            'default': ('django.db.models.fields.CharField', [], {'max_length': '1000', 'blank': 'True'}),
            'field_function': ('django.db.models.fields.CharField', [], {'max_length': '64', 'null': 'True', 'blank': 'True'}),
            'field_type': ('django.db.models.fields.CharField', [], {'max_length': '64'}),
            'form': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'fields'", 'to': "orm['forms.Form']"}),
            'function_params': ('django.db.models.fields.CharField', [], {'max_length': '100', 'null': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'label': ('django.db.models.fields.CharField', [], {'max_length': '2000'}),
            'position': ('django.db.models.fields.PositiveIntegerField', [], {'default': '0'}),
            'required': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'visible': ('django.db.models.fields.BooleanField', [], {'default': 'True'})
        },
        'forms.fieldentry': {
            'Meta': {'object_name': 'FieldEntry'},
            'entry': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'fields'", 'to': "orm['forms.FormEntry']"}),
            'field': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'field'", 'to': "orm['forms.Field']"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'value': ('django.db.models.fields.CharField', [], {'max_length': '2000'})
        },
        'forms.form': {
            'Meta': {'object_name': 'Form'},
            'address': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'allow_anonymous_view': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'allow_member_edit': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'allow_member_view': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'allow_user_edit': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'allow_user_view': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'city': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'comments': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'company_address': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'company_city': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'company_country': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'company_name': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'company_phone': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'company_state': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'company_zipcode': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'completion_url': ('django.db.models.fields.URLField', [], {'max_length': '200', 'null': 'True', 'blank': 'True'}),
            'country': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'create_dt': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'creator': ('django.db.models.fields.related.ForeignKey', [], {'default': 'None', 'related_name': "'forms_form_creator'", 'null': 'True', 'to': "orm['auth.User']"}),
            'creator_username': ('django.db.models.fields.CharField', [], {'max_length': '50'}),
            'custom_payment': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'email': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'email_copies': ('django.db.models.fields.CharField', [], {'max_length': '2000', 'blank': 'True'}),
            'email_from': ('django.db.models.fields.EmailField', [], {'max_length': '75', 'blank': 'True'}),
            'email_text': ('django.db.models.fields.TextField', [], {'default': "''", 'max_length': '2000', 'blank': 'True'}),
            'entity': ('django.db.models.fields.related.ForeignKey', [], {'default': 'None', 'related_name': "'forms_form_entity'", 'null': 'True', 'blank': 'True', 'to': "orm['entities.Entity']"}),
            'first_name': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'intro': ('django.db.models.fields.TextField', [], {'max_length': '2000', 'blank': 'True'}),
            'last_name': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'owner': ('django.db.models.fields.related.ForeignKey', [], {'default': 'None', 'related_name': "'forms_form_owner'", 'null': 'True', 'to': "orm['auth.User']"}),
            'owner_username': ('django.db.models.fields.CharField', [], {'max_length': '50'}),
            'payment_methods': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['payments.PaymentMethod']", 'symmetrical': 'False', 'blank': 'True'}),
            'phone': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'position_title': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'recurring_payment': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'response': ('django.db.models.fields.TextField', [], {'max_length': '2000', 'blank': 'True'}),
            'send_email': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'slug': ('django.db.models.fields.SlugField', [], {'unique': 'True', 'max_length': '100', 'db_index': 'True'}),
            'state': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'status': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'status_detail': ('django.db.models.fields.CharField', [], {'default': "'active'", 'max_length': '50'}),
            'subject_template': ('django.db.models.fields.CharField', [], {'default': "'[title] - [first name]  [last name] - [phone]'", 'max_length': '200', 'null': 'True', 'blank': 'True'}),
            'template': ('django.db.models.fields.CharField', [], {'max_length': '50', 'blank': 'True'}),
            'title': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'update_dt': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'blank': 'True'}),
            'url': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'zipcode': ('django.db.models.fields.BooleanField', [], {'default': 'False'})
        },
        'forms.formentry': {
            'Meta': {'object_name': 'FormEntry'},
            'address': ('django.db.models.fields.CharField', [], {'max_length': '100', 'blank': 'True'}),
            'city': ('django.db.models.fields.CharField', [], {'max_length': '100', 'blank': 'True'}),
            'comments': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            'company_address': ('django.db.models.fields.CharField', [], {'max_length': '100', 'blank': 'True'}),
            'company_city': ('django.db.models.fields.CharField', [], {'max_length': '100', 'blank': 'True'}),
            'company_country': ('django.db.models.fields.CharField', [], {'max_length': '100', 'blank': 'True'}),
            'company_name': ('django.db.models.fields.CharField', [], {'max_length': '500', 'blank': 'True'}),
            'company_phone': ('django.db.models.fields.CharField', [], {'max_length': '50', 'blank': 'True'}),
            'company_state': ('django.db.models.fields.CharField', [], {'max_length': '100', 'blank': 'True'}),
            'company_zipcode': ('django.db.models.fields.CharField', [], {'max_length': '100', 'blank': 'True'}),
            'country': ('django.db.models.fields.CharField', [], {'max_length': '100', 'blank': 'True'}),
            'create_dt': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'creator': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'formentry_creator'", 'null': 'True', 'to': "orm['auth.User']"}),
            'email': ('django.db.models.fields.CharField', [], {'max_length': '200', 'blank': 'True'}),
            'entry_path': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '200', 'blank': 'True'}),
            'entry_time': ('django.db.models.fields.DateTimeField', [], {}),
            'first_name': ('django.db.models.fields.CharField', [], {'max_length': '200', 'blank': 'True'}),
            'form': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'entries'", 'to': "orm['forms.Form']"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'last_name': ('django.db.models.fields.CharField', [], {'max_length': '200', 'blank': 'True'}),
            'payment_method': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['payments.PaymentMethod']", 'null': 'True'}),
            'phone': ('django.db.models.fields.CharField', [], {'max_length': '50', 'blank': 'True'}),
            'position_title': ('django.db.models.fields.CharField', [], {'max_length': '500', 'blank': 'True'}),
            'pricing': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['forms.Pricing']", 'null': 'True'}),
            'state': ('django.db.models.fields.CharField', [], {'max_length': '100', 'blank': 'True'}),
            'update_dt': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'blank': 'True'}),
            'url': ('django.db.models.fields.URLField', [], {'max_length': '200', 'blank': 'True'}),
            'zipcode': ('django.db.models.fields.CharField', [], {'max_length': '100', 'blank': 'True'})
        },
        'forms.pricing': {
            'Meta': {'object_name': 'Pricing'},
            'billing_frequency': ('django.db.models.fields.IntegerField', [], {'default': '1'}),
            'billing_period': ('django.db.models.fields.CharField', [], {'default': "'month'", 'max_length': '50'}),
            'due_sore': ('django.db.models.fields.CharField', [], {'default': "'start'", 'max_length': '20'}),
            'form': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['forms.Form']"}),
            'has_trial_period': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'label': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'num_days': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'price': ('django.db.models.fields.DecimalField', [], {'null': 'True', 'max_digits': '10', 'decimal_places': '2', 'blank': 'True'}),
            'tax_rate': ('django.db.models.fields.DecimalField', [], {'default': '0', 'max_digits': '5', 'decimal_places': '4', 'blank': 'True'}),
            'taxable': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'trial_amount': ('django.db.models.fields.DecimalField', [], {'default': '0.0', 'null': 'True', 'max_digits': '15', 'decimal_places': '2', 'blank': 'True'}),
            'trial_period_days': ('django.db.models.fields.IntegerField', [], {'default': '0'})
        },
        'payments.paymentmethod': {
            'Meta': {'object_name': 'PaymentMethod'},
            'admin_only': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'human_name': ('django.db.models.fields.CharField', [], {'max_length': '200'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'is_online': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'machine_name': ('django.db.models.fields.CharField', [], {'max_length': '200'})
        },
        'perms.objectpermission': {
            'Meta': {'object_name': 'ObjectPermission'},
            'codename': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'content_type': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['contenttypes.ContentType']"}),
            'create_dt': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'group': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['user_groups.Group']", 'null': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'object_id': ('django.db.models.fields.IntegerField', [], {}),
            'user': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['auth.User']", 'null': 'True'})
        },
        'user_groups.group': {
            'Meta': {'ordering': "('name',)", 'object_name': 'Group'},
            'allow_anonymous_view': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'allow_member_edit': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'allow_member_view': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'allow_self_add': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'allow_self_remove': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'allow_user_edit': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'allow_user_view': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'auto_respond': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'auto_respond_priority': ('django.db.models.fields.FloatField', [], {'default': '0', 'blank': 'True'}),
            'create_dt': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'creator': ('django.db.models.fields.related.ForeignKey', [], {'default': 'None', 'related_name': "'user_groups_group_creator'", 'null': 'True', 'to': "orm['auth.User']"}),
            'creator_username': ('django.db.models.fields.CharField', [], {'max_length': '50'}),
            'description': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            'email_recipient': ('django.db.models.fields.CharField', [], {'max_length': '255', 'blank': 'True'}),
            'entity': ('django.db.models.fields.related.ForeignKey', [], {'default': 'None', 'related_name': "'user_groups_group_entity'", 'null': 'True', 'blank': 'True', 'to': "orm['entities.Entity']"}),
            'group': ('django.db.models.fields.related.OneToOneField', [], {'default': 'None', 'to': "orm['auth.Group']", 'unique': 'True', 'null': 'True'}),
            'guid': ('django.db.models.fields.CharField', [], {'max_length': '40'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'label': ('django.db.models.fields.CharField', [], {'max_length': '255', 'blank': 'True'}),
            'members': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['auth.User']", 'through': "orm['user_groups.GroupMembership']", 'symmetrical': 'False'}),
            'name': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '255'}),
            'notes': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            'owner': ('django.db.models.fields.related.ForeignKey', [], {'default': 'None', 'related_name': "'user_groups_group_owner'", 'null': 'True', 'to': "orm['auth.User']"}),
            'owner_username': ('django.db.models.fields.CharField', [], {'max_length': '50'}),
            'permissions': ('django.db.models.fields.related.ManyToManyField', [], {'symmetrical': 'False', 'related_name': "'group_permissions'", 'blank': 'True', 'to': "orm['auth.Permission']"}),
            'show_as_option': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'slug': ('tendenci.core.base.fields.SlugField', [], {'unique': 'True', 'max_length': '100', 'db_index': 'True'}),
            'status': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'status_detail': ('django.db.models.fields.CharField', [], {'default': "'active'", 'max_length': '50'}),
            'sync_newsletters': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'type': ('django.db.models.fields.CharField', [], {'default': "'distribution'", 'max_length': '75', 'blank': 'True'}),
            'update_dt': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'blank': 'True'})
        },
        'user_groups.groupmembership': {
            'Meta': {'unique_together': "(('group', 'member'),)", 'object_name': 'GroupMembership'},
            'create_dt': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'creator_id': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'creator_username': ('django.db.models.fields.CharField', [], {'max_length': '50'}),
            'group': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['user_groups.Group']"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'member': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'group_member'", 'to': "orm['auth.User']"}),
            'owner_id': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'owner_username': ('django.db.models.fields.CharField', [], {'max_length': '50'}),
            'role': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '255', 'blank': 'True'}),
            'sort_order': ('django.db.models.fields.IntegerField', [], {'default': '0', 'blank': 'True'}),
            'status': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'status_detail': ('django.db.models.fields.CharField', [], {'default': "'active'", 'max_length': '50'}),
            'update_dt': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'blank': 'True'})
        }
    }

    complete_apps = ['forms']
