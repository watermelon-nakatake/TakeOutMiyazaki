from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as AuthUserAdmin
from django.contrib.auth.forms import UserChangeForm, UserCreationForm
from .models import User
from .models import Restaurant, RestaurantMenu, CityName, CityArea, Genre, RestaurantImage, MenuImage


class MyUserChangeForm(UserChangeForm):
    class Meta:
        model = User
        fields = '__all__'


class MyUserCreationForm(UserCreationForm):
    class Meta:
        model = User
        fields = ('email',)


class MyUserAdmin(AuthUserAdmin):
    fieldsets = (
        (None, {'fields': ('email', 'password')}),
        ('Personal info', {'fields': ('first_name', 'last_name',)}),
        ('Permissions', {'fields': ('is_active', 'is_staff', 'is_superuser',
                                       'groups', 'user_permissions')}),
        ('Important dates', {'fields': ('last_login', 'date_joined')}),
    )
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('email', 'password1', 'password2'),
        }),
    )
    form = MyUserChangeForm
    add_form = MyUserCreationForm
    list_display = ('email', 'first_name', 'last_name', 'is_staff')
    list_filter = ('is_staff', 'is_superuser', 'is_active', 'groups')
    search_fields = ('email', 'first_name', 'last_name')
    ordering = ('email',)


class RestaurantInline(admin.StackedInline):
    model = Restaurant
    max_num = 1
    can_delete = False


class UserAdmin(AuthUserAdmin):
    inlines = [RestaurantInline]


admin.site.register(User, MyUserAdmin)
admin.site.register(Restaurant)
admin.site.register(RestaurantMenu)
admin.site.register(CityName)
admin.site.register(CityArea)
admin.site.register(Genre)
admin.site.register(RestaurantImage)
admin.site.register(MenuImage)
