"""
User Version Manager API
"""
from core_main_app.access_control.api import is_superuser
from core_main_app.access_control.decorators import access_control
from core_main_app.commons import exceptions
from core_main_app.components.template import api as template_api
from core_main_app.components.template.access_control import can_read, can_read_global
from core_main_app.components.version_manager import api as version_manager_api
from core_main_app.components.version_manager.utils import (
    get_latest_version_name,
)
from core_user_registration_app.components.user_template_version_manager.access_control import (
    can_write,
)
from core_user_registration_app.components.user_template_version_manager.models import (
    UserTemplateVersionManager,
)


@access_control(can_write)
def insert(user_version_manager, template, request):
    """Add a version to a user template version manager.

    Args:
        user_version_manager:
        template:
        request:

    Returns:

    """
    # save the template in database
    template_api.upsert(template, request=request)
    try:
        # insert the initial template in the version manager
        version_manager_api.insert_version(
            user_version_manager, template, request=request
        )
        # insert the version manager in database
        version_manager_api.upsert(user_version_manager, request=request)
        # get template display name
        display_name = get_latest_version_name(user_version_manager)
        # update saved template
        template_api.set_display_name(template, display_name, request=request)
        # return version manager
        return user_version_manager
    except Exception as e:
        template_api.delete(template, request=request)
        raise e


@access_control(can_read_global)
def get_global_version_managers(request, _cls=True):
    """Get all global version managers of a template.

    Args:
        request:
        _cls:

    Returns:

    """
    return UserTemplateVersionManager.get_global_version_managers(_cls)


def get_version_manager_by_id(id):
    """Return Version manager with given version manager id

    :param id:
    :return:
    """
    return UserTemplateVersionManager.get_by_id(id)


@access_control(can_read)
def get_from_version(version, request):
    """Return a version manager from a version.

    Args:
        version:
        request:

    Returns:

    """
    user_version_managers = UserTemplateVersionManager.get_all()
    for user_version_manager in user_version_managers:
        if str(version.id) in user_version_manager.versions:
            return user_version_manager
    raise exceptions.ApiError("No version manager could be found for this version.")


@access_control(can_write)
def set_current(version, request):
    """Set the current version of the object, then saves it.

    Args:
        version:
        request:

    Returns:

    """
    user_version_manager = get_from_version(version, request=request)

    # a disabled version cannot be current
    if str(version.id) in user_version_manager.get_disabled_versions():
        raise exceptions.ApiError(
            "Unable to set the current version because it is disabled."
        )

    user_version_manager.set_current_version(version)
    return upsert(user_version_manager, request=request)


@access_control(is_superuser)
def get_all(request, _cls=True):
    """Return all Template Version Managers.

    Returns:

    """
    return UserTemplateVersionManager.get_all_version_manager(_cls)


def get_default_version_manager():
    """Return default User Version Manager.

    Returns:

    """
    return UserTemplateVersionManager.objects(is_default=True)


@access_control(can_write)
def upsert(user_version_manager, request):
    """Save or update user_version manager.

    Args:
        user_version_manager:
        request:

    Returns:

    """
    return user_version_manager.save_version_manager()


def set_default_version_manager(user_version_manager, request):
    """Set default version manager.

    Args:
        user_version_manager:
        request:

    Returns:

    """
    default_user_version_manager = (
        UserTemplateVersionManager.get_default_version_manager()
    )
    for version_manager in default_user_version_manager:
        version_manager.is_default = False
        version_manager.save_version_manager()
    user_version_manager = get_version_manager_by_id(user_version_manager)
    user_version_manager.is_default = True
    user_version_manager.save_version_manager()

    return user_version_manager
