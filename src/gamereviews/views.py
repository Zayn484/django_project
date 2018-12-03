from django.contrib.auth.decorators import login_required
from django.contrib.contenttypes.models import ContentType
from django.contrib.auth.mixins import LoginRequiredMixin
from django.db.models import Q
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.shortcuts import render
from django.http import HttpResponseRedirect
from django.core.urlresolvers import reverse
from django.core.exceptions import ValidationError
from django.shortcuts import render, render_to_response, get_object_or_404
from django.views import View
from django.views.generic import TemplateView, ListView, DetailView, CreateView, UpdateView, DeleteView
from django.db.models.signals import pre_save
from django.utils import timezone
from django.contrib.contenttypes.models import ContentType

from comments.forms import CommentForm
from comments.models import Comment
from .models import News, Reviews, Topgames, Slideshow, pre_save_reciever
from .forms import NewsCreateForm, ReviewsCreateForm, TopgamesCreateForm, SlideshowCreateForm
from .utils import unique_slug_generator


def search(request):
    try:
        q = request.GET['q']
        review_list = Reviews.objects.filter(title__icontains=q).order_by("-timestamp")
        if (Reviews.objects.filter(title__icontains=q)):
            total_reviews = range(len(review_list))
            for t in total_reviews:
                t = t+1
            return render_to_response('bootstrap/reviews.html', {'review_list':review_list,'results':t, 'q':q})
        else:
            return render_to_response('bootstrap/reviews.html', {'review_list':review_list, 'q':q})
    except KeyError:
        return render_to_response('bootstrap/reviews.html')


class IndexTemplateView(TemplateView):
    template_name = 'bootstrap/index.html'
    paginate_by = 12

    def get_context_data(self,*args, **kwargs):

        slideshow_query_set = Slideshow.objects.filter().order_by('-id')[:5]
        news_query_set = News.objects.filter().order_by('-id')[:4]
        reviews_query_set = Reviews.objects.filter().order_by('-id')
        topgames_query_set = Topgames.objects.filter().order_by('-id')[:10]
        paginator = Paginator(reviews_query_set, self.paginate_by)

        page = self.request.GET.get('page')
        try:
            file_exams = paginator.page(page)
        except PageNotAnInteger:
            file_exams = paginator.page(1)
        except EmptyPage:
            file_exams = paginator.page(paginator.num_pages)

        context = {
            "news_list" : news_query_set,
            "review_list" : file_exams,
            "topgames_list": topgames_query_set,
            "slideshow_list": slideshow_query_set,
            
        }
        return context


class NewsTemplateView(TemplateView):
    template_name = 'bootstrap/news.html'
    paginate_by = 10

    def get_context_data(self,*args, **kwargs):

        slideshow_query_set = Slideshow.objects.filter().order_by('-id')[:5]
        news_query_set = News.objects.filter().order_by('-id')[:10]
        topgames_query_set = Topgames.objects.filter().order_by('-id')[:10]
        paginator = Paginator(news_query_set, self.paginate_by)
        page = self.request.GET.get('page')

        try:
            file_exams = paginator.page(page)
        except PageNotAnInteger:
            file_exams = paginator.page(1)
        except EmptyPage:
            file_exams = paginator.page(paginator.num_pages)
        context = {
            "news_list" : file_exams,
            "topgames_list": topgames_query_set,
            "slideshow_list": slideshow_query_set
        }
        return context


# class NewsListView(ListView):
#     def get_queryset(self):
#         slug = self.page_kwarg.get("slug")
#         if slug:
#             queryset = News.objects.filter(
#                 Q(category__iexact=slug) |
#                 Q(category__icontains=slug)
#             )
#         else:
#             queryset = News.objects.all()
#         return queryset

class NewsCreateView(LoginRequiredMixin, CreateView):
    form_class = NewsCreateForm
    login_url = '/login/'
    template_name = 'bootstrap/postPanel/news_form.html'
    success_url = '/news/'

    def form_valid(self, form):
        instance = form.save(commit=False)
        instance.owner = self.request.user
        return super(NewsCreateView, self).form_valid(form)


class NewsUpdateView(LoginRequiredMixin, UpdateView):
    model = News
    form_class = NewsCreateForm
    template_name = 'bootstrap/postPanel/news_form.html'
    pre_save.connect(pre_save_reciever, sender=News.title)
    success_url = '/news/'


class NewsDeleteView(LoginRequiredMixin, DeleteView):
    model = News
    success_url = '/'


class ReviewTemplateView(TemplateView):
    template_name = 'bootstrap/reviews.html'
    paginate_by = 20

    def get_context_data(self,*args, **kwargs):

        news_query_set = News.objects.filter().order_by('-timestamp')[:4]
        reviews_query_set = Reviews.objects.filter().order_by('-timestamp')[:20]
        paginator = Paginator(reviews_query_set, self.paginate_by) 
        page = self.request.GET.get('page')
        try:
            file_exams = paginator.page(page)
        except PageNotAnInteger:
            file_exams = paginator.page(1)
        except EmptyPage:
            file_exams = paginator.page(paginator.num_pages)

        context = {
            "news_list" : news_query_set,
            "review_list" : file_exams
        }
        return context


