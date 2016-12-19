import logging

from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from django.shortcuts import render, redirect, get_object_or_404
from django.views.generic import FormView

from main.forms import PostForm
from main.models import Post

DEFAULT_PAGE_SIZE = 10

logger = logging.getLogger('everpost.custom')


class RegisterFormView(FormView):
    form_class = UserCreationForm

    # Ссылка, на которую будет перенаправляться пользователь в случае успешной регистрации.
    # В данном случае указана ссылка на страницу входа для зарегистрированных пользователей.
    success_url = "/login/"

    # Шаблон, который будет использоваться при отображении представления.
    template_name = "register.html"

    def form_valid(self, form):
        # Создаём пользователя, если данные в форму были введены корректно.
        form.save()

        # Вызываем метод базового класса
        return super(RegisterFormView, self).form_valid(form)


def get_recent_posts(request):
    page = request.GET.get('page', 0)
    posts = Post.objects.order_by('-created_at')[page * DEFAULT_PAGE_SIZE:(page + 1) * DEFAULT_PAGE_SIZE]
    return render(request, 'recent_posts.html', {'posts': posts})


@login_required(login_url='/login/')
def get_user_posts(request, pk):
    user = get_object_or_404(User, pk=pk)
    page = request.GET.get('page', 0)
    posts = Post.objects.filter(author=user).order_by('-created_at')[
            page * DEFAULT_PAGE_SIZE:(page + 1) * DEFAULT_PAGE_SIZE]
    return render(request, 'user_posts.html', {'posts': posts, 'target_user': user})


@login_required(login_url='/login/')
def add_post(request):
    if request.method == 'POST':
        form = PostForm(request.POST)
        if form.is_valid():
            post_item = form.save()
            return redirect('post_view', pk=post_item.pk)
    else:
        form = PostForm(instance=Post())
    return render(request, 'post_edit.html', {'form': form, 'action': 'add'})


@login_required(login_url='/login/')
def edit_post(request, pk):
    post_item = get_object_or_404(Post, pk=pk)
    if post_item.author != request.user:
        raise ValidationError(
            'You are not the owner of the post',
            code='error.not.post.owner',
        )
    if request.method == 'POST':
        post_form = PostForm(request.POST)
        if post_form.is_valid():
            post_item.save()
            return redirect('post_view', pk=post_item.pk)
    else:
        post_form = PostForm(instance=post_item)
    return render(request, 'post_edit.html', {'post': post_form, 'action': 'edit'})


@login_required(login_url='/login/')
def delete_post(request, pk):
    post_item = get_object_or_404(Post, pk=pk)
    if post_item.author != request.user:
        raise ValidationError(
            'You are not the owner of the post',
            code='error.not.post.owner',
        )
    if request.method == "POST":
        post_item.delete()
        return redirect('my_posts')
    return render(request, 'post_delete.html', {'post': PostForm(instance=post_item)})


def view_post(request, pk):
    post_item = get_object_or_404(Post, pk=pk)
    return render(request, 'post_view.html', {'post': PostForm(instance=post_item)})
