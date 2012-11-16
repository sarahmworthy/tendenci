import os
import chardet
import traceback

from django.core.management.base import BaseCommand
from django.shortcuts import get_object_or_404
from django.core.files.storage import default_storage
from django.core.files.base import ContentFile


class Command(BaseCommand):
    """
    Encode the uploaded file for MembershipDefault import.

    Usage:
        python manage.py encode_import_uploaded_file [mimport_id]

        example:
        python manage.py encode_import_uploaded_file 56
    """

    def handle(self, *args, **options):
        from tendenci.addons.memberships.models import MembershipImport

        mimport = get_object_or_404(MembershipImport,
                                        pk=args[0])
        if mimport.status == 'not_started':
            if mimport.upload_file:
                mimport.status = 'encoding'
                mimport.save()

                # encode to utf8 and write to path2
                path2 = '%s_utf8%s' % (os.path.splitext(
                                        mimport.upload_file.name))
                default_storage.save(path2, ContentFile(''))
                f = default_storage.open(mimport.upload_file.name)
                f2 = default_storage.open(path2, 'wb+')
                encoding_updated = False
                for chunk in f.chunks():
                    encoding = chardet.detect(chunk)['encoding']
                    if encoding not in ('ascii', 'utf8'):
                        if encoding == 'ISO-8859-1' or encoding == 'ISO-8859-2':
                            encoding = 'latin-1'
                        chunk = chunk.decode(encoding)
                        chunk = chunk.encode('utf8')
                        encoding_updated = True
                    f2.write(chunk)
                f2.close()
                if encoding_updated:
                    mimport.upload_file.file = f2
                    mimport.upload_file.name = f2.name
                    mimport.save()
                else:
                    default_storage.delete(path2)

                mimport.status = 'encoding_done'
                mimport.save()
