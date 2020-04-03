from django.db import models
from tinymce.models import HTMLField
from db.base_model import BaseModel


# Create your models here.

class JobsType(BaseModel):
    """岗位类型模型类"""
    name = models.CharField(max_length=20, verbose_name='种类名称')
    logo = models.CharField(max_length=20, verbose_name='标识')
    image = models.ImageField(upload_to='type', verbose_name='岗位类型图片')

    class Meta:
        db_table = 'df_jobs_type'
        verbose_name = '职位种类'
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.name


class JobsSPU(BaseModel):
    """岗位SPU模型类"""
    name = models.CharField(max_length=20, verbose_name='岗位SPU名称')
    detail = HTMLField(blank=True, verbose_name='岗位详情')

    class Meta:
        db_table = 'df_jobs_spu'
        verbose_name = '岗位SPU'
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.name


class JobsSKU(BaseModel):
    """岗位SKU模型类"""
    # fromsite
    # positionType
    # positionName
    # salary
    # education
    # city
    # workYear
    # jobDes
    # company
    # companySize
    # financeStage
    # industryField
    # rate

    status_choices = (
        (0, '下线'),
        (1, '上线'),
    )


    fromsite = models.CharField(max_length=20, null=True, blank=True, verbose_name='数据来源')
    positionType = models.CharField(max_length=20, null=True, blank=True, verbose_name='岗位种类')
    positionName = models.CharField(max_length=20, null=True, blank=True, verbose_name='岗位名称')
    jobDes = models.CharField(max_length=1256, null=True, blank=True, verbose_name='岗位简介')
    education = models.CharField(max_length=20, null=True, blank=True, verbose_name='教育程度')
    company = models.CharField(max_length=20, null=True, blank=True, verbose_name='单位名称')
    companySize = models.CharField(max_length=20, null=True, blank=True, verbose_name='单位规模')
    financeStage = models.CharField(max_length=20, null=True, blank=True, verbose_name='单位类型')
    industryField = models.CharField(max_length=20, null=True, blank=True, verbose_name='行业领域')
    salary = models.CharField(max_length=20,null=True, blank=True, verbose_name='职薪')
    city = models.CharField(max_length=20, null=True, blank=True, verbose_name='岗位地点')
    workYear = models.CharField(max_length=20, null=True, blank=True, verbose_name='岗位年限')
    number = models.CharField(max_length=20,default=0, null=True, blank=True, verbose_name='招聘人数')
    status = models.SmallIntegerField(default=1, choices=status_choices, null=True, blank=True, verbose_name='岗位状态')

    class Meta:
        db_table = 'df_jobs_sku'
        verbose_name = '岗位'
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.name


class IndexJobsBanner(BaseModel):
    """首页轮播岗位展示模型类"""
    sku = models.ForeignKey('JobsSKU', on_delete=models.CASCADE, verbose_name='岗位')
    image = models.ImageField(upload_to='banner', verbose_name='图片')
    index = models.SmallIntegerField(default=0, verbose_name='展示顺序')

    class Meta:
        db_table = 'df_index_banner'
        verbose_name = '首页轮播图片'
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.sku.name


class IndexTypeJobsBanner(BaseModel):
    """首页分类岗位展示模型类"""
    DISPLAY_TYPE_CHOICES = (
        (0, '标题'),
        (1, '图片'),
    )
    type = models.ForeignKey('JobsType', on_delete=models.CASCADE, verbose_name='岗位类型')
    sku = models.ForeignKey('JobsSKU', on_delete=models.CASCADE, verbose_name='岗位')
    display_type = models.SmallIntegerField(default=1, choices=DISPLAY_TYPE_CHOICES, verbose_name='岗位显示方式')
    index = models.SmallIntegerField(default=0, verbose_name='展示顺序')

    class Meta:
        db_table = 'df_index_type_jobs'
        verbose_name = '主页分类展示岗位'
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.sku.name


class IndexPromotionBanner(BaseModel):
    """首页促销活动模型类"""
    url = models.CharField(max_length=256, verbose_name='活动链接')
    name = models.CharField(max_length=20, verbose_name='活动名称')
    image = models.ImageField(upload_to='jobs', verbose_name='图片路径')
    index = models.SmallIntegerField(default=0, verbose_name='展示顺序')

    class Meta:
        db_table = 'df_index_promotion'
        verbose_name = '主页促销活动'
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.name
