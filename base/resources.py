from import_export import resources
from .models import Asset

class AssetResource(resources.ModelResource):
    class Meta:
        model = Asset
        # This is optional, but good for skipping new records
        skip_unchanged = True
        # This will create assets that don't exist
        import_id_fields = ('asset_code',) 
        # You can specify which fields to use
        fields = ('asset_name', 'asset_code', 'asset_type', 'location', 'manager', 'is_active', 'hierarchy_level', 'start_date', 'end_date')