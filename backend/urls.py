from django.urls import path
from django.views.decorators.csrf import csrf_exempt
from . import views

urlpatterns = [
    path('clear/', csrf_exempt(views.clear), name='clear'),
    path('details/', csrf_exempt(views.details), name='details'),
    path('update/', csrf_exempt(views.update), name='update'),
    path('process/', csrf_exempt(views.process), name='process'),
    path('converse/', csrf_exempt(views.converse), name='converse'),
    path('image/', csrf_exempt(views.image), name='image'),
    path('done/', csrf_exempt(views.done), name='done'),
]
