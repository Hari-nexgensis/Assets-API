from django.urls import path
from . import views

urlpatterns = [
    path('',views.home, name='home'),
    path('asset/', views.assets, name='asset'),
        # /api/assets/
    path('assets/', views.asset_list_create, name='asset-list-create'),
    
    # /api/assets/<id>/
    # The <int:pk> captures the ID from the URL and passes it as 
    # a variable named 'pk' to your asset_detail view.
    path('assets/<int:pk>/', views.asset_detail, name='asset-detail'),
]