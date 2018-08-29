'use strict'

this.ckan.module('ckanpackager-dl-package', function(jQuery, _){

    var self = init_self();
    
    function create_all_checkbox(module) {

        console.log("ckanpackager-dl-package.create_all_checkbox()");

        module.el.change(function() {
            if(this.checked) {
                // click if unclicked
                jQuery('.package_checkbox').each(
                    function(i){
                        if (jQuery(this).prop("checked") == false) {
                            jQuery(this).click();
                        }
                    }
                )
            } else {
                // unclick if clicked
                jQuery('.package_checkbox').each(
                    function(i){
                        if (jQuery(this).prop("checked") == true) {
                            jQuery(this).click();
                        }                    }
                )
            }
        });
    }

    function create_checkboxes(module) {

        module.el.prop("checked", false);

        var dl_list = self.get_data('download_package_list');
        console.log(dl_list);
        if (dl_list === null){
            dl_list = [];
        } else {
            dl_list = JSON.parse(dl_list);
        }

        console.log(dl_list.length);

        for (var d in dl_list) {
            if (module.options.packageId === dl_list[d]) {
                module.el.prop("checked", true);
            }
        }

        module.el.change(function() {
            if(this.checked) {
                console.log(module.options.packageId + ' checked');
                update_storage(module.options.packageId, true)
            } else {
                update_storage(module.options.packageId, false);
                console.log(module.options.packageId + ' unchecked');

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

        var dl_list = self.get_data('download_package_list');

        if (dl_list === null){
            dl_list = [];
            console.log('download_package_list init');
        } else {
            dl_list = JSON.parse(dl_list);
            console.log('parse download_package_list');
        }


        if(add){
            dl_list.push(id);
        } else {
            remove(dl_list, id);
        }
        console.log(dl_list);

        self.store_data('download_package_list', JSON.stringify(dl_list));

    }

    return {
        initialize: function(){
            // console.log("I've been initialized for element: ", this.el);
            console.log("I've got options: ", this.options);
            // console.log(this.sandbox.jQuery);


            if(this.options.checkType == "all"){
                return create_all_checkbox(this);
            } else {
                return create_checkboxes(this);
            }

        }
    }
});
