
from django.urls import path
from . import views

urlpatterns = [
    path('create_transaction/', views.create_transaction, name='create_transaction'),
    path('transaction_list/', views.transaction_list, name='transaction_list'),  # Add this line
    path('group_liability/<int:group_id>/', views.group_liabilities_view, name='group_liability'),
    path('user_liability/<int:user_id>/', views.user_liability_view, name='user_liability'),
    path('make_payment/<int:group_id>/', views.make_payment, name='make_payment'),
    path('edit_transaction/<int:transaction_id>/', views.update_transaction, name='edit_transaction'),
    path('get-members/<int:group_id>/', views.get_members, name='get_members'),
]
 