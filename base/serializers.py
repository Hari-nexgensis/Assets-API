from rest_framework import serializers
from .models import Asset

class AssetSerializer(serializers.ModelSerializer):
    """
    Serializes the Asset model to and from JSON.
    """
    class Meta:
        model = Asset
        fields = '__all__'

    def validate(self, data):
        """
        Custom validation to check that an asset is not its own parent.
        This method is automatically run by serializer.is_valid().
        """
        
        # This validation only matters during an update
        if self.instance:
            # Check if 'parent' is one of the fields being updated
            if 'parent' in data:
                new_parent = data['parent'] # This is the new parent object
                
                # Check if the new parent is the same as the asset itself
                if new_parent == self.instance:
                    # This error will be caught by .is_valid()
                    # and returned as a 400 Bad Request.
                    raise serializers.ValidationError({
                        'parent': 'An asset cannot be its own parent.'
                    })
        # Always return the validated data
        return data