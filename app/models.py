from django.db import models


# Create your models here.

class Department(models.Model):
    """部分表"""
    # id = models.BigAutoField()
    title = models.CharField(verbose_name="标题", max_length=32)

    def __str__(self):
        return self.title


class UserInfo(models.Model):
    name = models.CharField(verbose_name="姓名", max_length=16)
    password = models.CharField(verbose_name="密码", max_length=64)
    age = models.IntegerField(verbose_name="年龄")
    account = models.DecimalField(verbose_name="账户余额", max_digits=10, decimal_places=2, default=0)
    create_time = models.DateField(verbose_name="入职时间")
    # 无约束
    # depart_id = models.BigIntegerField(verbose_name="部门ID")
    # 有约束  自动加上_id
    depart = models.ForeignKey(verbose_name="部门", to="Department", to_field="id", on_delete=models.CASCADE)
    # depart = models.ForeignKey(to="Department", to_field="id",blank=True, null=True, on_delete=models.SET_NULL)
    gender_chioces = (
        (1, "男"),
        (2, "女"),
    )  # 元组套元组
    gender = models.SmallIntegerField(verbose_name="性别", choices=gender_chioces)


class PreetyNum(models.Model):
    """靓号表"""
    mobile = models.CharField(verbose_name="手机号", max_length=32)
    # 想要允许为空  null= true   blank= true
    price = models.IntegerField(verbose_name="价格")
    level_choices = (
        (1, "1级"),
        (2, "4级"),
        (3, "3级"),
        (4, "4级"),
    )
    level = models.SmallIntegerField(verbose_name="级别", choices=level_choices, default=1)
    status_choices = (
        (1, "已使用"),
        (2, "未使用"),
    )
    status = models.SmallIntegerField(verbose_name="状态", choices=status_choices, default=2)

    class Meta:
        db_table = "phoneNumber"


class Admin(models.Model):
    user_name = models.CharField(verbose_name="管理员", max_length=32)
    password = models.CharField(verbose_name="密码", max_length=64)

    def __str__(self):
        return self.user_name


class Task(models.Model):
    """任务"""
    level_choices = (
        (1, "紧急"),
        (2, "重要"),
        (3, "临时"),
    )

    level = models.SmallIntegerField(verbose_name="级别", choices=level_choices, default=1)
    title = models.CharField(max_length=63, verbose_name="标题")
    detail = models.TextField(verbose_name="详细信息")
    user = models.ForeignKey(verbose_name="负责人", to="Admin", on_delete=models.CASCADE)


class Order(models.Model):
    oid = models.CharField(max_length=64, verbose_name="订单号", blank=False, null=False)
    title = models.CharField(max_length=32, verbose_name="名称")
    price = models.FloatField(verbose_name="价格")

    status_choices = (
        (1, "待支付"),
        (2, "已支付"),
    )
    status = models.SmallIntegerField(verbose_name="状态", choices=status_choices, default=1)
    admin = models.ForeignKey(verbose_name="管理员", to="Admin", on_delete=models.CASCADE)
