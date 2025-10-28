from django.urls import path
from . import views

app_name = 'records'

urlpatterns = [
    path('', views.home, name='home'),
    path('records/', views.create_record, name='create_record'),
    path('records/<int:record_id>/', views.record_detail, name='record_detail'),
]