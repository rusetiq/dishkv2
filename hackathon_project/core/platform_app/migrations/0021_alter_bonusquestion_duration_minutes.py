from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('platform_app', '0020_bonusquestion_auto_start_triggered_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='bonusquestion',
            name='duration_minutes',
            field=models.IntegerField(default=10),
        ),
    ]
