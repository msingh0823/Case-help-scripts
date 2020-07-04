import sys, os, django

sys.path.append('/opt/avi/python/bin/portal')
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'portal.settings_full')

from api.models import Backup

django.setup()

if __name__ == '__main__':
    for backup in Backup.objects.all():
        backup.delete()

