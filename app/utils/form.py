from django import forms
from django.core.exceptions import ValidationError

from app.models import *
from app.utils import encrypt
from .bootstrap import BootstrapModelForm


class MobileModelForm(BootstrapModelForm):
    class Meta:
        model = PreetyNum
        fields = "__all__"

    # def __init__(self, *args, **kwargs):
    #     super().__init__(*args, **kwargs)
    #     for name, filed in self.fields.items():
    #         # print(name, filed)
    #         filed.widget.attrs = {"class": "form-control"}


class UserInfoModelForm(BootstrapModelForm):
    class Meta:
        model = UserInfo
        fields = "__all__"

    # def __init__(self, *args, **kwargs):
    #     super().__init__(*args, **kwargs)
    #     for name, filed in self.fields.items():
    #         # print(name, filed)
    #         filed.widget.attrs = {"class": "form-control"}


class AdminModelForm(BootstrapModelForm):
    confirm_pwd = forms.CharField(label="确认密码",
                                  widget=forms.PasswordInput(render_value=True))
    password = forms.CharField(label='密码', widget=forms.PasswordInput(render_value=True))

    class Meta:
        model = Admin
        fields = "__all__"
        widgets = {
            "password": forms.PasswordInput
        }

    def clean_confirm_pwd(self):
        confirm_pwd = encrypt.md5(self.cleaned_data.get('confirm_pwd'))
        pwd = self.cleaned_data.get('password')
        if pwd != confirm_pwd:
            raise ValidationError("密码不一致！")
        return confirm_pwd

    def clean_password(self):
        pwd = self.cleaned_data.get('password')
        # print(type(pwd))
        return encrypt.md5(pwd)


class AdminResetModelForm(BootstrapModelForm):
    confirm_pwd = forms.CharField(
        label="确认密码",
        widget=forms.PasswordInput(render_value=True)
    )
    password = forms.CharField(label='密码', widget=forms.PasswordInput(render_value=True))

    class Meta:
        model = Admin
        fields = ['password', 'confirm_pwd']

    # def clean_confirm_pwd(self):
    def clean_confirm_pwd(self):
        confirm_pwd = encrypt.md5(self.cleaned_data.get('confirm_pwd'))
        pwd = self.cleaned_data.get('password')
        print(pwd != confirm_pwd)
        if pwd != confirm_pwd:
            raise ValidationError("密码不一致！")
        return confirm_pwd

    def clean_password(self):
        pwd = self.cleaned_data.get('password')
        # print(type(pwd))
        pwd = encrypt.md5(pwd)
        exists = Admin.objects.filter(id=self.instance.pk, password=pwd).exists()
        if exists:
            raise ValidationError('密码不能与之前的一致！')
        return pwd


class LoginForm(forms.Form):
    user_name = forms.CharField(
        label="用户名",
        widget=forms.TextInput,
        required=True
    )
    password = forms.CharField(
        label="密码",
        widget=forms.PasswordInput(render_value=True),
        required=True
    )

    code = forms.CharField(
        label="验证码",
        widget=forms.TextInput,
        required=True
    )

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for name, field in self.fields.items():
            if field.widget.attrs:
                field.widget.attrs["class"] = "form-control"
                field.widget.attrs["placeholder"] = field.label
            else:
                # print(self.fields.items())
                field.widget.attrs = {"class": "form-control",
                                      "placeholder": field.label}

    def clean_password(self):
        pwd = self.cleaned_data.get("password")
        pwd = encrypt.md5(pwd)
        return pwd
