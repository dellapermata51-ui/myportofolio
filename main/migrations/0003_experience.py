from django.db import migrations, models

class Migration(migrations.Migration):

    dependencies = [
        ('main', '0002_education'),
    ]

    operations = [
        migrations.AddField(
            model_name='experience',
            name='organization',
            field=models.CharField(blank=True, default='', max_length=255),
        ),
    ]