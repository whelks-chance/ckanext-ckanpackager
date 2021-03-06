'use strict'

this.ckan.module('ckanpackager-dl-checkbox', function(jQuery, _){

    var self = init_self();


    function create_checkboxes(module) {

        module.el.prop("checked", false);

        var dl_package_list = self.get_data('download_package_list');
        console.log(dl_package_list);
        if (dl_package_list === null){
            dl_package_list = [];
        } else {
            dl_package_list = JSON.parse(dl_package_list);
        }
        console.log('dl_package_list', dl_package_list.length, dl_package_list);

        var dl_list = self.get_data('download_list');
        console.log(dl_list);
        if (dl_list === null){
            dl_list = [];
        } else {
            dl_list = JSON.parse(dl_list);
        }
        console.log('dl_list', dl_list.length, dl_list);

        for (var d in dl_list) {
            if (module.options.resourceId === dl_list[d]) {
                module.el.prop("checked", true);
            }
        }

        // If whole dataset is selected, ignore the resource selected status
        // TODO less brute force
        if ( dl_package_list.indexOf(module.options.packageId) != -1) {
            module.el.prop("checked", true);
        }

        module.el.change(function() {
            if(this.checked) {
                console.log(module.options.resourceId + ' checked');
                update_storage(module.options.resourceId, true)
            } else {
                update_storage(module.options.resourceId, false);
                console.log(module.options.resourceId + ' unchecked');

            }
        });
    }

    function remove(array, id) {
        var index = array.indexOf(id);
        if (index > -1) {
            array.splice(index, 1);
        }
        return array
    }

    function update_storage(id, add){
        // if add == false, remove it

        var dl_list = self.get_data('download_list');

        if (dl_list === null){
            dl_list = [];
            console.log('dl_list init');
        } else {
            dl_list = JSON.parse(dl_list);
            console.log('parse dl_list');
        }


        if(add){
            dl_list.push(id);
        } else {
            remove(dl_list, id);
        }
        console.log(dl_list);

        self.store_data('download_list', JSON.stringify(dl_list));

    }

    return {
        initialize: function(){
            console.log("I've been initialized for element: ", this.el);
            console.log("I've got options: ", this.options);
            console.log(this.sandbox.jQuery);

            return create_checkboxes(this);
        }
    }
});
