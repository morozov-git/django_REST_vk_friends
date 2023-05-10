# Generated by Django 4.2.1 on 2023-05-10 17:46

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('friends', '0001_initial'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.AddField(
            model_name='friendshiprequest',
            name='receiver',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='receiver_users', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='friendshiprequest',
            name='sender',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='sender_users', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='friends',
            name='user1',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='user1_users', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='friends',
            name='user2',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='user2_users', to=settings.AUTH_USER_MODEL),
        ),
    ]