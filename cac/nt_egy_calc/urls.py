

from django.urls import path
from . import views
from .views import ask_chatgpt #ask_chatgpt_dummy, 
from .views import trends_view


#from .views import ask_chatgpt,
urlpatterns = [
    path('', views.home, name='home'),
    path('calculator/', views.calculator, name='calculator'),
    path('delete/', views.delete_data, name='delete_data'),
    path('recalculate/', views.recalculate, name='recalculate'),
    path('chat/', ask_chatgpt, name='chat'),
    #path('ask_chatgpt/', ask_chatgpt_dummy, name='ask_chatgpt'),
    path('trends/', trends_view, name='trends'),
]
