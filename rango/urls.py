# rango/urls.py

from django.contrib import admin
from django.urls import path, include

# 1. GARANTA QUE ESTES IMPORTS ESTÃO AQUI
from django.conf import settings
from django.conf.urls.static import static

# 2. SUAS URLS PRINCIPAIS
urlpatterns = [
    path('admin/', admin.site.urls),
    path('janela/', include('janela.urls')),
]

# 3. A PARTE MAIS IMPORTANTE (E QUE ESTAVA FALTANDO)
# Este bloco DEVE estar aqui, no final do arquivo, para que o Django
# aprenda a servir os arquivos da pasta 'media' em modo de desenvolvimento.
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)