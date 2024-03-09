from django.urls import path

from main.views import PaymentView

urlpatterns = [
    path('', PaymentView.as_view(), name='')
]
