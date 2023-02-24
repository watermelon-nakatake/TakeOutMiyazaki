from django.http import HttpResponse
from django.shortcuts import get_object_or_404, get_list_or_404, render, redirect, resolve_url
from .models import RestaurantImage, MenuImage, Restaurant, RestaurantMenu, Genre, CityName, CityArea
from django.contrib.auth.decorators import login_required
from django.contrib.auth.base_user import AbstractBaseUser
from django.contrib.auth import get_user_model
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.views import generic
from register.forms import UserCreateForm
from .forms import RestaurantEditForm, RestaurantCreateForm, UserEditForm, RestaurantImageForm, MenuCreateForm, \
    MenuEditForm, MenuCreateForm2, RestaurantImageUploadForm
from django import forms
from django.urls import reverse, reverse_lazy
from django.db.models import Max
from PIL import Image
import os
import io
from django.core.files.uploadedfile import InMemoryUploadedFile

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


def restaurant_detail(request, restaurant_pk):
    """
    検索結果からの店の情報ページを表示
    """
    this_restaurant = get_object_or_404(Restaurant, pk=restaurant_pk)
    # menu_list = get_list_or_404(RestaurantMenu, sub_restaurant=this_restaurant)
    # view_menu_list = [{'name_text': menu.menu_name_text, 'price': menu.menu_price,
    # 'comment_text': menu.menu_comment_text,
    # 'images': MenuImage.objects.filter(sub_menu=menu)} for menu in menu_list]
    # restaurant_images = get_list_or_404(RestaurantImage, sub_restaurant=this_restaurant)
    return render(request, 'info_edit/detail.html',
                  {'this_restaurant': this_restaurant, 'images': this_restaurant.RestaurantImage})
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
    restaurant_images = this_restaurant.RestaurantImage
    context = {'user': user, 'restaurant': this_restaurant, 'menu_list': this_menu_list,
               'r_images': restaurant_images}
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


# チェック済み
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


# チェック済み
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


# 以下クラスビューで実装
# 店舗基本情報のCRUD
class RestaurantCreateView(LoginRequiredMixin, generic.CreateView):
    model = Restaurant
    fields = ('restaurant_name_text', 'restaurant_address', 'restaurant_city', 'restaurant_genre',
              'restaurant_comment')
    template_name = 'info_edit/restaurant_create_c.html'

    def form_valid(self, form):
        this_restaurant = form.save(commit=False)
        this_restaurant.user = self.request.user
        this_restaurant.save()
        return super().form_valid(form)

    def get_success_url(self):
        return reverse('info_edit:restaurant_detail', kwargs={'pk': self.kwargs['pk']})


class RestaurantDetailView(LoginRequiredMixin, generic.DetailView):
    model = Restaurant
    context_object_name = 'restaurant_detail'
    template_name = 'info_edit/restaurant_detail_c.html'


class RestaurantUpdateView(LoginRequiredMixin, generic.UpdateView):
    model = Restaurant
    context_object_name = 'restaurant_detail'
    fields = ('restaurant_name_text', 'restaurant_address', 'restaurant_city', 'restaurant_genre',
              'restaurant_comment')
    template_name = 'info_edit/restaurant_update_c.html'


class RestaurantDeleteView(LoginRequiredMixin, generic.DeleteView):
    model = Restaurant
    template_name = 'info_edit/delete.html'


# メニュー情報のCRUD
class MenuCreateView(LoginRequiredMixin, generic.CreateView):
    fields = ('menu_name_text', 'menu_comment_text', 'menu_price')
    model = RestaurantMenu
    template_name = 'info_edit/menu_create_c.html'
    login_url = reverse_lazy('info_edit:user_detail')
    context_object_name = 'this_menu'

    def get_context_data(self, **kwargs):
        this_pk = self.kwargs.get('r_pk')
        context = super().get_context_data(**kwargs)
        context['this_restaurant'] = Restaurant.objects.get(pk=this_pk)
        return context

    def form_valid(self, form):
        this_menu = form.save(commit=False)
        this_menu.sub_restaurant = Restaurant.objects.get(user=self.request.user)
        this_menu.save()
        return super().form_valid(form)

    def get_success_url(self):
        return reverse('info_edit:restaurant_detail', kwargs={'pk': self.kwargs['r_pk']})


