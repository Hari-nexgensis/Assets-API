from django.db.models import Q
from django.http import HttpResponse
from django.shortcuts import render
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.pagination import PageNumberPagination
from rest_framework.response import Response

from .models import Asset
from .serializers import AssetSerializer

# Create your views here.


def home(request):
    """Serve the React application"""
    return render(request, "home.html")


@api_view(["GET", "POST"])
def asset_list_create(request):
    """
    List all assets, or create a new asset.
    """
    if request.method == "GET":
        # Get all assets from the database
        assets = Asset.objects.all()

        # Global search across all fields
        global_search = request.query_params.get("search", None)
        if global_search:
            assets = assets.filter(
                Q(asset_name__icontains=global_search) |
                Q(asset_code__icontains=global_search) |
                Q(asset_type__icontains=global_search) |
                Q(location__icontains=global_search) |
                Q(manager__icontains=global_search)
            )

        # Individual field filters
        asset_name = request.query_params.get("asset_name", None)
        asset_code = request.query_params.get("asset_code", None)
        asset_type = request.query_params.get("asset_type", None)
        location = request.query_params.get("location", None)
        manager = request.query_params.get("manager", None)
        is_active = request.query_params.get("is_active", None)

        # Apply filters if provided
        if asset_name:
            assets = assets.filter(asset_name__icontains=asset_name)
        if asset_code:
            assets = assets.filter(asset_code__icontains=asset_code)
        if asset_type:
            assets = assets.filter(asset_type__icontains=asset_type)
        if location:
            assets = assets.filter(location__icontains=location)
        if manager:
            assets = assets.filter(manager__icontains=manager)
        if is_active:
            assets = assets.filter(is_active=(is_active.lower() == 'true'))

        # Sorting
        sort_by = request.query_params.get("sort_by", "id")
        order = request.query_params.get("order", "asc")
        
        # Valid sort fields
        valid_fields = ['id', 'asset_name', 'asset_code', 'asset_type', 'location', 'manager', 'start_date', 'is_active']
        if sort_by in valid_fields:
            if order == "desc":
                assets = assets.order_by(f"-{sort_by}")
            else:
                assets = assets.order_by(sort_by)

        # Instantiate the paginator
        paginator = PageNumberPagination()

        # Set your page size (how many items per page)
        paginator.page_size = 10

        # Paginate the filtered queryset
        paginated_queryset = paginator.paginate_queryset(assets, request)

        # Serialize the *paginated* queryset
        serializer = AssetSerializer(paginated_queryset, many=True)

        # Return the paginator's formatted response
        # This automatically adds "count", "next", and "previous"
        return paginator.get_paginated_response(serializer.data)
        # Serialize the list of assets
        # serializer = AssetSerializer(assets, many=True)

        # Return the JSON response
        # return Response(serializer.data, status=status.HTTP_200_OK)

    elif request.method == "POST":
        # Get the incoming data from the request
        data = request.data

        # Create a new serializer instance with the incoming data
        serializer = AssetSerializer(data=data)

        # Validate the data
        if serializer.is_valid():
            # If valid, save the new object to the database
            serializer.save()
            # Return the newly created object's data and a 201 status
            return Response(serializer.data, status=status.HTTP_201_CREATED)

        # If invalid, return the errors and a 400 status
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(["GET", "PUT", "DELETE"])
def asset_detail(request, pk):
    """
    Retrieve, update or delete a single asset by its primary key (pk).
    """
    try:
        # Try to find the asset with the given primary key
        asset = Asset.objects.get(pk=pk)
    except Asset.DoesNotExist:
        # If it doesn't exist, return a 404 Not Found
        return Response({"error": "Asset not found"}, status=status.HTTP_404_NOT_FOUND)

    if request.method == "GET":
        # Serialize the single asset
        serializer = AssetSerializer(asset)
        # Return its data
        return Response(serializer.data, status=status.HTTP_200_OK)

    elif request.method == "PUT":
        # Get the incoming data
        data = request.data
        # Update the asset instance with the new data
        serializer = AssetSerializer(asset, data=data)

        # Validate the new data
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)

        # If invalid, return errors
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    elif request.method == "DELETE":
        # Delete the asset from the database
        asset.delete()
        # Return a 204 No Content status
        return Response(status=status.HTTP_204_NO_CONTENT)


@api_view(["GET"])
def asset_children(request, pk):
    """
    Get all direct children of a specific asset.
    """
    try:
        asset = Asset.objects.get(pk=pk)
    except Asset.DoesNotExist:
        return Response({"error": "Asset not found"}, status=status.HTTP_404_NOT_FOUND)

    # Get direct children only
    children = asset.children.all()
    serializer = AssetSerializer(children, many=True)
    
    return Response({
        "parent": AssetSerializer(asset).data,
        "children": serializer.data,
        "count": children.count()
    }, status=status.HTTP_200_OK)