class GameDetailView(UpdateView):
    form_class = CommentForm
    model = Reviews
    template_name = 'gamereviews/reviews_detail.html'

    def get_initial(self):
        initial_data = super(GameDetailView, self).get_initial()
        obj = self.get_object()
        content_type = ContentType.objects.get_for_model(Reviews)
        obj_id = obj.id
        initial_data.update({
            "content_type": content_type,
            "object_id": obj_id,
        })
        return initial_data

    def get_context_data(self, *args, **kwargs):
        context = super(GameDetailView, self).get_context_data(*args, **kwargs)
        obj = self.get_object()
        content_type = ContentType.objects.get_for_model(Reviews)
        obj_id = obj.id
        slug = obj.slug
        comments = Comment.objects.filter(content_type=content_type, object_id=obj_id)
        comments = comments.order_by("-timestamp")
        initial_data = {
            "content_type": content_type,
            "object_id": obj_id,
        }
        form = CommentForm(initial=initial_data)
        context = {
            "object": obj,
            "slug": slug,
            "comments": comments,
            "comment_form": form,
        }
        return context

    def form_valid(self, form):
        c_type = form.cleaned_data.get("content_type")
        content_type = ContentType.objects.get(model=c_type)
        obj_id = form.cleaned_data.get('object_id')
        content_data = form.cleaned_data.get("comment_content")
        new_comment, created = Comment.objects.get_or_create(
                        user = self.request.user,
                        content_type= content_type,
                        object_id = obj_id,
                        comment_content = content_data
                    )
        return super(GameDetailView, self).form_valid(form)

    def get_success_url(self):
        obj = self.get_object()
        slug = obj.slug
        return reverse('gamereview', kwargs={'slug': slug,})


class GameUpdateView(LoginRequiredMixin, UpdateView):
    model = Reviews
    form_class = ReviewsCreateForm
    template_name = 'bootstrap/postPanel/review_form.html'
    pre_save.connect(pre_save_reciever,sender=Reviews.title)
    
    def get_success_url(self):
        obj = self.get_object()
        slug = obj.slug
        return reverse('gamereview', kwargs={'slug': slug,})


class GameDeleteView(LoginRequiredMixin, DeleteView):
    model = Reviews
    success_url = '/'


class CommentDeleteView(LoginRequiredMixin, DeleteView):
    model = Comment
    success_url = '/'



class ReviewsCreateView(LoginRequiredMixin, CreateView):
    form_class = ReviewsCreateForm
    login_url = '/login/'
    template_name = 'bootstrap/postPanel/review_form.html'
    success_url = '/reviews/'

    def form_valid(self, form):
        instance = form.save(commit=False)
        instance.owner = self.request.user
        return super(ReviewsCreateView, self).form_valid(form)



class PcTemplateView(TemplateView):
    template_name = 'bootstrap/reviews.html'
    paginate_by = 20

    def get_context_data(self,*args, **kwargs):

        pc_query_set = Reviews.objects.filter(category__iexact='pc').order_by("-timestamp")
        news_query_set = News.objects.filter().order_by('-timestamp')[:4]
        paginator = Paginator(pc_query_set, self.paginate_by)  # Show 20 items per page
        page = self.request.GET.get('page')
        try:
            file_exams = paginator.page(page)
        except PageNotAnInteger:
            file_exams = paginator.page(1)
        except EmptyPage:
            file_exams = paginator.page(paginator.num_pages)

        context = {
            "review_list" : file_exams,
            "news_list" : news_query_set
        }
        return context


class AndroidTemplateView(TemplateView):
    template_name = 'bootstrap/reviews.html'
    paginate_by = 20

    def get_context_data(self,*args, **kwargs):

        android_query_set = Reviews.objects.filter(category__iexact='android').order_by("-timestamp")
        news_query_set = News.objects.filter().order_by('-timestamp')[:4]
        paginator = Paginator(android_query_set, self.paginate_by)  # Show 25 contacts per page
        page = self.request.GET.get('page')
        try:
            file_exams = paginator.page(page)
        except PageNotAnInteger:
            file_exams = paginator.page(1)
        except EmptyPage:
            file_exams = paginator.page(paginator.num_pages)

        context = {
            "review_list" : file_exams,
            "news_list" : news_query_set
        }
        return context


class TopgamesListView(ListView):
    queryset = Topgames.objects.order_by("-timestamp")[:30]
    template_name = 'bootstrap/topgames.html'


class TopgamesCreateView(LoginRequiredMixin, CreateView):
    form_class = TopgamesCreateForm
    login_url = '/login/'
    template_name = 'bootstrap/postPanel/topgames_form.html'
    success_url = '/topgames/'

    def form_valid(self, form):
        instance = form.save(commit=False)
        instance.owner = self.request.user
        return super(TopgamesCreateView,self).form_valid(form)


class TopgamesUpdateView(LoginRequiredMixin, UpdateView):
    model = Topgames
    form_class = TopgamesCreateForm
    template_name = 'bootstrap/postPanel/topgames_form.html'
    pre_save.connect(pre_save_reciever, sender=Topgames.title)
    success_url = '/topgames/'


class TopgamesDeleteView(LoginRequiredMixin, DeleteView):
    model = Topgames
    success_url = '/topgames/'


class SlideshowCreateView(LoginRequiredMixin, CreateView):
    form_class = SlideshowCreateForm
    login_url = '/login/'
    template_name = 'slideshow/form.html'
    success_url = '/'

    def form_valid(self, form):
        instance = form.save(commit=False)
        instance.owner = self.request.user
        return super(SlideshowCreateView,self).form_valid(form)
