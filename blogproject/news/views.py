from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import HttpResponseForbidden
from .models import Articles
from .forms import ArticlesForm
from django.views.generic import DetailView, UpdateView, DeleteView

def editor_required(view_func):
    @login_required
    def wrapper(request, *args, **kwargs):
        if hasattr(request.user, 'profile') and request.user.profile.role == 'editor':
            return view_func(request, *args, **kwargs)
        return HttpResponseForbidden("У вас нет прав редактора для выполнения этого действия.")
    return wrapper

class NewsDetailView(DetailView):
    model = Articles
    template_name = 'news/details_view.html'
    context_object_name = 'article'

class NewsDeleteView(LoginRequiredMixin, DeleteView):
    model = Articles
    template_name = 'news/delete.html'
    success_url = '/news/'

    def dispatch(self, request, *args, **kwargs):
        if not hasattr(request.user, 'profile') or request.user.profile.role != 'editor':
            return HttpResponseForbidden("У вас нет прав редактора для удаления статьи.")
        return super().dispatch(request, *args, **kwargs)

class NewsUpdateView(LoginRequiredMixin, UpdateView):
    model = Articles
    template_name = 'news/update.html'
    form_class = ArticlesForm

    def dispatch(self, request, *args, **kwargs):
        if not hasattr(request.user, 'profile') or request.user.profile.role != 'editor':
            return HttpResponseForbidden("У вас нет прав редактора для редактирования статьи.")
        return super().dispatch(request, *args, **kwargs)

@editor_required
def create(request):
    error = ''
    if request.method == 'POST':
        form = ArticlesForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('home')
        else:
            error = 'Форма заполнения была неверной'

    form = ArticlesForm()
    data = {
        'form': form,
        'error': error
    }
    return render(request, 'news/create.html', data)

def news_home(request):
    news = Articles.objects.order_by('-date')[:3]
    return render(request, 'news/news_home.html', {'news': news})