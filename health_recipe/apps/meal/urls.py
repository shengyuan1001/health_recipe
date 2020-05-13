#  -*- codeing: utf-8 -*- #
# 作者: bob
# 日期: 2020/5/9
from rest_framework.routers import SimpleRouter

from apps.users.views import AuthUserViewSet

Users_router = SimpleRouter()
Users_router.register(r'users', AuthUserViewSet)
