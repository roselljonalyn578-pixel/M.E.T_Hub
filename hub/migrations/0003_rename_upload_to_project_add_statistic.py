from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
from django.core.validators import MinValueValidator, MaxValueValidator


class Migration(migrations.Migration):

    dependencies = [
        ('hub', '0002_upload_public_id'),
    ]

    operations = [
        migrations.CreateModel(
            name='Statistic',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('metric_name', models.CharField(max_length=100)),
                ('metric_value', models.DecimalField(decimal_places=2, max_digits=10)),
                ('recorded_at', models.DateTimeField(auto_now_add=True)),
                ('notes', models.TextField(blank=True)),
                ('project', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='statistics', to='hub.upload')),
            ],
            options={
                'ordering': ['-recorded_at'],
            },
        ),
        migrations.AlterModelOptions(
            name='upload',
            options={'ordering': ['-created_at']},
        ),
        migrations.AlterModelTable(
            name='upload',
            table='hub_upload',
        ),
    ]
