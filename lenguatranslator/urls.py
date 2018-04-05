from django.conf.urls import include, url
from django.urls import path

from django.contrib import admin

from texts import urls as t_urls

admin.autodiscover()

import hello.views

# Examples:
# url(r'^$', 'lenguatranslator.views.home', name='home'),
# url(r'^blog/', include('blog.urls')),

urlpatterns = [
    url(r'^$', hello.views.index, name='index'),
    url(r'^db', hello.views.db, name='db'),
    url(r'^translate', include(t_urls), name='translate'),
    path('admin/', admin.site.urls),
]
