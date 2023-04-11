from django.urls import path
from . import views

app_name = 'item'
urlpatterns = [
    path('', views.items, name='items'),
    path('add-item/', views.addItem, name='add-item'),
    path('edit/<int:pk>/', views.editItem, name='edit'),
    path('delete/<int:pk>/', views.delete, name='delete'),
    path('<int:pk>/', views.detail, name='detail'),
]
