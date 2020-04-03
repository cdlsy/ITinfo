# Generated by Django 2.2 on 2020-03-28 13:42

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('user', '0002_auto_20200320_1738'),
    ]

    operations = [
        migrations.AddField(
            model_name='address',
            name='age',
            field=models.IntegerField(blank=True, null=True, verbose_name='年龄'),
        ),
        migrations.AddField(
            model_name='address',
            name='education',
            field=models.CharField(blank=True, max_length=8, null=True, verbose_name='学历'),
        ),
        migrations.AddField(
            model_name='address',
            name='school',
            field=models.CharField(blank=True, max_length=12, null=True, verbose_name='学校'),
        ),
        migrations.AlterField(
            model_name='address',
            name='addr',
            field=models.CharField(blank=True, max_length=256, null=True, verbose_name='地址'),
        ),
        migrations.AlterField(
            model_name='address',
            name='receiver',
            field=models.CharField(blank=True, max_length=20, null=True, verbose_name='收件人'),
        ),
    ]
