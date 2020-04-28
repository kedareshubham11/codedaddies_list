from django.urls import path
from . import views

app_name = 'my_app'
urlpatterns = [
    path('', views.home, name='home'),
    path('new_search', views.new_search, name='new_search'),
    path('search_history', views.search_history, name='search_history'),
    path('delete_history/<int:history_id>', views.delete_history, name='delete_history'),
    path('delete_all_history', views.delete_all_history, name='delete_all_history'),
    path('goto/<str:search>', views.goto, name='goto'),

        
]