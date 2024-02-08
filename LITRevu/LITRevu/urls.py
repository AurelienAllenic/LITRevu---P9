from djangoApp import views
from django.contrib import admin
from django.urls import path
from django.contrib.auth.views import LogoutView
from django.conf import settings
from django.conf.urls.static import static

"""
URL configuration for LITRevu project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""

urlpatterns = [
    path('', views.home_view, name='home'),
    path('signup', views.signup_view, name='signup'),
    path('flux', views.flux_view, name='flux'),
    path('posts', views.posts_view, name='posts'),
    path('subscribes', views.subscribes_view, name='subscribes'),
    path('login', views.login_view, name='login'),
    path('tickets', views.tickets_view, name='tickets'),
    path('createCritic', views.createCritic_view, name='createCritic'),
    path('createTicket', views.createTicket_view, name='createTicket'),
    path('logout', LogoutView.as_view(next_page='/'), name='logout'),
    path('edit/<str:type>/<int:id>/', views.edit_post, name='edit_post'),
    path('delete/<str:type>/<int:id>/', views.delete_post, name='delete_post'),
    path('admin', admin.site.urls),
]


if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)