import uuid
from django.db import migrations, models

class Migration(migrations.Migration):

    dependencies = [
        ('main', '0003_experience'),
    ]

    operations = [
        migrations.CreateModel(
            name='Skill',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('name', models.CharField(max_length=100)),
                ('category', models.CharField(
                    choices=[
                        ('language', 'Programming Language'),
                        ('framework', 'Framework / Library'),
                        ('tool', 'Tool / Platform'),
                        ('soft', 'Soft Skill'),
                    ],
                    default='language',
                    max_length=20,
                )),
                ('level', models.CharField(
                    choices=[
                        ('beginner', 'Beginner'),
                        ('intermediate', 'Intermediate'),
                        ('advanced', 'Advanced'),
                        ('expert', 'Expert'),
                    ],
                    default='intermediate',
                    max_length=20,
                )),
                ('icon', models.URLField(blank=True, null=True)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
            ],
            options={
                'ordering': ['category', 'name'],
            },
        ),
    ]