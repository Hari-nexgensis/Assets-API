

from django.contrib import admin
from .models import Asset
from import_export.admin import ImportExportModelAdmin
from .resources import AssetResource # <-- Import your resource

# Use ImportExportModelAdmin instead of the standard ModelAdmin
class AssetAdmin(ImportExportModelAdmin):
    resource_class = AssetResource # <-- Connect the resource
    list_display = ('asset_name', 'asset_code', 'asset_type', 'location', 'is_active')
    search_fields = ('asset_name', 'asset_code')

admin.site.register(Asset, AssetAdmin)
