"""
Direct SQL migration to add created_at to core_newspost.

Migration 0018 (AddField) may have been recorded in django_migrations
without the ALTER TABLE running (same pattern as 0015-0017).
This RunSQL uses IF NOT EXISTS so it is always safe to run.
"""
from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0018_newspost_created_at'),
    ]

    operations = [
        migrations.RunSQL(
            sql="""
                DO $$
                BEGIN
                    IF NOT EXISTS (
                        SELECT 1 FROM information_schema.columns
                        WHERE table_name = 'core_newspost'
                          AND column_name = 'created_at'
                    ) THEN
                        ALTER TABLE core_newspost
                        ADD COLUMN created_at TIMESTAMP WITH TIME ZONE NOT NULL
                        DEFAULT NOW();
                    END IF;
                END $$;
            """,
            reverse_sql=migrations.RunSQL.noop,
        ),
    ]
