from django.test import TestCase
from django.contrib.auth.models import User
from rest_framework.test import APITestCase
from rest_framework import status
from .models import Asset  # Import your Asset model

class AssetAPITests(APITestCase):

    def setUp(self):
        """
        This method runs before every single test.
        """
        # Create a test user
        self.user = User.objects.create_user(username='testuser', password='testpassword')
        
        # Create a sample asset
        self.asset = Asset.objects.create(
            asset_name="Lam, Smith and Shannon Software License 243",
            asset_code="CODE-00021",
            asset_type="Software License",
            location="Building B",
            manager="Krystal Wilcox",
            is_active=True,
            start_date="2025-05-30",
            end_date=None, 
            custom_data={},
            parent=None    
        )

    def test_get_asset_list(self):
        """
        Test retrieving the list of assets.
        """
        url = '/assets/'  # Make sure this URL is correct
        response = self.client.get(url)

        # Check the status code
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        # Check that our asset is in the response data
        response_data = response.json()
        
        # API is paginated, so check the 'results' key
        self.assertIn('results', response_data)
        self.assertGreaterEqual(len(response_data['results']), 1)
        
        # Check that our test asset is in the results
        asset_names = [asset['asset_name'] for asset in response_data['results']]
        self.assertIn("Lam, Smith and Shannon Software License 243", asset_names)

    def test_create_asset(self):
        """
        Test creating a new asset.
        """
        self.client.force_authenticate(user=self.user)

        # Define the new asset's data
        data = {
            "asset_name": "A Brand New Asset", 
            "asset_code": "CODE-00022",
            "asset_type": "Hardware",
            "location": "Building C",
            "manager": "Test User",
            "is_active": True, 
            "start_date": "2025-11-07",
            "end_date": None,  
            "custom_data": {},
            "parent": None     
        }

        url = '/assets/'
        response = self.client.post(url, data, format='json')

        # Check for '201 Created'
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        # Check that the asset was actually created in the database
        self.assertEqual(Asset.objects.count(), 2) # We had 1 from setUp, now 2
        
        # FIX: Check for the asset we just created
        new_asset = Asset.objects.get(asset_name="A Brand New Asset")
        self.assertIsNotNone(new_asset)
        self.assertEqual(new_asset.asset_code, "CODE-00022")