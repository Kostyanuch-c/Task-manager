# Generated by Django 5.1.1 on 2024-09-28 09:14

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('tasks', '0004_alter_task_labels'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='task',
            name='labels',
        ),
        migrations.AddField(
            model_name='task',
            name='label',
            field=models.ManyToManyField(blank=True, related_name='task_as_label', through='tasks.Membership', to='tasks.label', verbose_name='Label'),
        ),
    ]
