# Generated by Django 2.2 on 2020-03-20 09:19

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('job', '0003_auto_20200320_1702'),
    ]

    operations = [
        migrations.AddField(
            model_name='jobssku',
            name='fromsite',
            field=models.CharField(blank=True, max_length=20, null=True, verbose_name='数据来源'),
        ),
        migrations.AlterField(
            model_name='jobssku',
            name='Size',
            field=models.CharField(blank=True, max_length=20, null=True, verbose_name='单位规模'),
        ),
        migrations.AlterField(
            model_name='jobssku',
            name='city',
            field=models.CharField(blank=True, max_length=20, null=True, verbose_name='岗位地点'),
        ),
        migrations.AlterField(
            model_name='jobssku',
            name='company',
            field=models.CharField(blank=True, max_length=20, null=True, verbose_name='岗位单位'),
        ),
        migrations.AlterField(
            model_name='jobssku',
            name='desc',
            field=models.CharField(blank=True, max_length=1256, null=True, verbose_name='岗位简介'),
        ),
        migrations.AlterField(
            model_name='jobssku',
            name='education',
            field=models.CharField(blank=True, max_length=20, null=True, verbose_name='教育程度'),
        ),
        migrations.AlterField(
            model_name='jobssku',
            name='financeStage',
            field=models.CharField(blank=True, max_length=20, null=True, verbose_name='单位类型'),
        ),
        migrations.AlterField(
            model_name='jobssku',
            name='industryField',
            field=models.CharField(blank=True, max_length=20, null=True, verbose_name='行业领域'),
        ),
        migrations.AlterField(
            model_name='jobssku',
            name='name',
            field=models.CharField(blank=True, max_length=20, null=True, verbose_name='岗位名称'),
        ),
        migrations.AlterField(
            model_name='jobssku',
            name='number',
            field=models.IntegerField(blank=True, default=0, null=True, verbose_name='招聘人数'),
        ),
        migrations.AlterField(
            model_name='jobssku',
            name='salary',
            field=models.IntegerField(blank=True, null=True, verbose_name='职薪'),
        ),
        migrations.AlterField(
            model_name='jobssku',
            name='status',
            field=models.SmallIntegerField(blank=True, choices=[(0, '下线'), (1, '上线')], default=1, null=True, verbose_name='岗位状态'),
        ),
        migrations.AlterField(
            model_name='jobssku',
            name='stock',
            field=models.IntegerField(blank=True, default=1, null=True, verbose_name='岗位库存'),
        ),
        migrations.AlterField(
            model_name='jobssku',
            name='workYear',
            field=models.CharField(blank=True, max_length=20, null=True, verbose_name='岗位年限'),
        ),
    ]