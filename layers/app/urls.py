from django.urls import path
from .views import index

urlpatterns = [
   path('<str:group_name>',index ),
]