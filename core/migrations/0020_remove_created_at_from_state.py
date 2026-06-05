"""
Remove created_at from Django's model state so the ORM stops selecting it.

Migrations 0018 and 0019 are already recorded in django_migrations but the
column was never added to the production DB (the migrations were fake-applied).
This migration uses SeparateDatabaseAndState to tell Django the field no longer
exists in its model state — without touching the database at all.
Result: every NewsPost queryset stops including created_at in SELECT,
so the ProgrammingError disappears immediately.
"""
from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0019_newspost_created_at_sql'),
    ]

    operations = [
        migrations.SeparateDatabaseAndState(
            # Tell Django's ORM: this field doesn't exist on the model.
            state_operations=[
                migrations.RemoveField(
                    model_name='newspost',
                    name='created_at',
                ),
            ],
            # Don't touch the database — column may or may not exist, either way is fine.
            database_operations=[],
        ),
    ]
