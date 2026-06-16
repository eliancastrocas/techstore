from django.urls import path
from . import views

urlpatterns = [
    path("", views.product_list, name="product_list"),
    path("catalogo/", views.product_catalog, name="product_catalog"),
    path("search/", views.product_search, name="product_search"),
    path("servicios/", views.services_catalog, name="services_catalog"),
    path("service_create/", views.service_create, name="service_create"),
    path("service_list/", views.service_list, name="service_list"),
    path("service_update/<int:pk>/", views.service_update, name="service_update"),
    path("service_delete/<int:pk>/", views.service_delete, name="service_delete"),
    path("garantia/", views.warranty_request, name="warranty_request"),
    path("garantia/lista/", views.warranty_request_list, name="warranty_list"),
    path("solicitudes/", views.vendor_form_requests, name="vendor_form_requests"),
    path("create/", views.product_create, name="product_create"),
    path("update/<int:pk>/", views.product_update, name="product_update"),
    path("delete/<int:pk>/", views.product_delete, name="product_delete"),
    path("carga-masiva/", views.bulk_upload, name="bulk_upload"),
    path("ciudades/", views.cities_list, name="cities_list"),
    path("reparacion-form/", views.reparacion_form, name="reparacion_form"),
    path("mantenimiento-form/", views.mantenimiento_form, name="mantenimiento_form"),
]
