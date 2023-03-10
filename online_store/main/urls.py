from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('imports', views.add_imports, name='add_import'),
    path('imports/<int:import_id>/citizens/<int:citizen_id>',
         views.change_citizen_data, name='change_citizen'),
    path('imports/<int:import_id>/citizens', views.get_citizens,
         name='get_import_citizens'),
    path('imports/<int:import_id>/citizens/birthdays',
         views.get_import_citizens_birthsdays,
         name='get_import_citizens_birthdays'),
    path('imports/<int:import_id>/towns/stat/percentile/age',
         views.get_percentile_age, name='get_percentile_age')
]
