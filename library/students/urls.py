from django.urls import path
from . import views

app_name = 'students' 


urlpatterns = [
    path('', views.student_list, name='student_list'),
    path('add/', views.student_create, name='student_add'),
    path('delete/', views.student_delete_search, name='student_delete_search'),
    path('<int:pk>/', views.student_detail, name='student_detail'),
    path('<int:pk>/borrow/', views.borrow_book, name='borrow_book'),
    path('borrow/<int:borrow_id>/return/', views.return_borrowed_book, name='return_borrowed_book'),
    path('borrow/<int:pk>/delete/', views.delete_borrow_record, name='delete_borrow_record'),
]
