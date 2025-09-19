from django.urls import path
from . import views

app_name = 'books'

urlpatterns = [
    path('', views.book_list, name='book_list'),
    path('add/', views.book_create, name='book_add'),
    path('update/<int:pk>/', views.book_update, name='book_update'),
    path('delete/', views.book_delete_search, name='book_delete_search'),  # search + delete
]
