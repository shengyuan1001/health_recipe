from django.core.cache import cache
from django.shortcuts import redirect

from apps.blog.models import *

from utils.errors import ParameterException


# try:
#     if not request.user.is_authenticated():
#         return request.user
# except Exception as e:
#     print('用户登录异常：', e)
#     raise ParameterException({'code': 1111, 'msg': '您还未登录，请先登录'})

def authenticate(request):
    try:
        # token = request.data.get('token') if request.data.get('token')\
        #     else request.META.get('HTTP_TOKEN')  # 获取请求体中的名称为token的参数
        if request.data.get('token'):
            token = request.data.get('token')
        elif request.query_params.get('token'):
            token = request.query_params.get('token')
        elif request.META.get('HTTP_AUTHORIZATION'):
            token = request.META.get('HTTP_AUTHORIZATION')
        else:
            token = ''
        print(token)
        # user_id = cache.get(token)  # 获取token对相应的用户id
        # user = User.objects.get(pk=user_id)  # 如果用户未登录，则此处报错
        return ''
    except Exception as e:
        print('用户登录异常：', e)
        return ParameterException({'code': 1111, 'msg': '您还未登录，请先登录'})
