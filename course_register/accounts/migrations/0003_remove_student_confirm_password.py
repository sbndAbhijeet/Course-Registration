# Generated by Django 5.1.5 on 2025-02-28 15:50

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0002_remove_student_id_alter_student_email'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='student',
            name='confirm_password',
        ),
    ]
