from datetime import date

from django.core.exceptions import ValidationError
from django.db import models
from django.db.models.signals import pre_delete
from django.dispatch import receiver
from mptt.models import MPTTModel, TreeForeignKey

# Create your models here.


class Asset(MPTTModel):
    asset_name = models.CharField(max_length=255, db_index=True)
    asset_code = models.CharField(max_length=255, unique=True)
    parent = TreeForeignKey(
        "self",  # This tells Django the relationship is with the *same* model
        on_delete=models.SET_NULL,  # Best option for this
        null=True,
        blank=True,
        related_name="children",  # Lets you do asset.children.all()
    )
    asset_type = models.CharField(max_length=255)
    location = models.CharField(max_length=255)
    manager = models.CharField(max_length=255)
    is_active = models.BooleanField(
        default=True, help_text="Is this asset currently in service"
    )
    # hierarchy_level = models.PositiveIntegerField(default = 0, help_text="A number to define the asset's level in a hierarchy (e.g., 0=Top, 1=Child).")
    start_date = models.DateField(
        default=date.today, help_text="Date the asset was put into service."
    )
    end_date = models.DateField(
        null=True,
        blank=True,
        help_text="Date the asset was decommissioned or inactivated.",
    )
    # This single field will hold all your dynamic "columns"
    custom_data = models.JSONField(
        default=dict,
        blank=True,
        null=True,
        help_text="Flexible field for custom data (e.g., {'warranty_id': 'XYZ-123'})",
    )

    def soft_delete(self):
        self.is_active = False
        self.end_date = date.today()
        self.save()

    def restore(self):
        self.is_active = True
        self.end_date = None
        self.save()

    def delete(self, *args, **kwargs):
        """
        Overrides the default delete method to perform a soft delete.
        """
        self.soft_delete()

    def hard_delete(self, *args, **kwargs):
        """
        Permanently deletes the asset from the database.
        """
        # This calls the original, un-overridden delete method
        super().delete(*args, **kwargs)

    def __str__(self):
        return f"{self.asset_name} ({self.asset_code})"


@receiver(pre_delete, sender=Asset)
def reparent_children_on_delete(sender, instance, **kwargs):
    """
    Before deleting an asset, find its children and
    re-assign them to this asset's parent (the "grandparent").
    """

    # 1. Find the new parent
    new_parent = instance.parent

    # 2. update their 'parent' field to be the 'new_parent'.
    #    This is done in a single, efficient database query.
    instance.children.update(parent=new_parent)
