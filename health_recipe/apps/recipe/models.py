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
    calorie = models.FloatField(default=0, verbose_name='卡路里值')
    vitamin_a = models.FloatField(default=0, verbose_name='维A值')
    vitamin_c = models.FloatField(default=0, verbose_name='维C值')
    vitamin_e = models.FloatField(default=0, verbose_name='维E值')
    vitamin_b1 = models.FloatField(default=0, verbose_name='维B1值')
    vitamin_b2 = models.FloatField(default=0, verbose_name='维B2值')
    protein = models.FloatField(default=0, verbose_name='蛋白质值')
    axunge = models.FloatField(default=0, verbose_name='脂肪值')
    carbohydrate = models.FloatField(default=0, verbose_name='碳水化合物值')
    dietary_fiber = models.FloatField(default=0, verbose_name='膳食纤维值')

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
    r_name = models.CharField(max_length=25, verbose_name='食谱名称', default='')
    img = models.ImageField(upload_to='recipe', verbose_name='食谱图片')
    content = models.CharField(max_length=255, verbose_name='食谱内容', default='')
    add_time = models.DateTimeField(auto_now=True, verbose_name='创建时间')
    flag = models.IntegerField(default=0, verbose_name='是否为每日一餐', choices=((0, '否'), (1, '是')))

    class Meta:
        db_table = "recipe"

    def show_img(self):
        try:
            img = mark_safe('<a href="{}"><img src="{}" width="50px" /></a>'.format(self.img.url, self.img.url))
        except Exception as e:
            img = ''
        return img

    show_img.short_description = '图片'
    show_img.allow_tags = True
