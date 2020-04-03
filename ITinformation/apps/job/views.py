from django.shortcuts import render, redirect
from django.views.generic import View
from django.urls import reverse
# from goods.models import GoodsType, IndexGoodsBanner, \
#     IndexPromotionBanner, IndexTypeGoodsBanner, GoodsSKU
from django_redis import get_redis_connection
from django.core.cache import cache
# from order.models import OrderGoods
from django.core.paginator import Paginator

# Create your views here.
class IndexView(View):

    def get(self, request):
        return render(request,'index.html')
