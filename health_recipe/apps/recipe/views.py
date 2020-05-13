from rest_framework.viewsets import ModelViewSet

from apps.recipe.serializers import *
from utils.page import Pagination


# 食物分类视图
class ClassFoodViewSet(ModelViewSet):
    queryset = ClassFoodModel.objects.all()
    serializer_class = ClassFoodSerializer
    pagination_class = Pagination  # 自定义分页会覆盖settings全局配置的【url后加“?p='page'”】
    # filter_class = WhAuthUserFilter
    # authentication_classes = (WhTokenAuthentication,)


# 食物视图
class FoodViewSet(ModelViewSet):
    queryset = FoodModel.objects.all()
    serializer_class = FoodSerializer
    pagination_class = Pagination  # 自定义分页会覆盖settings全局配置的【url后加“?p='page'”】
    # filter_class = WhAuthUserFilter
    # authentication_classes = (WhTokenAuthentication,)


# 食谱分类视图
class RecipeViewSet(ModelViewSet):
    queryset = RecipeModel.objects.all()
    serializer_class = RecipeModelSerializer
    pagination_class = Pagination  # 自定义分页会覆盖settings全局配置的【url后加“?p='page'”】
    # filter_class = WhAuthUserFilter
    # authentication_classes = (WhTokenAuthentication,)
