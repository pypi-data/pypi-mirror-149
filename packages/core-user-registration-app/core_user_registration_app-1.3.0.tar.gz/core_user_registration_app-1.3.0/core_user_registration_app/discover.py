""" Initialize permissions for core user registration app.
"""
import logging

from django.contrib.auth.models import Group, Permission
from django.core.exceptions import ObjectDoesNotExist
from django_celery_beat.models import CrontabSchedule, PeriodicTask

import core_main_app.permissions.rights as main_rights
import core_user_registration_app.permissions.rights as registration_rights
from core_user_registration_app.components.user_template_version_manager import (
    api as user_version_manager_api,
)
from core_user_registration_app.settings import (
    REGISTRY_XSD_USER_FILENAME,
    REGISTRY_XSD_USER_FILEPATH,
)
from core_user_registration_app.system import api as registry_system_api
from core_user_registration_app.tasks import delete_user_data_structure

logger = logging.getLogger(__name__)

from os.path import join

from django.contrib.staticfiles import finders

from core_user_registration_app.settings import (
    XSL_FOLDER_PATH,
    LIST_XSL_FILENAME,
    DETAIL_XSL_FILENAME,
)
from core_main_app.commons import exceptions

from core_main_app.components.xsl_transformation import api as xslt_transformation_api
from core_main_app.components.xsl_transformation.models import XslTransformation
from core_main_app.utils.file import read_file_content


def init_registration_app():
    """Init the registry. Add the registry template.

    Returns:

    """

    try:
        # Init scheduled tasks
        _init_periodic_tasks()
        # Add template
        _add_user_template()
        # Init the permissions
        _init_permissions()
        # Init the xslt
        _init_xslt()
    except Exception as e:
        logger.error("Impossible to init the registration app: {0}".format(str(e)))


def _init_permissions():
    """Initialization of groups and permissions."""
    try:
        # Get or Create the default group
        anonymous, created = Group.objects.get_or_create(
            name=main_rights.anonymous_group
        )

        # Get registration permissions
        register_access_perm = Permission.objects.get(
            codename=registration_rights.register_access
        )
        register_view_data_save_repo_perm = Permission.objects.get(
            codename=registration_rights.register_data_structure_access
        )

        # Add permissions to default group
        anonymous.permissions.add(
            register_access_perm,
            register_view_data_save_repo_perm,
        )

    except Exception as e:
        logger.error("Impossible to init register permissions: %s" % str(e))


def _add_user_template():
    """Add the registry template.

    Returns:

    """
    xsd_filepath = REGISTRY_XSD_USER_FILEPATH
    xsd_filename = REGISTRY_XSD_USER_FILENAME
    if xsd_filename == "":
        raise Exception(
            "Please configure the REGISTRY_XSD_USER_FILENAME setting in your project."
        )
    if xsd_filepath == "":
        raise Exception(
            "Please configure the REGISTRY_XSD_USER_FILEPATH setting in your project."
        )
    try:
        registry_system_api.get_active_global_version_manager_by_title(xsd_filename)
    except exceptions.DoesNotExist:
        default_xsd_path = finders.find(xsd_filepath)
        xsd_data = read_file_content(default_xsd_path)
        registry_system_api.insert_registry_user_schema(xsd_filename, xsd_data)
    except Exception as e:
        logger.error("Impossible to add the template: {0}".format(str(e)))


def _init_xslt():
    """Init the XSLTs. Add XSLTs and the binding with the user template.

    Returns:

    """
    try:
        # Get or create template
        template_version_manager = (
            user_version_manager_api.get_default_version_manager()
        )
        # Get or create XSLTs
        list_xslt = _get_or_create_xslt(LIST_XSL_FILENAME)
        default_detail_xslt = _get_or_create_xslt(DETAIL_XSL_FILENAME)
        list_detail_xslt = [default_detail_xslt]
        # Create binding between template and XSLTs if does not exist
        _bind_template_xslt(
            template_version_manager[0].current,
            list_xslt,
            default_detail_xslt,
            list_detail_xslt,
        )
    except Exception as e:
        print("ERROR : Impossible to init the XSLTs. " + str(e))


def _get_or_create_xslt(filename):
    """Get or create an xslt.

    Args:
        filename: XSLT filename.

    Returns:
        XSLT.

    """
    try:
        return xslt_transformation_api.get_by_name(filename)
    except exceptions.ApiError:
        # Get XSLT.
        list_xslt_path = finders.find(join(XSL_FOLDER_PATH, filename))
        # Read content.
        list_xsl_data = read_file_content(list_xslt_path)
        # Create the XSLT.
        list_xslt = XslTransformation(
            name=filename, filename=filename, content=list_xsl_data
        )
        return xslt_transformation_api.upsert(list_xslt)
    except Exception as e:
        raise Exception(
            "Impossible to add the xslt {0} : {1} ".format(filename, str(e))
        )


def _bind_template_xslt(template_id, list_xslt, default_detail_xslt, list_detail_xslt):
    """Bind the registry template with the XSLTs.

    Args:
        template_id: Registry template id.
        list_xslt: List XSLT.
        default_detail_xslt: Detail XSLT.
        list_detail_xslt:

    Returns:

    """
    from core_main_app.components.template_xsl_rendering import (
        api as template_xsl_rendering_api,
    )

    try:
        template_xsl_rendering_api.get_by_template_id(template_id)
    except exceptions.DoesNotExist:
        template_xsl_rendering_api.add_or_delete(
            template_id=template_id,
            list_xslt=list_xslt,
            default_detail_xslt=default_detail_xslt,
            list_detail_xslt=list_detail_xslt,
        )
    except Exception as e:
        raise Exception("Impossible to bind the template with XSLTs : " + str(e))


def _init_periodic_tasks():
    """Create periodic tasks for the app and add them to a crontab schedule"""
    schedule, _ = CrontabSchedule.objects.get_or_create(
        minute="*",
    )
    try:
        PeriodicTask.objects.get(name=delete_user_data_structure.__name__)
    except ObjectDoesNotExist:
        PeriodicTask.objects.create(
            crontab=schedule,
            name=delete_user_data_structure.__name__,
            task="core_user_registration_app.tasks.delete_user_data_structure",
        )
