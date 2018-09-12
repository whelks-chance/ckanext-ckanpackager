# encoding: utf-8

from logging import getLogger
from ckan.common import json
import ckan.plugins as p
import ckan.plugins.toolkit as toolkit
import ckanext.resourceproxy.plugin as proxy

default = toolkit.get_validator(u'default')
boolean_validator = toolkit.get_validator(u'boolean_validator')
ignore_missing = toolkit.get_validator(u'ignore_missing')


class FileTreeViewPlugin(p.SingletonPlugin):
    '''
    DataTables file tree view plugin
    '''
    p.implements(p.IConfigurer, inherit=True)
    p.implements(p.IResourceView, inherit=True)
    # p.implements(p.IRoutes, inherit=True)

    def update_config(self, config):
        '''
        Set up the resource library, public directory and
        template directory for the view
        '''
        toolkit.add_template_directory(config, u'templates')
        toolkit.add_resource(u'public', u'ckanext-filetreeview')

    def can_view(self, data_dict):
        return True
        # resource = data_dict['resource']
        # return resource.get(u'datastore_active')

    def view_template(self, context, data_dict):
        print(context)
        print(data_dict)
        return u'filetreeview/filetreeview.html'

    def form_template(self, context, data_dict):
        return u'filetreeview/filetreeview_form.html'

    def setup_template_variables(self, context, data_dict):
        # metadata = {'text_formats': self.text_formats,
        #             'json_formats': self.json_formats,
        #             'jsonp_formats': self.jsonp_formats,
        #             'xml_formats': self.xml_formats}

        url = proxy.get_proxified_resource_url(data_dict)

        return {
            # 'preview_metadata': json.dumps(metadata),
            'resource_json': json.dumps(data_dict['resource']),
            'resource_url': json.dumps(url)
        }

    def info(self):
        return {
            u'name': u'filetree_view',
            u'title': u'File Tree',
            u'filterable': True,
            u'icon': u'table',
            u'requires_datastore': False,
            u'default_title': p.toolkit._(u'Table'),
            u'schema': {
                u'responsive': [default(False), boolean_validator],
                u'show_fields': [ignore_missing],
                u'filterable': [default(True), boolean_validator],
            }
        }
    #
    # def before_map(self, m):
    #     m.connect(
    #         u'/datatables/ajax/{resource_view_id}',
    #         controller=u'ckanext.datatablesview.controller'
    #                    u':DataTablesController',
    #         action=u'ajax')
    #     return m
