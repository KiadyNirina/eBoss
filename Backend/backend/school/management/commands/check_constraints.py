# yourapp/management/commands/check_constraints.py

from django.core.management.base import BaseCommand
from django.db import connection

class Command(BaseCommand):
    help = 'Check database constraints for django_admin_log table'

    def handle(self, *args, **kwargs):
        with connection.cursor() as cursor:
            cursor.execute("SHOW TABLES LIKE 'django_content_type';")
            result = cursor.fetchall()
            self.stdout.write("Tables: " + str(result))

            if result:
                cursor.execute("SHOW CREATE TABLE django_content_type;")
                result = cursor.fetchall()
                self.stdout.write("Table Structure: " + str(result))
            else:
                self.stdout.write("Table `django_content_type` does not exist.")
