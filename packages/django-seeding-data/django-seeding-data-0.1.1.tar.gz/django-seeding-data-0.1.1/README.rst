Django Seeding Data
=====

Django Seeding Data is Django app for seeding data in existing DB.

Quick start
-----------

1. Add "django_seeding_data" to your INSTALLED_APPS setting like this::

      INSTALLED_APPS = (
          ...
          'seeding',
      )

2. Add "SEEDING_DIR" to your settings.py file like this::

    SEEDING_DIR = "mainapp/seeding/"

3. Run `python manage.py seeding create` to create new seeding file in path from previous instruction.

4. Write some seeding code in method `seeding` from class `Seeding`, for create superuser, or add new groups.

5. Run `python manage.py seeding seed` to apply new seeding files that was never applied on this DB instance.

