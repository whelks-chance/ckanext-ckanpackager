import ckan.plugins.toolkit as t


class CkanPackagerController(t.BaseController):

    def show_resource(self, package_id, resource_id):
        t.redirect_to(
            t.url_for(controller='package',
                      action='resource_read',
                      id=package_id,
                      resource_id=resource_id)
        )

