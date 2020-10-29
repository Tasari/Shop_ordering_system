from django.urls import path

from . import views

app_name = 'ordersys'

urlpatterns = [
    path('', views.OrdersView.as_view(), name='index'),
    path('pending/', views.PendingOrdersView.as_view(), name='pending'),
    path('prepare/', views.PrepareOrdersView.as_view(), name='prepare'),
    path('collect/', views.CollectOrdersView.as_view(), name='collect'),
    path('done/', views.DoneOrdersView.as_view(), name='done'),
    path('customers/', views.CustomersOrdersView.as_view(), name='customers'),
]