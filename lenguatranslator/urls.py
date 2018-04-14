from django.conf.urls import include, url
from django.urls import path

from django.contrib import admin

from texts import urls as t_urls
from profile import urls as p_urls

admin.autodiscover()

import hello.views

# Examples:
# url(r'^$', 'lenguatranslator.views.home', name='home'),
# url(r'^blog/', include('blog.urls')),
from django.contrib.auth import views as auth_views

urlpatterns = [
    url(r'^$', hello.views.index, name='index'),
    url(r'^db', hello.views.db, name='db'),
    url(r'^profile/', include(p_urls), name='translate'),
    url(r'^api/', include(t_urls), name='translate'),
    path('admin/', admin.site.urls),
]
