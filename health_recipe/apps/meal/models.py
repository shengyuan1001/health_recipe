from django.contrib.auth.models import User
from django.db import models


# Create your models here.
from apps.recipe.models import RecipeModel


class MealModel(models.Model):
    name = models.CharField(max_length=255, verbose_name='每日一餐', default='默认推荐')
    user = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name='关联用户')
    recipe = models.ForeignKey(RecipeModel, on_delete=models.CASCADE, verbose_name='关联食谱', default=1)
    add_time = models.DateTimeField(auto_now=True, verbose_name='创建时间')

    class Meta:
        db_table = 'meal'

    def m_user(self):
        return self.user.username

    m_user.short_description = '关联用户'

    def m_recipe(self):
        return self.recipe.r_name

    m_recipe.short_description = '关联食谱'

