from django.urls import path
from . import views

app_name = 'portfolio_details'

urlpatterns = [
    path('<str:theme>/<str:color>/<int:id>/', views.details, name='details'),
]
