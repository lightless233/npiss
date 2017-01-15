# coding: utf-8
"""piss URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.10/topics/http/urls/
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
from django.conf.urls import url
from django.contrib import admin

from apps.index_app.views import IndexView
from apps.engine_app.views import ApiUploadImageView
from apps.engine_app.views import ApiUploadURLView
from apps.user_app.UserController import LoginView
from apps.user_app.UserController import RegisterView
from apps.user_app.UserController import ValidEmailView
from apps.user_app import ManagerController
from apps.user_app import HomeController
from apps.engine_app import ShowController

urlpatterns = [
    url(r'^admin/', admin.site.urls),

    # index views
    url(r'^$', IndexView.as_view(), name="index"),
    url(r'^index$', IndexView.as_view(), name="index"),

    # api views
    url(r'^api/upload/file$', ApiUploadImageView.as_view(), name="upload_file"),
    url(r'^api/upload/url$', ApiUploadURLView.as_view(), name="upload_url"),

    # user views
    url(r'^login$', LoginView.as_view(), name="login"),
    url(r'^register$', RegisterView.as_view(), name='register'),
    url(r'^v_email$', ValidEmailView.as_view(), name="validate_email"),

    # manage controller start
    url(r'^manage/generate/ac$', ManagerController.GenerateACView.as_view(), name="generate_ac"),
    url(r'^manage/get/ac$', ManagerController.QueryACView.as_view(), name="get_ac"),
    # manage controller end

    # 用户个人中心部分路由 开始 ##
    url(r'^home/index$', HomeController.DashboardView.as_view(), name="home_dashboard"),
    url(r'^home/images$', HomeController.ImageListView.as_view(), name="home_image_list"),
    url(r'^home/logout$', HomeController.LogoutView.as_view(), name="logout"),
    # 用户个人中心部分路由 结束 ##

    # 图片短链展示部分 开始 ##
    url(r'^i/(?P<image_name>.+)$', ShowController.ShowNormalImages.as_view(), name="show_normal_image"),
    url(r'^t/(?P<image_name>.+)$', ShowController.ShowThumbImages.as_view(), name="show_thumb_image"),
    url(r'^r/(?P<image_name>.+)$', ShowController.ShowOriginImages.as_view(), name="show_origin_image"),
    # 图片短链展示部分 结束 ##

]
