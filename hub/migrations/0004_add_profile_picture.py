from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('hub', '0003_rename_upload_to_project_add_statistic'),
    ]

    operations = [
        migrations.AddField(
            model_name='customuser',
            name='profile_picture',
            field=models.ImageField(blank=True, null=True, upload_to='profile_pictures/'),
        ),
    ]
