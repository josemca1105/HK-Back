from django.urls import path
from .views import (
    InmueblesAllView,
    InmueblesPersonalView,
    InmueblesCreateView,
    InmuebleDetailView
)

urlpatterns = [
    path('inmuebles', InmueblesAllView.as_view(), name='inmuebles_api'),
    path('inmuebles-personales', InmueblesPersonalView.as_view(), name='inmuebles_personales_api'),
    path('inmuebles-create', InmueblesCreateView.as_view(), name='inmuebles_create_api'),
    path('inmuebles/<int:id>', InmuebleDetailView.as_view(), name='inmueble_detail_api'),
    path('inmuebles-update/<int:id>', InmuebleDetailView.as_view(), name='inmueble_update_api'),
    path('inmuebles-delete/<int:id>', InmuebleDetailView.as_view(), name='inmueble_delete_api'),
]