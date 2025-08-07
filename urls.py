"""fitness URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.2/topics/http/urls/
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
import settings
from django.contrib import admin
from django.urls import path, include

from django.conf.urls.static import static

from products.views import create_product, get_product
from qrcodes.views import create_qrcode, get_qrcode
from start.views.start import start, reload_start

urlpatterns = [
    path('admin/', admin.site.urls),
    path('',start,name='start'),
    path('reload/',reload_start,name='reload_start'),
    path('create_product/',create_product,name='create_product'),
    path('create_qrcode',create_qrcode,name='create_qrcode'),
    path('get_qrcode/<int:product_id>/',get_qrcode,name='get_qrcode'),
    path('get_product/<uuid:qr_uuid>/',get_product,name='get_product'),




] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
