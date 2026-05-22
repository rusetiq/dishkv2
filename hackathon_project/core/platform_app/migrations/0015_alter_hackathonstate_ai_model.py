from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('platform_app', '0014_hackathonstate_ai_model'),
    ]

    operations = [
        migrations.AlterField(
            model_name='hackathonstate',
            name='ai_model',
            field=models.CharField(choices=[('gemini-3.1-flash-lite', 'Gemini 3.1 Flash Lite'), ('gemini-3.1-flash', 'Gemini 3.1 Flash'), ('gemini-3.1-pro', 'Gemini 3.1 Pro'), ('gemini-2.5-flash-lite', 'Gemini 2.5 Flash Lite'), ('gemini-2.5-flash', 'Gemini 2.5 Flash'), ('gemini-2.5-pro', 'Gemini 2.5 Pro'), ('gemma-4-26b', 'Gemma 4 26B'), ('gemma-4-31b', 'Gemma 4 31B')], default='gemini-3.1-flash-lite', help_text='Gemini model used for AI hints — change takes effect immediately', max_length=100),
        ),
    ]
