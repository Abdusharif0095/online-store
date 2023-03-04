from django.urls import path
from . import views

urlpatterns = [
    path('', views.index),
    path('imports', views.add_imports),
    path('imports/<int:import_id>/citizens/<int:citizen_id>', views.change_citizen_data),
    path('imports/<int:import_id>/citizens', views.get_citizens)
]