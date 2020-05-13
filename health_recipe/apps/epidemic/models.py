from django.db import models


# Create your models here.

# 全球国家疫情模型
class EpidemicCountry(models.Model):
    name = models.CharField(max_length=25, verbose_name='国家名称')
    confirm = models.IntegerField(verbose_name='累计确诊人数')
    confirmIncr = models.IntegerField(verbose_name='新增确诊人数')
    suspect = models.IntegerField(verbose_name='疑似人数')
    dead = models.IntegerField(verbose_name='累计死亡人数')
    deadIncr = models.IntegerField(verbose_name='新增死亡人数')
    heal = models.IntegerField(verbose_name='累计治愈人数')
    healIncr = models.IntegerField(verbose_name='新增治愈人数')
    deadRate = models.FloatField(verbose_name='死亡率')
    healRate = models.FloatField(verbose_name='治愈率')
    detail_json_url = models.CharField(max_length=255, verbose_name='详细数据接口')
    date = models.CharField(max_length=25, verbose_name='产生数据日期')

    class Mete:
        db_table = "country_epidemic"


# 全球国家历史疫情模型
class DetailEpidemicCountry(models.Model):
    e = models.ForeignKey(EpidemicCountry, on_delete=models.CASCADE, verbose_name='关联全球国家疫情模型')
    name = models.CharField(max_length=25, verbose_name='国家名称')
    confirm = models.IntegerField(verbose_name='累计确诊人数')
    confirmIncr = models.IntegerField(verbose_name='新增确诊人数')
    suspect = models.IntegerField(verbose_name='疑似人数')
    suspectIncr = models.IntegerField(verbose_name='新增疑似人数')
    dead = models.IntegerField(verbose_name='累计死亡人数')
    deadIncr = models.IntegerField(verbose_name='新增死亡人数')
    heal = models.IntegerField(verbose_name='累计治愈人数')
    healIncr = models.IntegerField(verbose_name='新增治愈人数')
    deadRate = models.FloatField(verbose_name='死亡率')
    healRate = models.FloatField(verbose_name='治愈率')
    date = models.CharField(max_length=25, verbose_name='产生数据日期')

    class Meta:
        db_table = 'history_epidemic_country'
