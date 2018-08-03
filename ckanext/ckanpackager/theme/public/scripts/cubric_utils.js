function init_self(){

    var self = {
        store_data: setCookie,
        get_data: getCookie,
        erase_data: eraseCookie
    };

    self.use_local_storage = true;

    if (self.use_local_storage) {
        self.store_data = store_data_localStorage;
        self.get_data = get_data_localStorage;
        self.erase_data = erase_data_localStorage;
    }
    return jQuery.extend(true, {}, self);

}

function store_data_localStorage(key, value) {
    return localStorage.setItem(key, value)
}

function get_data_localStorage(key) {
    return localStorage.getItem(key)
}

function erase_data_localStorage(key) {
    localStorage.removeItem(key)
}


// https://stackoverflow.com/a/24103596
function setCookie(name, value, days) {
    var expires = "";
    if (days) {
        var date = new Date();
        date.setTime(date.getTime() + (days*24*60*60*1000));
        expires = "; expires=" + date.toUTCString();
    }
    document.cookie = name + "=" + (value || "")  + expires + "; path=/";
}

function getCookie(name) {
    var nameEQ = name + "=";
    var ca = document.cookie.split(';');
    for(var i=0;i < ca.length;i++) {
        var c = ca[i];
        while (c.charAt(0)==' ') c = c.substring(1,c.length);
        if (c.indexOf(nameEQ) == 0) return c.substring(nameEQ.length,c.length);
    }
    return null;
}

function eraseCookie(name) {
    document.cookie = name+'=; Max-Age=-99999999;';
}