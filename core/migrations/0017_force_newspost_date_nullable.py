"""
Emergency fix: force the core_newspost.date column to be nullable via direct SQL.

Migrations 0015 and 0016 may already be recorded in django_migrations as
'applied' (from a failed earlier attempt) while the actual ALTER TABLE was
never committed to PostgreSQL.  This migration has a brand-new name that
Django has never seen, so it will always run fresh.

ALTER COLUMN date DROP NOT NULL is idempotent in PostgreSQL — safe to run
even if the column is already nullable.
"""
from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0016_newspost_date_nullable_sql'),
    ]

    operations = [
        migrations.RunSQL(
            sql="""
                DO $$
                BEGIN
                    IF EXISTS (
                        SELECT 1 FROM information_schema.columns
                        WHERE table_name = 'core_newspost'
                          AND column_name = 'date'
                          AND is_nullable = 'NO'
                    ) THEN
                        ALTER TABLE core_newspost ALTER COLUMN date DROP NOT NULL;
                    END IF;
                END $$;
            """,
            reverse_sql=migrations.RunSQL.noop,
        ),
    ]
