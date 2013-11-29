import os
import zipfile
import urllib
from shutil import rmtree, move

from django.core.management.base import BaseCommand, CommandError
from django.conf import settings


class Command(BaseCommand):

    def handle(self, theme_url=None, **options):
        from tendenci.core.base.models import UpdateTracker

        UpdateTracker.start()
        if not theme_url:
            theme_url = "https://github.com/tendenci/tendenci-themes/archive/master.zip"

        themes_dir_path = os.path.join(settings.PROJECT_ROOT, "themes")

        # Copy the theme files down
        theme_download = urllib.urlopen(theme_url)
        theme_zip_path = os.path.join(themes_dir_path, "themes.zip")
        theme_zip = open(theme_zip_path, 'wb')
        theme_zip.write(theme_download.read())
        theme_zip.close()

        # Unzip the theme files
        theme_zip_file = open(theme_zip_path, 'r')
        zfobj = zipfile.ZipFile(theme_zip_file)
        unzip_dirname = "themes"
        for i, name in enumerate(zfobj.namelist()):
            if i == 0:
                unzip_dirname = name[:-1]
            if name.endswith('/'):
                try:  # Don't try to create a directory if exists
                    os.mkdir(os.path.join(themes_dir_path, name))
                except:
                    pass
            else:
                outfile = open(os.path.join(themes_dir_path, name), 'wb')
                outfile.write(zfobj.read(name))
                outfile.close()

        # Delete the zip file
        os.remove(theme_zip_path)

        # Move the themes out of the unzipped folder
        unzip_dir_path = os.path.join(themes_dir_path, unzip_dirname)
        for name in os.listdir(unzip_dir_path):
            # Check for themes
            if os.path.isdir(os.path.join(unzip_dir_path, name)) and not name.startswith('.'):
                # Check if the theme already exists
                if not os.path.isdir(os.path.join(themes_dir_path, name)):
                    move(os.path.join(unzip_dir_path, name), os.path.join(themes_dir_path, name))

        rmtree(os.path.join(themes_dir_path, unzip_dirname))
        UpdateTracker.end()
