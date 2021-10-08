"""codeera URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.2/topics/http/urls/
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
from django.contrib import admin
from django.urls import path, re_path, include

from django.contrib.auth import views as auth_views

from django.conf import settings
from django.conf.urls.static import static


from tweetcode.views import (
    dashboard,
    post_detail_view,
    post_delete_view,
    post_list_view,
    post_create_view,
    index,
    loginUser,
    registerUser,
    logoutUser,
    newsFeed
)
urlpatterns = [
    path('admin/', admin.site.urls),
    path('',index,name="home"),
    path('dashboard/',dashboard),
    path('login/',loginUser,name="login"),
    path('register/',registerUser,name="register"),
    path('logout/',logoutUser,name="logout"),
    path('home/',newsFeed),
    path('create-post',post_create_view),
    path('posts/',post_list_view),
    path('posts/<int:post_id>',post_detail_view),
    path('api/posts/<int:post_id>/delete',post_delete_view),
    path('api/posts/', include('tweetcode.urls')),


    path('reset_password/', auth_views.PasswordResetView.as_view(template_name="pages/password_reset.html"),name="reset_password"),
    path('reset_password_sent/', auth_views.PasswordResetDoneView.as_view(template_name="pages/password_reset_sent.html"),name="password_reset_done"),
    path('reset/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view(template_name="pages/password_reset_form.html"),name="password_reset_confirm"),
    path('reset_password_complete/', auth_views.PasswordResetCompleteView.as_view(template_name="pages/password_reset_done.html"),name="password_reset_complete"),


    ]
if settings.DEBUG:
    urlpatterns +=  static(settings.STATIC_URL,document_root=settings.STATIC_ROOT)

    