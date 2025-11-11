from django.core.management.base import BaseCommand
from django.utils import timezone

from base.models import Asset


class Command(BaseCommand):
    help = "Finds assets whose end_date has passed and sets is_active to False."

    def handle(self, *args, **options):
        # Get today's date
        today = timezone.now().date()

        # Find all assets that are still active BUT
        # their end_date is in the past (less than today).
        assets_to_deactivate = Asset.objects.filter(
            is_active=True,
            end_date__isnull=False,  # Make sure end_date is set
            end_date__lt=today,  # end_date is "less than" today
        )

        if not assets_to_deactivate.exists():
            self.stdout.write(self.style.SUCCESS("No assets to deactivate today."))
            return

        # Get the count *before* updating
        count = assets_to_deactivate.count()

        # Update them all in one efficient database query
        assets_to_deactivate.update(is_active=False)

        self.stdout.write(
            self.style.SUCCESS(f"Successfully deactivated {count} expired asset(s).")
        )
