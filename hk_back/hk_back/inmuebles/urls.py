from django.urls import path
from .views import (
    InmueblesAllView,
    InmueblesPersonalView,
    InmueblesCreateView,
    InmuebleDetailView
)

urlpatterns = [
    path('inmuebles', InmueblesAllView.as_view(), name='inmuebles'),
    path('inmuebles-personales', InmueblesPersonalView.as_view(), name='inmuebles-personales'),
    path('inmuebles-create', InmueblesCreateView.as_view(), name='inmuebles-create'),
    path('inmuebles/<int:id>', InmuebleDetailView.as_view(), name='inmueble-detail'),
]