from django.contrib.auth.models import User
from django.db import models
from django.utils.safestring import mark_safe


# Create your models here.


# 食物分类模型
class ClassFoodModel(models.Model):
    name = models.CharField(max_length=25, verbose_name='食物名称')
    img = models.ImageField(upload_to='class_food', verbose_name='食物分类图片', null=True, blank=True)

    class Meta:
        db_table = "class_food"

    def show_img(self):
        try:
            img = mark_safe('<a href="{}"><img src="{}" width="50px" /></a>'.format(self.img.url, self.img.url))
        except Exception as e:
            img = ''
        return img

    show_img.short_description = '图片'
    show_img.allow_tags = True


# 食物模型
class FoodModel(models.Model):
    f_class = models.ForeignKey(ClassFoodModel, on_delete=models.CASCADE, verbose_name='关联食物分类')
    name = models.CharField(max_length=25, verbose_name='食物名称')
    img = models.ImageField(upload_to='food', verbose_name='食物图片', null=True, blank=True)
    f_calorie = models.FloatField(default=0, verbose_name='食物含有卡路里值')

    class Meta:
        db_table = "food"

    def class_name(self):
        return self.f_class.name

    class_name.short_description = '关联食物分类'

    def show_img(self):
        try:
            img = mark_safe('<a href="{}"><img src="{}" width="50px" /></a>'.format(self.img.url, self.img.url))
        except Exception as e:
            img = ''
        return img

    show_img.short_description = '图片'
    show_img.allow_tags = True


# 食谱模型
class RecipeModel(models.Model):
    u_recipe = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name='关联用户')
    r_name = models.CharField(max_length=25, verbose_name='食谱名称')
    r_food1 = models.ForeignKey(FoodModel, on_delete=models.CASCADE, related_name='recipe_org1', verbose_name='关联食物',
                                null=True, blank=True)
    r_food2 = models.ForeignKey(FoodModel, on_delete=models.CASCADE, related_name='recipe_org2', verbose_name='关联食物',
                                null=True, blank=True)
    r_food3 = models.ForeignKey(FoodModel, on_delete=models.CASCADE, related_name='recipe_org3', verbose_name='关联食物',
                                null=True, blank=True)
    r_food4 = models.ForeignKey(FoodModel, on_delete=models.CASCADE, related_name='recipe_org4', verbose_name='关联食物',
                                null=True, blank=True)
    r_food5 = models.ForeignKey(FoodModel, on_delete=models.CASCADE, related_name='recipe_org5', verbose_name='关联食物',
                                null=True, blank=True)
    r_calorie = models.FloatField(default=0, verbose_name='食谱含有卡路里值')
    add_time = models.DateTimeField(auto_now=True, verbose_name='创建时间')
    flag = models.IntegerField(default=0, verbose_name='是否为每日一餐', choices=((0, '否'), (1, '是')))

    class Meta:
        db_table = "recipe"

    def food1(self):
        return self.r_food1.name

    def food2(self):
        return self.r_food2.name

    def food3(self):
        return self.r_food3.name

    def food4(self):
        return self.r_food4.name

    def food5(self):
        return self.r_food5.name

    food1.short_description = '食物'
    food2.short_description = '食物'
    food3.short_description = '食物'
    food4.short_description = '食物'
    food5.short_description = '食物'
