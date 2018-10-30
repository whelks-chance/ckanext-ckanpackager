import json
import logging
import urllib
import urllib2
import paste.fileapp

import ckan.logic as logic
from ckan.lib import base
from ckan.lib.helpers import flash_success, flash_error, redirect_to
import ckan.plugins.toolkit as t
from ckan.common import OrderedDict, _, json, request, c, response

import ckan.model as model
from ckanext.ckanpackager.plugin import config
import ckan.lib.uploader as uploader

from ckanext.ckanpackager.model.DownloadQueue import DLQueue

NotFound = logic.NotFound
NotAuthorized = logic.NotAuthorized
ValidationError = logic.ValidationError
get_action = logic.get_action
abort = base.abort

_ = t._
log = logging.getLogger()


class PackageListControllerError(Exception):
    """Exception raised on internal errors (not propagated)"""
    pass


class PackageListController(t.BaseController):
    def queue_resource_list(self):
        log.info(t.request.__dict__)

        """Action called to package a resource

                @param package_id: The package id
                @param resource_id: The resource id
                """
        try:
            # self._setup_request(package_id=package_id, resource_id=resource_id)
            self._validate_request()

            if t.c.user:
                email = t.c.userobj.email
            else:
                email = t.request.params['email']

            packager_url, request_params = self._prepare_packager_parameters(email, t.request.params)

            # # cycle through any implementors
            # for plugin in PluginImplementations(ICkanPackager):
            #     packager_url, request_params = plugin.before_package_request(resource_id, package_id, packager_url,
            #                                                                  request_params)

            result = self._send_packager_request(packager_url, request_params)
            if 'message' in result:
                flash_success(result['message'])
            else:
                flash_success(_("Request successfully posted. The resource should be emailed to you shortly"))
        except PackageListControllerError as e:
            flash_error(e.message)
        else:
            # TODO record progress
            # Create new download object
            # stat = DLQueue(
            #     user=t.c.user.id
            # )
            # model.Session.add(stat)
            # model.Session.commit()
            pass

        if 'destination' in t.request.params:
            self.destination = t.request.params['destination']
        else:
            self.destination = '/'

        redirect_to(self.destination)

    def _prepare_packager_parameters(self, email, params):
        """Prepare the parameters for the ckanpackager service for the current request

        @param resource_id: The resource id
        @param params: A dictionary of parameters
        @return: A tuple defining an URL and a dictionary of parameters
        """

        print(type(params))
        print(params)

        packager_url = config['url']
        request_params = {
            'secret': config['secret'],
            'email': email,
            # default to csv format, this can be overridden in the params
            'format': u'csv',
        }
        context = {'model': model, 'session': model.Session,
                   'user': t.c.user, 'auth_user_obj': t.c.userobj}

        # TODO check this makes sense...
        request_params['download_payload'] = params['download_payload']

        download_payload = json.loads(params['download_payload'])

        resource_file_paths = []

        for resource_id in download_payload['download_list']:
            if resource_id:
                print '\n\n', resource_id
                try:
                    rsc = get_action('resource_show')(context, {'id': resource_id})
                    # get_action('package_show')(context, {'id': id})

                    if rsc.get('url_type') == 'upload':
                        upload = uploader.get_resource_uploader(rsc)
                        filepath = upload.get_path(rsc['id'])

                        print filepath

                        resource_file_paths.append({
                            'name': rsc['url'].split('/')[-1],
                            'file_path': filepath,
                            'size': rsc['size']
                        })

                        fileapp = paste.fileapp.FileApp(filepath)
                        try:
                            status, headers, app_iter = request.call_application(fileapp)
                        except OSError:
                            pass

                            #     abort(404, _('Resource data not found'))
                            # response.headers.update(dict(headers))
                            # content_type, content_enc = mimetypes.guess_type(
                            #     rsc.get('url', ''))
                            # if content_type:
                            #     response.headers['Content-Type'] = content_type
                            # response.status = status
                            # return app_iter
                    elif 'url' not in rsc:
                        pass
                        # abort(404, _('No download is available'))

                except (NotFound, NotAuthorized):
                    pass

        request_params['file_paths'] = json.dumps({
            'paths': resource_file_paths
        })
        packager_url += '/package_url'

        return packager_url, request_params

    def _send_packager_request(self, packager_url, request_params):
        """Send the request to the ckanpackager service

        @param packager_url: The ckanpackager service URL
        @request_params: The parameters to send
        """

        # Send request
        try:
            request = urllib2.Request(packager_url)
            response = urllib2.urlopen(request, urllib.urlencode(request_params))
        except urllib2.URLError as e:
            print(e)

            raise PackageListControllerError(_("Failed to contact the ckanpackager service"))
        if response.code != 200:
            response.close()

            print(response.__dict__)
            raise PackageListControllerError(_("Failed to contact the ckanpackager service - or it returned an error"))

        # Read response and return.
        try:
            data = response.read()
            result = json.loads(data)
        except ValueError:
            raise PackageListControllerError(_("Could not parse response from ckanpackager service"))
        finally:
            response.close()
        return result

    def _validate_request(self):
        """Validate the current request, and raise exceptions on errors"""
        # Validate resource
        # try:
        #     if not is_downloadable_resource(self.resource_id):
        #         raise PackagerControllerError(_("This resource cannot be downloaded"))
        # except t.ObjectNotFound:
        #     raise PackagerControllerError("Resource not found")
        #
        # # Validate anonymous access and email parameters
        # if 'anon' in t.request.params:
        #     raise PackagerControllerError(_("You must be logged on or have javascript enabled to use this functionality."))
        # if t.c.user and 'email' in t.request.params:
        #     raise PackagerControllerError(_("Parameter mismatch. Please reload the page and try again."))
        # if not t.c.user and 'email' not in t.request.params:
        #     raise PackagerControllerError(_("Please reload the page and try again."))
