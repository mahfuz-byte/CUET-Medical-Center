# Generated migration for extended user profile fields

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0002_otp_user_password_plaintext_alter_user_first_name'),
    ]

    operations = [
        # Student fields
        migrations.AddField(
            model_name='user',
            name='dept',
            field=models.CharField(blank=True, max_length=100, null=True),
        ),
        migrations.AddField(
            model_name='user',
            name='age',
            field=models.IntegerField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='user',
            name='blood_group',
            field=models.CharField(
                blank=True,
                choices=[
                    ('A+', 'A+'),
                    ('A-', 'A-'),
                    ('B+', 'B+'),
                    ('B-', 'B-'),
                    ('O+', 'O+'),
                    ('O-', 'O-'),
                    ('AB+', 'AB+'),
                    ('AB-', 'AB-'),
                ],
                max_length=5,
                null=True,
            ),
        ),
        # Doctor fields
        migrations.AddField(
            model_name='user',
            name='specialization',
            field=models.CharField(blank=True, max_length=100, null=True),
        ),
        migrations.AddField(
            model_name='user',
            name='qualification',
            field=models.CharField(blank=True, max_length=255, null=True),
        ),
        migrations.AddField(
            model_name='user',
            name='license_number',
            field=models.CharField(blank=True, max_length=50, null=True),
        ),
        migrations.AddField(
            model_name='user',
            name='experience',
            field=models.IntegerField(blank=True, null=True),
        ),
        # Admin fields
        migrations.AddField(
            model_name='user',
            name='designation',
            field=models.CharField(blank=True, max_length=100, null=True),
        ),
        migrations.AddField(
            model_name='user',
            name='department',
            field=models.CharField(blank=True, max_length=100, null=True),
        ),
        migrations.AddField(
            model_name='user',
            name='employee_id',
            field=models.CharField(blank=True, max_length=50, null=True),
        ),
    ]
