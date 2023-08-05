"""User Registration tasks """

import logging
from datetime import timedelta

from celery import shared_task
from django.utils import timezone

from core_user_registration_app.settings import (
    USER_DATA_STRUCTURE_HOURS_THRESHOLD,
)
from core_user_registration_app.system import api as system_api

logger = logging.getLogger(__name__)


@shared_task
def delete_user_data_structure():
    """DELETES every DELETE_USER_DATA_STRUCTURE_RATE the UserDataStructure in the DataStructure collection"""
    logger.info("Checking Old UserDataStructures")
    try:
        for data_structure_element in system_api.get_all_data_structure_elements():
            if (
                data_structure_element.data_structure
                and data_structure_element.data_structure.collection
                == "user_data_structure"
            ):
                if (
                    data_structure_element.id.generation_time
                    < timezone.now()
                    - timedelta(hours=USER_DATA_STRUCTURE_HOURS_THRESHOLD)
                ):
                    data_structure_element.delete()
        logger.info("FINISH checking DataStructures.")

    except Exception as e:
        logger.error(f"ERROR : Error while deleting data structures: {str(e)}")
