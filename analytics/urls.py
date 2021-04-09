from django.urls import path
from . import views

urlpatterns = [
    path('<int:pk>/', views.analytics, name='analytics'),

    # item detail
    path('olditem/<int:pk>/', views.old_item_detail, name='old-item-detail'),
    path('newitem/<int:pk>/', views.new_item_detail, name='new-item-detail'),

    # item CRUD
    path('newitem/<int:pk>/edit/', views.new_item_edit, name='new-item-edit'),
    path('newitem/<int:pk>/delete/', views.new_item_delete, name='new-item-delete'),
    path('olditem/<int:pk>/edit/', views.old_item_edit, name='old-item-edit'),
    path('olditem/<int:pk>/delete/', views.old_item_delete, name='old-item-delete'),

    # charts
    path('charts/<int:pk>/', views.savings_chart, name='savings-chart'),
]