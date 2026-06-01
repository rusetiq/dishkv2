from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('platform_app', '0012_bonusquestion_is_paused_bonusquestion_paused_at'),
    ]

    operations = [
        migrations.AddField(
            model_name='hackathonstate',
            name='hints_enabled',
            field=models.BooleanField(default=True, help_text='Allow teams to request AI hints on problem pages'),
        ),
        migrations.AddField(
            model_name='hackathonstate',
            name='onboarding_tour_enabled',
            field=models.BooleanField(default=True, help_text='Show the guided UI tour to teams on their first visit to a problem'),
        ),
    ]
