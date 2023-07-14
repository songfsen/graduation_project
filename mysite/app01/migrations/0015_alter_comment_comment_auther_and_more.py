# Generated by Django 4.1.7 on 2023-05-15 02:34

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0013_alter_user_avatar'),
        ('app01', '0014_alter_collection_collect_user_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='comment',
            name='comment_auther',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='blog.user', verbose_name='评论者'),
        ),
        migrations.AlterField(
            model_name='comment',
            name='commented_merchant',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='app01.merchant', verbose_name='被评论商家'),
        ),
    ]
