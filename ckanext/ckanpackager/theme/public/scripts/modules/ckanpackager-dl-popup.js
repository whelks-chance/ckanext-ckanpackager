"use strict";

/* example_theme_popover
 *
 * This JavaScript module adds a Bootstrap popover with some extra info about a
 * dataset to the HTML element that the module is applied to. Users can click
 * on the HTML element to show the popover.
 *
 * title - the title of the dataset
 * license - the title of the dataset's copyright license
 * num_resources - the number of resources that the dataset has.
 *
 */
ckan.module('ckanpackager-dl-popup', function(jQuery, _) {

    function build_popup(module) {
        var self = {};
        self.el = module.el;
        self.sandbox = module.sandbox;

        self.options = {
            title: module.options.title,
            num_resources: module.options.num_resources,
            license: module.options.license
        };

        self.initialize = function() {
            jQuery.proxyAll(this, /_on/);
            // disable the button for now, we'll enable it once we get the template from the server
            self.disableButton();
            // request the template from the server, this is async
            // var template_options = {resource_id: self.options.resource_id, is_record: self.options.is_record};
            // self.sandbox.client.getTemplate('ckanpackager_post_form.html', template_options, self._onReceiveSnippet);
        };

        // Add an event handler to the button, when the user clicks the button
        // our _onClick() function will be called.
        self.el.on('click', function(){
            // Send an ajax request to CKAN to render the popover.html snippet.
            // We wrap this in an if statement because we only want to request
            // the snippet from CKAN once, not every time the button is clicked.
            if (!self._snippetReceived) {

                self.sandbox.client.getTemplate('eula_text.html',
                    self.options,
                    self._onReceiveSnippet);
                self._snippetReceived = true;
            }
            self.el[0].scrollIntoView();
        });

        // Access some options passed to this JavaScript module by the calling
        // template.
        var num_resources = self.options.num_resources;
        var license = self.options.license;

        // Format a simple string with the number of resources and the license,
        // e.g. "3 resources, Open Data Commons Attribution License".
        var content = 'NUM resources, LICENSE'
            .replace('NUM', self.options.num_resources)
            .replace('LICENSE', self.options.license);

        // Add a Bootstrap popover to the HTML element (this.el) that this
        // JavaScript module was initialized on.
        self.el.popover({
            title: self.options.title, html: true,
            content: 'Loading...', placement: 'left'
        });

        // Whether or not the rendered snippet has already been received from CKAN.
        self._snippetReceived = false;


        // CKAN calls this function when it has rendered the snippet, and passes
        // it the rendered HTML.
        self._onReceiveSnippet = function(html) {
console.log('got snippet', html);
            // Replace the popover with a new one that has the rendered HTML from the
            // snippet as its contents.
            self.el.popover('destroy');
            self.el.popover({title: self.options.title, html: true,
                content: html, placement: 'right'});
            self.el.popover('show');
        }

    }


    return {
        initialize: function () {

            console.log("I've been initialized for element: ", this.el);
            console.log("Sandbox: ", this.sandbox);


            return build_popup(this);
        }
    }
});