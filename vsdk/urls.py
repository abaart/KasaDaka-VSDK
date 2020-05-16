"""vsdk URL Configuration

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
from django.conf.urls import url, include
from django.contrib import admin
from django.conf.urls.static import static
from django.utils.translation import ugettext_lazy as _
from django.conf import settings
from django.conf.urls.i18n import i18n_patterns

admin.site.site_header = _("KasaDaka Voice Services")

urlpatterns = [
    url(r'^', admin.site.urls),
    url(r'^i18n/', include('django.conf.urls.i18n')),
    url(r'^vxml/', include('vsdk.service_development.urls')),
] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT) + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

urlpatterns += i18n_patterns(
    url(r'^forobablon/', include('vsdk.forobablon.urls')),
)

#if not settings.DEBUG:
#        urlpatterns += urlpatterns('',
#                (r'^media/(?P<path>.*)$', 'django.views.static.serve', {'document_root': settings.MEDIA_ROOT, 'show_indexes': True, }),
#                (r'^static/(?P<path>*)$', 'django.views.static.serve', {'document_root': settings.STATIC_ROOT}))
