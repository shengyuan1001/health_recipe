from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.hashers import make_password
from django.contrib.auth.models import User

from django.http import QueryDict
from rest_framework import status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.viewsets import *
from apps.users.serializers import AuthUserSerializer
# from utils import HealthAuthentication
from utils.page import Pagination


# 用户视图
class AuthUserViewSet(ModelViewSet):
    queryset = User.objects.all()
    serializer_class = AuthUserSerializer
    pagination_class = Pagination  # 自定义分页会覆盖settings全局配置的【url后加“?p='page'”】
    # filter_class = WhAuthUserFilter
    # authentication_classes = (Authentication,)


class LoginViewSet(GenericViewSet,
                   mixins.CreateModelMixin,
                   mixins.RetrieveModelMixin,
                   mixins.UpdateModelMixin):
    queryset = User.objects.all()
    serializer_class = AuthUserSerializer
    pagination_class = Pagination  # 自定义分页会覆盖settings全局配置的【url后加“?p='page'”】

    def create(self, request, *args, **kwargs):
        data = QueryDict.dict(request.data)
        data['password'] = make_password(data['password'])
        serializer = self.get_serializer(data=data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        data = serializer.data
        res = {
            'code': 200,
            'data': {'id': data['id'], 'username': data['username']}
        }
        return Response(res)

    def retrieve(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(instance)
        data = serializer.data
        res = {
            'code': 200,
            'data': {'id': data['id'], 'username': data['username'], 'password': data['password']}
        }
        return Response(res)

    @action(methods=["POST"], detail=False)
    def login(self, request, *args, **kwargs):
        data = QueryDict.dict(request.data)
        username = data['username']
        password = data['password']
        user = authenticate(username=username, password=password)
        if user is not None:
            if user.is_active:
                login(request, user)
                data = {'code': 200, 'msg': '登录成功', 'user_id': user.id, 'username': user.username}
            else:
                data = {'code': 201, 'msg': '用户未激活'}
        else:
            data = {'code': 202, 'msg': '用户名或密码错误'}
        res = {'data': data}
        return Response(res)

    @action(methods=['GET'], detail=False)
    def logout(self, request, *args, **kwargs):
        logout(request)
        data = {'code': 200, 'msg': '已退成登录'}
        res = {'data': data}
        return Response(res)

    def update(self, request, *args, **kwargs):
        data = QueryDict.dict(request.data)
        newpwd = data.get('password')
        # oldpwd = data.get('oldusername')
        partial = kwargs.pop('partial', False)
        instance = self.get_object()
        # if newpwd and oldpwd:
        #     if instance.check_password(oldpwd):
        #         print(instance.password)
        instance.set_password(newpwd)
        instance.save()
        data['password'] = instance.password
        serializer = self.get_serializer(instance, data=data, partial=partial)
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)

        if getattr(instance, '_prefetched_objects_cache', None):
            # If 'prefetch_related' has been applied to a queryset, we need to
            # forcibly invalidate the prefetch cache on the instance.
            instance._prefetched_objects_cache = {}
        data = serializer.data
        res = {
            'code': 200,
            'data': {'id': data['id'], 'username': data['username']}
        }
        return Response(res)
