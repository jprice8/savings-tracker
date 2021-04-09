from django.urls import path
from . import views

urlpatterns = [
    path('conversions/', views.conversions, name='conversions'),

    # conversion CRUD
    path('conversions/add/', views.add_conversion, name='add-conversion'),
    path('conversions/<int:pk>/edit/', views.edit_conversion, name='edit-conversion'),
    path('conversions/<int:pk>/delete/', views.delete_conversion, name='delete-conversion'),

    # conversion detail
    path('conversions/<int:pk>/', views.conversion_detail, name='conversion-detail'),
    path('conversions/<int:pk>/addolditem/', views.add_old_item, name='add-old-item'),
    path('conversions/<int:pk>/addnewitem/', views.add_new_item, name='add-new-item'),


]