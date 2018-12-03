"""gamingispassion URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.11/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf.urls import url, include
from django.contrib import admin
from django.conf import settings
from django.conf.urls.static import static
from django.views.generic import TemplateView

from django.contrib.auth.views import LoginView, LogoutView

from gamereviews.views import (
        IndexTemplateView,
        NewsTemplateView,
        NewsCreateView,
        NewsUpdateView,
        NewsDeleteView,
        ReviewTemplateView,
        PcTemplateView,
        AndroidTemplateView,
        GameDetailView,
        GameUpdateView,
        GameDeleteView,
        ReviewsCreateView,
        TopgamesCreateView,
        TopgamesListView,
        TopgamesUpdateView,
        TopgamesDeleteView,
        search,
        SlideshowCreateView,
        CommentDeleteView
)

from login.views import (
        UserFormView

)

urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url(r'^$', IndexTemplateView.as_view(), name='home'),
    url(r'^bootstrap/$', TemplateView.as_view(template_name='bootstrap/example.html')),
    url(r'^search/$', search, name='search'),
    url(r'^login/$', LoginView.as_view(), name='login'),
    url(r'^logout/$', LogoutView.as_view(), name='logout'),
    url(r'^register/$', UserFormView.as_view(), name='register'),
    url(r'^news/$', NewsTemplateView.as_view(), name='news'),
    url(r'^slideshow/create/$', SlideshowCreateView.as_view(), name='slideshow-create'),
    url(r'^news/create/$', NewsCreateView.as_view(), name='news-create'),
    url(r'^news/(?P<slug>[\w-]+)/$', NewsUpdateView.as_view(), name='news-update'),
    url(r'^news/(?P<slug>[\w-]+)/delete/$', NewsDeleteView.as_view(), name='news-delete'),
    url(r'^reviews/$', ReviewTemplateView.as_view(), name='reviews'),
    url(r'^reviews/create/$', ReviewsCreateView.as_view(), name='reviews-create'),
    url(r'^reviews/pc-games/$', PcTemplateView.as_view(), name='pc'),
    url(r'^reviews/android-games/$', AndroidTemplateView.as_view(), name='android'),
    url(r'^reviews/(?P<slug>[\w-]+)/$', GameUpdateView.as_view(), name='edit'),
    url(r'^gamereview/(?P<slug>[\w-]+)/$', GameDetailView.as_view(), name='gamereview'),
    url(r'^gamereview/(?P<pk>[\w-]+)/comment-delete/$', CommentDeleteView.as_view(), name='comment-delete'),
    url(r'^gamereview/(?P<slug>[\w-]+)/delete/$', GameDeleteView.as_view(), name='delete'),
    url(r'^topgames/$', TopgamesListView.as_view(), name='topgames'),
    url(r'^topgames/create/$', TopgamesCreateView.as_view(), name='topgames-create'),
    url(r'^topgames/(?P<slug>[\w-]+)/$', TopgamesUpdateView.as_view(), name='topgames-update'),
    url(r'^topgames/(?P<slug>[\w-]+)/delete/$', TopgamesDeleteView.as_view(), name='topgames-delete'),
    url(r'^support/$', TemplateView.as_view(template_name='support.html'), name='support'),
    url(r'^post-panel/$', TemplateView.as_view(template_name='bootstrap/postPanel/index.html'), name='post-panel'),

]

if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)