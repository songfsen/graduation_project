from django import forms
from captcha.fields import CaptchaField


# 方便自动校验
class UserForm(forms.Form):
    """登录表单"""
    username = forms.CharField(label="用户名", max_length=128,
                               widget=forms.TextInput(attrs={'class': 'form-control'}))

    password = forms.CharField(label="密码", max_length=256,
                               widget=forms.PasswordInput(attrs={'class': 'form-control'}))

    captcha = CaptchaField(label='验证码')


class RegisterForm(forms.Form):
    """注册表单"""
    gender = (
        ('male', "男"),
        ('female', "女"),
    )
    username = forms.CharField(label="用户名", max_length=128,
                               widget=forms.TextInput(attrs={'class': 'form-control'}))

    password1 = forms.CharField(label="密码", max_length=256,
                                widget=forms.PasswordInput(attrs={'class': 'form-control'}))

    password2 = forms.CharField(label="确认密码", max_length=256,
                                widget=forms.PasswordInput(attrs={'class': 'form-control'}))

    email = forms.EmailField(label="邮箱",
                             widget=forms.EmailInput(attrs={'class': 'form-control'}))

    sex = forms.ChoiceField(label='性别', choices=gender)

    captcha = CaptchaField(label='验证码')


class ForgetPwdForm(forms.Form):
    """ 填写邮箱地址表单 """
    email = forms.EmailField(label="请填写您的注册邮箱",
                             widget=forms.EmailInput(attrs={'class': 'form-control'}))


class ResetPwdForm(forms.Form):
    """密码重置表单"""
    check_code = forms.CharField(max_length=6, label='验证码', widget=forms.TextInput(attrs={'class': 'form-control'}))

    new_pwd = forms.CharField(label="重置密码", max_length=256,
                              widget=forms.PasswordInput(attrs={'class': 'form-control'}))

    confirm_pwd = forms.CharField(label="再次确认密码", max_length=256,
                                  widget=forms.PasswordInput(attrs={'class': 'form-control'}))
