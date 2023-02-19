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
from .forms import RestaurantEditForm, RestaurantCreateForm, UserEditForm, RestaurantImageForm, MenuCreateForm, \
    MenuEditForm, MenuCreateForm2
from django import forms
from django.urls import reverse, reverse_lazy
from django.db.models import Max

User = get_user_model()


class Search(generic.TemplateView):
    template_name = 'info_edit/top.html'


class UserDetail(LoginRequiredMixin, generic.DetailView, generic.edit.ModelFormMixin):
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


class UserUpdate(LoginRequiredMixin, generic.UpdateView):
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
    if Restaurant.objects.get(user=request.user):
        this_restaurant = get_object_or_404(Restaurant, pk=restaurant_id)
    else:
        redirect('info_edit:user_create')
    # menu_list = get_list_or_404(RestaurantMenu, sub_restaurant=this_restaurant)
    # view_menu_list = [{'name_text': menu.menu_name_text, 'price': menu.menu_price,
    # 'comment_text': menu.menu_comment_text,
    # 'images': MenuImage.objects.filter(sub_menu=menu)} for menu in menu_list]
    restaurant_images = get_list_or_404(RestaurantImage, sub_restaurant=this_restaurant)
    return render(request, 'info_edit/detail.html',
                  {'this_restaurant': this_restaurant, 'image_list': restaurant_images})
    # 'menu_list': view_menu_list}


# チェック済み
@login_required
def user_detail(request):
    """
    ログインしたユーザーが見る自分の店の情報ページ
    """
    user = request.user
    if not Restaurant.objects.get(user=user):
        redirect('info_edit:user_create')
    this_restaurant = get_object_or_404(Restaurant, user=user)
    this_menu_list = this_restaurant.Menu
    # restaurant_images = RestaurantImage.objects.get(sub_restaurant=this_restaurant)
    context = {'user': user, 'restaurant': this_restaurant, 'menu_list': this_menu_list}
    return render(request, 'info_edit/user_detail.html', context)


# チェック済み
@login_required
def restaurant_create(request):
    restaurant_form = RestaurantCreateForm(request.POST or None)
    if request.method == 'POST' and restaurant_form.is_valid():
        restaurant = restaurant_form.save(commit=False)
        restaurant.user = request.user
        restaurant.save()
        restaurant_form.save_m2m()
        return redirect('info_edit:user_detail')
    context = {'restaurant_form': restaurant_form}
    return render(request, 'info_edit/restaurant_create.html', context)


# チェック済み
@login_required
def restaurant_edit(request):
    user = request.user
    this_restaurant = Restaurant.objects.get(user=user)
    restaurant_form = RestaurantEditForm(request.POST or None, instance=this_restaurant)
    if request.method == 'POST' and restaurant_form.is_valid():
        restaurant = restaurant_form.save(commit=False)
        restaurant.user = user
        restaurant.save()
        restaurant_form.save_m2m()
        return redirect('info_edit:user_top')

    context = {'restaurant_form': restaurant_form}
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


@login_required
def menu_create(request):
    menu_form = MenuCreateForm(request.POST or None)
    this_restaurant = Restaurant.objects.get(user=request.user, )
    if request.method == 'POST' and menu_form.is_valid():
        menu = menu_form.save(commit=False)
        menu.is_active = True
        menu.sub_restaurant = this_restaurant
        menu.save()
        menu_form.save_m2m()

        this_restaurant.max_menu_id \
            = RestaurantMenu.objects.filter(sub_restaurant=this_restaurant).aggregate(Max('menu_id'))[
                  'menu_id__max'] + 1
        this_restaurant.save()
        return redirect('info_edit:user_detail')

    context = {'menu_form': menu_form}
    return render(request, 'info_edit/menu_create.html', context)


@login_required
def menu_edit(request, menu_pk):
    this_menu = RestaurantMenu.objects.get(pk=menu_pk)
    menu_form = MenuEditForm(request.POST or None, instance=this_menu)
    this_restaurant = RestaurantMenu.sub_restaurant
    if request.method == 'POST' and menu_form.is_valid():
        menu = menu_form.save(commit=False)
        menu.is_active = True
        menu.restaurant = this_restaurant
        menu.save()
        menu_form.save_m2m()
        return redirect('info_edit:user_detail')

    context = {'menu_form': menu_form}
    return render(request, 'info_edit/menu_edit.html', context)


# クラスビューのテスト

class RestaurantCreateView(LoginRequiredMixin, generic.CreateView):
    model = Restaurant
    fields = ('restaurant_name_text', 'restaurant_address', 'restaurant_city', 'restaurant_genre',
              'restaurant_comment')
    template_name = 'info_edit/restaurant_create_c.html'

    def get_form_kwargs(self):
        kwgs = super().get_form_kwargs()
        kwgs['user'] = self.request.user
        return kwgs

    def get_success_url(self):
        return reverse('info_edit:restaurant_detail', kwargs={'pk': self.object.pk})


class RestaurantDetailView(LoginRequiredMixin, generic.DetailView):
    model = Restaurant
    context_object_name = 'restaurant_detail'
    template_name = 'info_edit/restaurant_detail_c.html'


class MenuCreateView(LoginRequiredMixin, generic.CreateView):
    fields = ('menu_name_text', 'menu_comment_text', 'menu_price')
    model = RestaurantMenu
    template_name = 'info_edit/menu_create_c.html'
    login_url = 'user/top/'

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        ctx['this_restaurant'] = Restaurant.objects.get(user=self.request.user)

    def get_success_url(self):
        return reverse('info_edit:restaurant_detail', kwargs={'pk': self.object.pk})


class MenuUpdateView(LoginRequiredMixin, generic.UpdateView):
    fields = ('menu_name_text', 'menu_comment_text', 'menu_price')
    model = RestaurantMenu
    template_name = 'info_edit/menu_create_c.html'
    login_url = 'user/top/'
