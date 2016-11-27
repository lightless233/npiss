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
from apps.user_app.views import LoginView
from apps.user_app.views import RegisterView

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
]
