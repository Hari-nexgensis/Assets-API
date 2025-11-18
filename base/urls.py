from django.urls import path

from . import views

urlpatterns = [
    # React frontend
    path("", views.home, name="home"),
    
    # API endpoints
    path("assets/", views.asset_list_create, name="asset-list-create"),
    path("assets/<int:pk>/", views.asset_detail, name="asset-detail"),
    path("assets/<int:pk>/children/", views.asset_children, name="asset-children"),
]
