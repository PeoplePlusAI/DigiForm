from django.urls import path
from django.views.decorators.csrf import csrf_exempt
from . import views

urlpatterns = [
    path('start/', csrf_exempt(views.start), name='start'),
    path('prompt/', csrf_exempt(views.prompt), name='prompt'),
]
