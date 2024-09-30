# Generated by Django 5.1.1 on 2024-09-30 11:46

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('tasks', '0006_remove_task_label_task_labels'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='task',
            name='labels',
        ),
        migrations.RemoveField(
            model_name='membership',
            name='label',
        ),
        migrations.RemoveField(
            model_name='membership',
            name='task',
        ),
        migrations.RemoveField(
            model_name='task',
            name='status',
        ),
        migrations.RemoveField(
            model_name='task',
            name='author',
        ),
        migrations.RemoveField(
            model_name='task',
            name='executor',
        ),
        migrations.DeleteModel(
            name='Label',
        ),
        migrations.DeleteModel(
            name='Membership',
        ),
        migrations.DeleteModel(
            name='Status',
        ),
        migrations.DeleteModel(
            name='Task',
        ),
    ]
