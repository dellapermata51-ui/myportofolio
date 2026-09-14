import uuid
from django.db import migrations, models

class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Experience',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('title', models.CharField(max_length=255)),
                ('description', models.TextField()),
                ('category', models.CharField(
                    choices=[
                        ('organization', 'Organisasi'),
                        ('committee', 'Kepanitiaan'),
                        ('volunteer', 'Volunteer'),
                        ('competition', 'Lomba/Kompetisi'),
                        ('training', 'Pelatihan/Sertifikasi'),
                    ],
                    default='organization',
                    max_length=20,
                )),
                ('thumbnail', models.URLField(blank=True, null=True)),
                ('started_at', models.DateTimeField(auto_now_add=True)),
                ('ended_at', models.DateTimeField(blank=True, null=True)),
            ],
        ),
    ]