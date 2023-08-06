from django.urls import path, include
from . import views

urlpatterns = [
    path('hello/', views.helloView, name='hello'),
    path('user/<int:id>/',views.MomoPaymentView.as_view()),
    path('callback/',views.MomoPaymentCallbackView.as_view()),
]