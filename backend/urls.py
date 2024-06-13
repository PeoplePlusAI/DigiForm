from django.urls import path
from django.views.decorators.csrf import csrf_exempt
from . import views

urlpatterns = [
    path('details/', csrf_exempt(views.details), name='details'),
    path('update/', csrf_exempt(views.update), name='update'),
    path('process/', csrf_exempt(views.process), name='process'),
    path('converse/', csrf_exempt(views.converse), name='converse'),
]
