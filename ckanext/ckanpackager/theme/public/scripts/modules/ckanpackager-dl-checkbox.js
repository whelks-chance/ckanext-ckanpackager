'use strict'

this.ckan.module('ckanpackager-dl-checkbox', function(jQuery, _){

    var self = init_self();


    function create_checkboxes(module) {

        console.log("ckanpackager-dl-checkbox.create_checkboxes()");


        module.el.prop("checked", false);

        var dl_list = self.get_data('download_list');
        console.log(dl_list);
        if (dl_list === null){
            dl_list = [];
        } else {
            dl_list = JSON.parse(dl_list);
        }

        console.log(dl_list.length);

        for (var d in dl_list) {
            if (module.options.resourceId === dl_list[d]) {
                module.el.prop("checked", true);
            }
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
            // console.log("I've been initialized for element: ", this.el);
            // console.log("I've got options: ", this.options);
            // console.log(this.sandbox.jQuery);

            return create_checkboxes(this);
        }
    }
});
