from django.db import models


class BaseModel(models.Model):
    '''模型抽象基类'''
    create_time = models.DateTimeField(auto_now=True,null=True, blank=True,verbose_name="创建时间")
    updata_time = models.DateTimeField(auto_now=True,null=True, blank=True,verbose_name='更新时间')
    is_delete = models.BooleanField(default=False,null=True, blank=True,verbose_name='删除标记')

    class Meta:
        '''说明是抽象基类'''
        abstract = True
