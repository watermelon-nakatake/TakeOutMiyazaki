from django.http import HttpResponse
from django.shortcuts import get_object_or_404, get_list_or_404, render
from .models import RestaurantImage, MenuImage, Restaurant, RestaurantMenu, Genre, CityName, CityArea
from .forms import MakeRestaurantMain
from django.contrib.auth.decorators import login_required
from django.contrib.auth.base_user import AbstractBaseUser
from django.conf import settings
from django.contrib.auth import get_user_model
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.contrib.auth.views import LoginView, LogoutView
from django.contrib.sites.shortcuts import get_current_site
from django.core.signing import BadSignature, SignatureExpired, loads, dumps
from django.shortcuts import redirect, resolve_url
from django.template.loader import render_to_string
from django.views import generic
from register.forms import LoginForm, UserCreateForm
from .forms import RestaurantEditForm, RestaurantCreateForm, UserEditForm, RestaurantImageForm
from django import forms

User = get_user_model()


class OnlyYouMixin(UserPassesTestMixin):
    raise_exception = True

    def test_func(self):
        user = self.request.user
        return user.pk == self.kwargs['pk'] or user.is_superuser


class Top(generic.TemplateView):
    template_name = 'info_edit/top.html'


class UserDetail(OnlyYouMixin, generic.DetailView, generic.edit.ModelFormMixin):
    model = User
    template_name = 'info_edit/user_detail.html'
    fields = '__all__'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context.update({
            'restaurant': Restaurant.objects.get(user=self.object),
        })
        return context


class UserCreate(generic.CreateView):
    model = Restaurant
    form_class = UserCreateForm
    template_name = 'info_edit/user_create.html'
    success_url = '/user/top/'


class UserUpdate(OnlyYouMixin, generic.UpdateView):
    model = Restaurant
    form_class = RestaurantEditForm
    template_name = 'info_edit/user_form.html'

    def get_success_url(self):
        return resolve_url('info_edit:user_detail', pk=self.kwargs['pk'])


def index(request):
    """
    インデックスページ(Topページ)を表示
    """
    if AbstractBaseUser.is_authenticated:
        user = AbstractBaseUser
        restaurant_id = Restaurant.objects
    else:
        user = None
        restaurant_id = None
    return render(request, 'info_edit/top.html', {'user': user, 'restaurant_id': restaurant_id})


def menu_detail(request, menu_id):
    """
    メニューページを表示
    """
    return HttpResponse("You're looking at question %s." % menu_id)


def restaurant_detail(request, restaurant_id):
    """
    検索結果からの店の情報ページを表示
    """
    this_restaurant = get_object_or_404(Restaurant, pk=restaurant_id)
    # menu_list = get_list_or_404(RestaurantMenu, sub_restaurant=this_restaurant)
    # view_menu_list = [{'name_text': menu.menu_name_text, 'price': menu.menu_price,
    # 'comment_text': menu.menu_comment_text,
    # 'images': MenuImage.objects.filter(sub_menu=menu)} for menu in menu_list]
    restaurant_images = get_list_or_404(RestaurantImage, sub_restaurant=this_restaurant)
    return render(request, 'info_edit/detail.html', {'this_restaurant': this_restaurant, 'image_list': restaurant_images})
    # 'menu_list': view_menu_list}


@login_required
def user_detail(request):
    """
    検索結果からの店の情報ページを表示
    """
    user = request.user
    this_restaurant = get_object_or_404(Restaurant, user=user)
    # restaurant_images = get_list_or_404(RestaurantImage, sub_restaurant=this_restaurant)
    context = {'user': user, 'restaurant': this_restaurant}
    return render(request, 'info_edit/user_detail.html', context)


@login_required
def restaurant_create(request):
    user_form = UserEditForm(request.POST or None, instance=request.user)
    restaurant_form = RestaurantCreateForm(request.POST or None)
    if request.method == 'POST' and user_form.is_valid() and restaurant_form.is_valid():
        user = user_form.save(commit=False)
        user.is_active = True
        user.save()

        restaurant = restaurant_form.save(commit=False)
        restaurant.user = user
        restaurant.save()
        restaurant_form.save_m2m()
        return redirect('info_edit:user_detail')

    context = {'user_form': user_form, 'restaurant_form': restaurant_form}
    return render(request, 'info_edit/restaurant_create.html', context)


@login_required
def restaurant_edit(request):
    user_form = UserEditForm(request.POST or None, instance=request.user)
    this_restaurant = Restaurant.objects.get(user=request.user)
    restaurant_form = RestaurantEditForm(request.POST or None, instance=this_restaurant)
    if request.method == 'POST' and user_form.is_valid() and restaurant_form.is_valid():
        user = user_form.save(commit=False)
        user.is_active = True
        user.save()

        restaurant = restaurant_form.save(commit=False)
        restaurant.user = user
        restaurant.save()
        restaurant_form.save_m2m()
        return redirect('info_edit:user_detail')

    context = {'user_form': user_form, 'restaurant_form': restaurant_form}
    return render(request, 'info_edit/restaurant_edit.html', context)


@login_required
def restaurant_image_upload(request):
    this_restaurant = Restaurant.objects.get(user=request.user)
    if request.method == "POST":
        form = RestaurantImageForm(request.POST, request.FILES)
        if form.is_valid():
            form.sub_restaurant = this_restaurant
            form.save()
            return redirect('info_edit:user_detail')
    else:
        form = RestaurantImageForm()

    context = {'form': form, 'restaurant': this_restaurant}
    return render(request, 'info_edit/user_image_upload.html', context)
