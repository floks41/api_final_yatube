# Generated by Django 3.2.16 on 2023-04-26 18:28

from django.db import migrations, models
import django.db.models.expressions


class Migration(migrations.Migration):

    dependencies = [
        ('posts', '0002_auto_20230421_1821'),
    ]

    operations = [
        migrations.RemoveConstraint(
            model_name='follow',
            name='unique_user_author',
        ),
        migrations.RemoveConstraint(
            model_name='follow',
            name='users_cannot_follow_themselves',
        ),
        migrations.RenameField(
            model_name='follow',
            old_name='author',
            new_name='following',
        ),
        migrations.AddConstraint(
            model_name='follow',
            constraint=models.UniqueConstraint(fields=('user', 'following'), name='unique_user_author'),
        ),
        migrations.AddConstraint(
            model_name='follow',
            constraint=models.CheckConstraint(check=models.Q(('user', django.db.models.expressions.F('following')), _negated=True), name='users_cannot_follow_themselves'),
        ),
    ]
