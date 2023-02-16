from .models import Restaurant, CityName, RestaurantImage
from django import forms
from django.contrib.auth.forms import UserChangeForm
from register.models import User


class MakeRestaurantMain(forms.ModelForm):
    parent_category = forms.ModelChoiceField(label='city_name', queryset=CityName.objects, required=False)

    class Meta:
        model = Restaurant
        fields = '__all__'

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields.values():
            field.widget['class'] = 'form-control'


class RestaurantEditForm(forms.ModelForm):
    """ユーザー情報更新フォーム"""

    class Meta:
        model = Restaurant
        exclude = ('user', 'pub_date', 'mod_date', 'image_num')
        widgets = {
            'city_area': forms.CheckboxSelectMultiple,
            'restaurant_genre': forms.CheckboxSelectMultiple
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields.values():
            field.widget.attrs['class'] = 'form-control'


class RestaurantCreateForm(forms.ModelForm):
    """レストラン情報新規作成フォーム"""

    class Meta:
        model = Restaurant
        exclude = ('user', 'pub_date', 'mod_date', 'image_num')
        widgets = {
            'city_area': forms.CheckboxSelectMultiple,
            'restaurant_genre': forms.CheckboxSelectMultiple
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields.values():
            field.widget.attrs['class'] = 'form-control'


class UserEditForm(UserChangeForm):
    password = None
    """レストラン情報ページ用ユーザーフォーム"""
    class Meta:
        model = User
        fields = ('last_name', 'first_name')


class RestaurantImageForm(forms.ModelForm):
    class Meta:
        model = RestaurantImage
        fields = ['image', 'title']
