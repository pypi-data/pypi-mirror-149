""" AccountRequestMetadata model
"""

from django_mongoengine import fields

from core_user_registration_app.components.user_metadata.models import UserMetadata
from core_website_app.components.account_request.models import AccountRequest


class AccountRequestMetadata(AccountRequest):
    """AccountRequestMetadata."""

    metadata = fields.ReferenceField(UserMetadata, blank=True)

    @staticmethod
    def get_all():
        """Get all Account Request Metadata

        Returns:

        """
        return AccountRequestMetadata.objects.all()
