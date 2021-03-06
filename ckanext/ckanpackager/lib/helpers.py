from ckan.logic import get_action


def should_show_format_options(resource_id):
    """
    Determines whether the format options should be shown for a given resource id.
    :param resource_id: the resource's id
    :return: True if they should be shown, False if not
    """
    resource = get_action('resource_show')({}, dict(id=resource_id))
    # currently we just predicate on whether the resource is in the datastore or not
    return resource.get('datastore_active', False)
