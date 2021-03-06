# Generated by Django 3.0.6 on 2020-05-13 04:48

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('recipe', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='MealModel',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(default='默认推荐', max_length=255, verbose_name='每日一餐')),
                ('add_time', models.DateTimeField(auto_now=True, verbose_name='创建时间')),
                ('recipe', models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, to='recipe.RecipeModel', verbose_name='关联食谱')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL, verbose_name='关联用户')),
            ],
            options={
                'db_table': 'meal',
            },
        ),
    ]
