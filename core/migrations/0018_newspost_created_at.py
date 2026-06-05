from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0017_force_newspost_date_nullable'),
    ]

    operations = [
        migrations.AddField(
            model_name='newspost',
            name='created_at',
            field=models.DateTimeField(auto_now_add=True, default=django.utils.timezone.now),
            preserve_default=False,
        ),
        migrations.AlterModelOptions(
            name='newspost',
            options={'ordering': ['-created_at']},
        ),
    ]
