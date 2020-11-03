from django.urls import path

from . import views

app_name = 'ordersys'

urlpatterns = [
    path('', views.OrdersView.as_view(), name='index'),
    path('pending/', views.PendingOrdersView.as_view(), name='pending'),
    path('<int:pk>/start_preparing/', views.start_preparing_order, name='start_preparing'),
    path('<int:pk>/finish_preparing/', views.finish_preparing_order, name='finish_preparing'),
    path('<int:pk>/collect_order/', views.collected_order, name='collect_preparing'),
    path('prepare/', views.PrepareOrdersView.as_view(), name='prepare'),
    path('collect/', views.CollectOrdersView.as_view(), name='collect'),
    path('done/', views.DoneOrdersView.as_view(), name='done'),
    path('customers/', views.CustomersOrdersView.as_view(), name='customers'),
]