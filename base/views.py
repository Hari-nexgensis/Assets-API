from django.shortcuts import render
from django.http import HttpResponse
from django.db.models import Q
from rest_framework.pagination import PageNumberPagination
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response
from .models import Asset
from .serializers import AssetSerializer

# Create your views here.

def home(request):
    return render(request, 'home.html')
def assets(request):
    return render(request, 'assets.html')




@api_view(['GET', 'POST'])
def asset_list_create(request):
    """
    List all assets, or create a new asset.
    """
    if request.method == 'GET':
        # Get all assets from the database
        assets = Asset.objects.all()
        
        search_query = request.query_params.get('search', None)
        if search_query:
            # Filter by any of the fields that match the query
            # '__icontains' means "case-insensitive contains"
            assets = assets.filter(
                Q(asset_name__icontains=search_query) |
                Q(asset_code__icontains=search_query) 
                # Q(asset_type__icontains=search_query) |
                # Q(location__icontains=search_query) |
                # Q(manager__icontains=search_query)
            )

            # THIS PAGINATION LOGIC ---
        
        # Instantiate the paginator
        paginator = PageNumberPagination()
        
        # Set your page size (how many items per page)
        paginator.page_size = 5 
        
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

    elif request.method == 'POST':
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


@api_view(['GET', 'PUT', 'DELETE'])
def asset_detail(request, pk):
    """
    Retrieve, update or delete a single asset by its primary key (pk).
    """
    try:
        # Try to find the asset with the given primary key
        asset = Asset.objects.get(pk=pk)
    except Asset.DoesNotExist:
        # If it doesn't exist, return a 404 Not Found
        return Response({'error': 'Asset not found'}, status=status.HTTP_404_NOT_FOUND)

    if request.method == 'GET':
        # Serialize the single asset
        serializer = AssetSerializer(asset)
        # Return its data
        return Response(serializer.data, status=status.HTTP_200_OK)

    elif request.method == 'PUT':
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

    elif request.method == 'DELETE':
        # Delete the asset from the database
        asset.delete()
        # Return a 204 No Content status
        return Response(status=status.HTTP_204_NO_CONTENT)
