# /snippets/django_view/snippets/
# /snippets/django_view/snippets/<pk>

# /snippets/api_view/snippets/
# /snippets/api_view/snippets/<pk>
from django.urls import path, include
from . import django_view, api_view, mixins, generic_cbv, veiwsets_router

app_name = 'snippets'

urlpatterns = [
    path('django_view/', include(django_view)),
    path('api_view/', include(api_view)),
    path('mixins/', include(mixins)),
    path('generic_cbv/', include(generic_cbv)),
    path('veiwsets_router/', include(veiwsets_router)),
]
