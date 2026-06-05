"""
Direct SQL migration to make core_newspost.date nullable.

Migration 0015 (AlterField) may fail on Render's Postgres if the build
rolls back before migrate completes. This RunSQL approach is explicit and
safe — ALTER COLUMN ... DROP NOT NULL is a no-op if the column is already
nullable, so it never errors on a repeated run.
"""
from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0015_newspost_date_optional'),
    ]

    operations = [
        migrations.RunSQL(
            sql="ALTER TABLE core_newspost ALTER COLUMN date DROP NOT NULL;",
            reverse_sql="ALTER TABLE core_newspost ALTER COLUMN date SET NOT NULL;",
        ),
    ]
