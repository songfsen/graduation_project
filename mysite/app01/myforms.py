from django import forms


class MerchantForm(forms.Form):
    """商户注册表单"""
    shop_name = forms.CharField(label="店铺名称", max_length=128,
                                widget=forms.TextInput(attrs={'class': 'form-control'}))

    location = forms.CharField(label="店铺位置", max_length=128,
                               widget=forms.TextInput(attrs={'class': 'form-control'}))

    email = forms.EmailField(label='联系邮箱', widget=forms.EmailInput(attrs={'class': 'form-control'}))

    phone = forms.CharField(label="手机号", max_length=128,
                            widget=forms.TextInput(attrs={'class': 'form-control'}))


class MerchantCheck(forms.Form):
    """登录验证码表单"""
    check_code = forms.CharField(label="验证码", max_length=32,
                                 widget=forms.TextInput(attrs={'class': 'form-control'}))


class MerchantEmail(forms.Form):
    """登录邮箱表单"""
    email = forms.CharField(label="邮箱地址", max_length=32,
                            widget=forms.TextInput(attrs={'class': 'form-control'}))


