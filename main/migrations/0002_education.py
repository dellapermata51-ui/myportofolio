import uuid
from django.db import migrations, models

class Migration(migrations.Migration):

    dependencies = [
        ('main', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Education',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('institution', models.CharField(max_length=255)),
                ('program', models.CharField(blank=True, default='', max_length=255)),
                ('level', models.CharField(
                    choices=[
                        ('sd', 'SD'),
                        ('smp', 'SMP'),
                        ('sma', 'SMA/SMK'),
                        ('s1', 'S1'),
                        ('s2', 'S2'),
                        ('s3', 'S3'),
                    ],
                    default='s1',
                    max_length=20,
                )),
                ('description', models.TextField(blank=True, default='')),
                ('thumbnail', models.URLField(blank=True, null=True)),
                ('started_at', models.DateTimeField(auto_now_add=True)),
                ('ended_at', models.DateTimeField(blank=True, null=True)),
            ],
        ),
    ]