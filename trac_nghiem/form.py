#coding: utf-8
__author__ = 'ThanhNT'

from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from models import UserProfile
from django.contrib.admin.widgets import AdminDateWidget

class UserForm(forms.ModelForm):
    error_messages = {
        'duplicate_username': ("A user with that username already exists."),
        'password_mismatch': ("The two password fields didn't match."),
    }
    username = forms.RegexField(label=("Username"), max_length=30,
    regex=r'^[\w.@+-]+$',
    help_text=("Tên đăng nhập không được chứa các ký tự đặc biệt"),
    error_messages={
        'invalid':("Chỉ chấp nhận chữ cái, số và các ký tự "
                     "@/./+/-/_")},
    widget=forms.TextInput(attrs={'placeholder': 'Tên tài khoản'}))
    password1 = forms.CharField(label=("Mật khẩu"),
        widget=forms.PasswordInput, max_length=4096)
    password2 = forms.CharField(label=("Nhập lại mật khẩu"),
        widget=forms.PasswordInput,
        max_length=4096,
        help_text=("Nhập lại mật khẩu đã nhập ở bên trên"))

    email = forms.EmailField()
    class Meta:
        model = User
        fields = ('username','email','password1','password2')
    def clean_username(self):
    # Since User.username is unique, this check is redundant,
    # but it sets a nicer error message than the ORM. See #13147.
        username = self.cleaned_data["username"]
        try:
            User._default_manager.get(username=username)
        except User.DoesNotExist:
            return username
        raise forms.ValidationError(self.error_messages['duplicate_username'])

    def clean_password2(self):
        password1 = self.cleaned_data.get("password1")
        password2 = self.cleaned_data.get("password2")
        if password1 and password2 and password1 != password2:
            raise forms.ValidationError(
                self.error_messages['password_mismatch'])
        return password2

    def save(self, commit=True):
        user = super(UserForm, self).save(commit=False)
        user.set_password(self.cleaned_data["password1"])
        if commit:
            user.save()
        return user

class UserProfileForm(forms.ModelForm):
    birthday = forms.DateField(label="Ngày sinh",
        widget=forms.TextInput(attrs={'placeholder': 'tháng / ngày / năm'})
    )
    c = (
        ('Nam','Nam'),
        (('Nữ').decode('utf8'),('Nữ').decode('utf8')),      #cân chỉ rõ cách mã hóa ký tự unicode khi lưu vào cơ sở dữ liệu
        (('Khác').decode('utf8'),('Khác').decode('utf8'))
    )
    sex = forms.ChoiceField(label="Giới tính", choices=c)
    name = forms.CharField(max_length=100,
        widget=forms.TextInput(attrs={'placeholder': 'Tên của bạn'})
    )
    class Meta:
        model = UserProfile
        fields = ('name','sex','birthday')