class MenuDetailView(LoginRequiredMixin, generic.DetailView):
    model = RestaurantMenu
    context_object_name = 'menu_detail'
    template_name = 'info_edit/menu_detail_c.html'


class MenuUpdateView(LoginRequiredMixin, generic.UpdateView):
    fields = ('menu_name_text', 'menu_comment_text', 'menu_price')
    model = RestaurantMenu
    template_name = 'info_edit/menu_update_c.html'
    login_url = reverse_lazy('info_edit:user_detail')

    def get_context_data(self, **kwargs):
        this_pk = self.kwargs.get('pk')
        context = super().get_context_data(**kwargs)
        context['this_menu'] = RestaurantMenu.objects.get(pk=this_pk)
        return context


class MenuDeleteView(LoginRequiredMixin, generic.DeleteView):
    model = Restaurant
    template_name = 'info_edit/delete.html'


class ResizeImageUploadView(generic.CreateView):

    def get_success_url(self):
        return reverse('info_edit:restaurant_detail_u',
                       kwargs={'pk': Restaurant.objects.get(user=self.request.user).pk})

    def add_form_pk_data(self, post_data):
        return post_data

    def form_valid(self, form):
        save_path = "up_images/temporary/" + str(self.request.FILES['image'])
        up_data = self.request.FILES['image']
        with open(save_path, 'wb+') as i:
            for chunk in up_data.chunks():
                i.write(chunk)
        # サイズ調整
        img = Image.open(save_path)
        if img.size[0] / 4 * 3 >= img.size[1]:
            re_img = img.resize((640, int(640 * img.size[1] / img.size[0])))
        else:
            re_img = img.resize((int(480 * img.size[0] / img.size[1]), 480))
        # I/Oデータ取り出し
        img_io = io.BytesIO()
        re_img.save(img_io, format="JPEG")
        io_image = InMemoryUploadedFile(img_io, field_name=None, name=save_path, charset=None,
                                        content_type="image/jpeg", size=img_io.getbuffer().nbytes)
        post = form.save(commit=False)
        post.image = io_image
        post = self.add_form_pk_data(post)
        post.save()
        os.remove(save_path)
        return super().form_valid(form)


class RestaurantImageUploadView(LoginRequiredMixin, ResizeImageUploadView):
    model = RestaurantImage
    template_name = 'info_edit/restaurant_image_upload.html'
    # form_class = RestaurantImageUploadForm
    fields = ('title', 'image')

    def add_form_pk_data(self, post_data):
        post_data.sub_restaurant = Restaurant.objects.get(user=self.request.user)
        return post_data


class MenuImageUploadView(LoginRequiredMixin, ResizeImageUploadView):
    model = MenuImage
    template_name = 'info_edit/menu_image_upload.html'
    fields = ('title', 'image')

    def add_form_pk_data(self, post_data):
        post_data.sub_menu = RestaurantMenu.objects.get(pk=self.kwargs['menu_pk'])
        return post_data


class RestaurantImageDeleteView(LoginRequiredMixin, generic.DetailView):
    model = RestaurantImage
    template_name = 'info_edit/restaurant_img_delete.html'


class MenuImageDeleteView(LoginRequiredMixin, generic.DetailView):
    model = MenuImage
    template_name = 'info_edit/menu_img_delete.html'


class ExRestaurantListView(generic.ListView):
    model = Restaurant
    context_object_name = 'restaurant_list'
    template_name = 'info_edit/Ex_restaurant_list.html'


class ExRestaurantDetailView(generic.DetailView):
    model = Restaurant
    context_object_name = 'restaurant_data'
    template_name = 'info_edit/Ex_restaurant_detail.html'


class ExMenuDetailView(generic.DetailView):
    model = RestaurantMenu
    context_object_name = 'menu_data'
    template_name = 'info_edit/Ex_menu_detail.html'


# todo: UserPassesTestMixinクラスでやってみる
