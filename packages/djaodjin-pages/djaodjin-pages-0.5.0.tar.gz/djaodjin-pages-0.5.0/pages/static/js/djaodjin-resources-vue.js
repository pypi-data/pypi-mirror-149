/* Generic mixins for Vue.js */

(function (root, factory) {
    if (typeof define === 'function' && define.amd) {
        // AMD. Register as an anonymous module.
        define(['exports', 'jQuery'], factory);
    } else if (typeof exports === 'object' && typeof exports.nodeName !== 'string') {
        // CommonJS
        factory(exports, require('jQuery'));
    } else {
        // Browser true globals added to `window`.
        factory(root, root.jQuery);
        // If we want to put the exports in a namespace, use the following line
        // instead.
        // factory((root.djResources = {}), root.jQuery);
    }
}(typeof self !== 'undefined' ? self : this, function (exports, jQuery) {


/** Formats a date shown to the user.
*/
const DATE_FORMAT = 'MMM DD, YYYY';
const DESC_SORT_PRE = '-';


/** Displays notification messages to the user

     requires `jQuery`, _showErrorMessagesProviderNotified
     optional toastr
 */
var messagesMixin = {
    data: function() {
        return {
            messagesElement: '#messages-content',
        }
    },
    methods: {
        /**
           Decorates elements when details exist, otherwise return messages
           to be shown globally.

           This method takes a `resp` argument as passed by jQuery ajax calls.
        */
        _showErrorMessages: function (resp) {
            var vm = this;
            var messages = [];
            if( typeof resp === "string" ) {
                messages = [resp];
            } else {
                var data = resp.data || resp.responseJSON;
                if( data && typeof data === "object" ) {
                    if( data.detail ) {
                        messages = [data.detail];
                    } else if( jQuery.isArray(data) ) {
                        for( var idx = 0; idx < data.length; ++idx ) {
                            messages = messages.concat(vm._showErrorMessages(data[idx]));
                        }
                    } else {
                        for( var key in data ) {
                            if (data.hasOwnProperty(key)) {
                                var message = data[key];
                                if( jQuery.isArray(data[key]) ) {
                                    message = "";
                                    var sep = "";
                                    for( var i = 0; i < data[key].length; ++i ) {
                                        var messagePart = data[key][i];
                                        if( typeof data[key][i] !== 'string' ) {
                                            messagePart = JSON.stringify(data[key][i]);
                                        }
                                        message += sep + messagePart;
                                        sep = ", ";
                                    }
                                } else if( data[key].hasOwnProperty('detail') ) {
                                    message = data[key].detail;
                                }
                                messages.push(key + ": " + message);
                                var inputField = jQuery("[name=\"" + key + "\"]");
                                var parent = inputField.parents('.form-group');
                                inputField.addClass("is-invalid");
                                parent.addClass("has-error");
                                var help = parent.find('.invalid-feedback');
                                if( help.length > 0 ) { help.text(message); }
                            }
                        }
                    }
                } else if( resp.detail ) {
                    messages = [resp.detail];
                }
            }
            return messages;
        },
        clearMessages: function() {
            var vm = this;
            jQuery(vm.messagesElement).empty();
        },
        showMessages: function (messages, style) {
            var vm = this;
            if( typeof toastr !== 'undefined'
                && $(toastr.options.containerId).length > 0 ) {
                for( var i = 0; i < messages.length; ++i ) {
                    toastr[style](messages[i]);
                }
            } else {
                var messageBlock = "<div class=\"alert alert-block";
                if( style ) {
                    if( style === "error" ) {
                        style = "danger";
                    }
                    messageBlock += " alert-" + style;
                }
                messageBlock += "\"><button type=\"button\" class=\"close\" data-dismiss=\"alert\">&times;</button>";

                if( typeof messages === "string" ) {
                    messages = [messages];
                }
                for( var i = 0; i < messages.length; ++i ) {
                    messageBlock += "<div>" + messages[i] + "</div>";
                }
                messageBlock += "</div>";
                jQuery(vm.messagesElement).append(messageBlock);
            }
            jQuery("#messages").removeClass("hidden");
            jQuery("html, body").animate({
                // scrollTop: $("#messages").offset().top - 50
                // avoid weird animation when messages at the top:
                scrollTop: jQuery("body").offset().top
            }, 500);
        },
        showErrorMessages: function (resp) {
            var vm = this;
            if( resp.status >= 500 && resp.status < 600 ) {
                msg = "Err " + resp.status + ": " + resp.statusText;
                if( _showErrorMessagesProviderNotified ) {
                    msg += "<br />" + _showErrorMessagesProviderNotified;
                }
                messages = [msg];
            } else {
                var messages = vm._showErrorMessages(resp);
                if( messages.length === 0 ) {
                    messages = ["Err " + resp.status + ": " + resp.statusText];
                }
            }
            vm.showMessages(messages, "error");
        },
    }
};

/** A wrapper around jQuery ajax functions that adds authentication
    parameters as necessary.

    requires `jQuery`
*/
var httpRequestMixin = {
    mixins: [
        messagesMixin
    ],
    // basically a wrapper around jQuery ajax functions
    methods: {

        _isArray: function (obj) {
            return obj instanceof Object && obj.constructor === Array;
        },

        _isFunction: function (func){
            // https://stackoverflow.com/a/7356528/1491475
            return func && {}.toString.call(func) === '[object Function]';
        },

        _isObject: function (obj) {
            // https://stackoverflow.com/a/46663081/1491475
            return obj instanceof Object && obj.constructor === Object;
        },

        _getAuthToken: function() {
            return null; // XXX NotYetImplemented
        },

        _csrfSafeMethod: function(method) {
            // these HTTP methods do not require CSRF protection
            return (/^(GET|HEAD|OPTIONS|TRACE)$/.test(method));
        },

        _getCSRFToken: function() {
            var vm = this;
            // Look first for an input node in the HTML page, i.e.
            // <input type="hidden" name="csrfmiddlewaretoken"
            //     value="{{csrf_token}}">
            var crsfNode = vm.$el.querySelector("[name='csrfmiddlewaretoken']");
            if( crsfNode ) {
                return crsfNode.value;
            }
            // Then look for a CSRF token in the meta tags, i.e.
            // <meta name="csrf-token" content="{{csrf_token}}">
            var metas = document.getElementsByTagName('meta');
            for( var i = 0; i < metas.length; i++) {
                if (metas[i].getAttribute("name") == "csrf-token") {
                    return metas[i].getAttribute("content");
                }
            }
            return "";
        },

        _safeUrl: function(base, path) {
            if( !path ) return base;

            if( base && base[base.length - 1] == '/') {
                if( path && path[0] == '/') {
                    return base + path.substring(1);
                }
                return base + path;
            }
            if( path && path[0] == '/') {
                return base + path;
            }
            return base + '/' + path;
        },

        /** This method generates a GET HTTP request to `url` with a query
            string built of a `queryParams` dictionnary.

            It supports the following prototypes:

            - reqGet(url, successCallback)
            - reqGet(url, queryParams, successCallback)
            - reqGet(url, queryParams, successCallback, failureCallback)
            - reqGet(url, successCallback, failureCallback)

            `queryParams` when it is specified is a dictionnary
            of (key, value) pairs that is converted to an HTTP
            query string.

            `successCallback` and `failureCallback` must be Javascript
            functions (i.e. instance of type `Function`).
        */
        reqGet: function(url, arg, arg2, arg3){
            var vm = this;
            var queryParams, successCallback;
            var failureCallback = vm.showErrorMessages;
            if(typeof url != 'string') throw 'url should be a string';
            if(vm._isFunction(arg)){
                // We are parsing reqGet(url, successCallback)
                // or reqGet(url, successCallback, errorCallback).
                successCallback = arg;
                if(vm._isFunction(arg2)){
                    // We are parsing reqGet(url, successCallback, errorCallback)
                    failureCallback = arg2;
                } else if( arg2 !== undefined ) {
                    throw 'arg2 should be a failureCallback function';
                }
            } else if(vm._isObject(arg)){
                // We are parsing
                // reqGet(url, queryParams, successCallback)
                // or reqGet(url, queryParams, successCallback, errorCallback).
                queryParams = arg;
                if(vm._isFunction(arg2)){
                    // We are parsing reqGet(url, queryParams, successCallback)
                    // or reqGet(url, queryParams, successCallback, errorCallback).
                    successCallback = arg2;
                    if(vm._isFunction(arg3)){
                        // We are parsing reqGet(url, queryParams, successCallback, errorCallback)
                        failureCallback = arg3;
                    } else if( arg3 !== undefined ){
                        throw 'arg3 should be a failureCallback function';
                    }
                } else {
                    throw 'arg2 should be a successCallback function';
                }
            } else {
                throw 'arg should be a queryParams Object or a successCallback function';
            }
            return jQuery.ajax({
                method: 'GET',
                url: url,
                beforeSend: function(xhr, settings) {
                    var authToken = vm._getAuthToken();
                    if( authToken ) {
                        xhr.setRequestHeader("Authorization",
                            "Bearer " + authToken);
                    } else {
                        if( !vm._csrfSafeMethod(settings.type) ) {
                            var csrfToken = vm._getCSRFToken();
                            if( csrfToken ) {
                                xhr.setRequestHeader("X-CSRFToken", csrfToken);
                            }
                        }
                    }
                },
                data: queryParams,
                traditional: true,
                cache: false,       // force requested pages not to be cached
           }).done(successCallback).fail(failureCallback);
        },

        /** This method generates a POST HTTP request to `url` with
            contentType 'application/json'.

            It supports the following prototypes:

            - reqPOST(url, data)
            - reqPOST(url, data, successCallback)
            - reqPOST(url, data, successCallback, failureCallback)
            - reqPOST(url, successCallback)
            - reqPOST(url, successCallback, failureCallback)

            `data` when it is specified is a dictionnary of (key, value) pairs
            that is passed as a JSON encoded body.

            `successCallback` and `failureCallback` must be Javascript
            functions (i.e. instance of type `Function`).
        */
        reqPost: function(url, arg, arg2, arg3){
            var vm = this;
            var data, successCallback;
            var failureCallback = vm.showErrorMessages;
            if(typeof url != 'string') throw 'url should be a string';
            if(vm._isFunction(arg)){
                // We are parsing reqPost(url, successCallback)
                // or reqPost(url, successCallback, errorCallback).
                successCallback = arg;
                if(vm._isFunction(arg2)){
                    // We are parsing reqPost(url, successCallback, errorCallback)
                    failureCallback = arg2;
                } else if (arg2 !== undefined){
                    throw 'arg2 should be a failureCallback function';
                }
            } else if( vm._isObject(arg) || vm._isArray(arg) ) {
                // We are parsing reqPost(url, data)
                // or reqPost(url, data, successCallback)
                // or reqPost(url, data, successCallback, errorCallback).
                data = arg;
                if(vm._isFunction(arg2)){
                    // We are parsing reqPost(url, data, successCallback)
                    // or reqPost(url, data, successCallback, errorCallback).
                    successCallback = arg2;
                    if(vm._isFunction(arg3)){
                        // We are parsing reqPost(url, data, successCallback, errorCallback)
                        failureCallback = arg3;
                    } else if (arg3 !== undefined){
                        throw 'arg3 should be a failureCallback function';
                    }
                } else if (arg2 !== undefined){
                    throw 'arg2 should be a successCallback function';
                }
            } else if (arg !== undefined){
                throw 'arg should be a data Object or a successCallback function';
            }
            return jQuery.ajax({
                method: 'POST',
                url: url,
                beforeSend: function(xhr, settings) {
                    var authToken = vm._getAuthToken();
                    if( authToken ) {
                        xhr.setRequestHeader("Authorization",
                            "Bearer " + authToken);
                    } else {
                        if( !vm._csrfSafeMethod(settings.type) ) {
                            var csrfToken = vm._getCSRFToken();
                            if( csrfToken ) {
                                xhr.setRequestHeader("X-CSRFToken", csrfToken);
                            }
                        }
                    }
                },
                contentType: 'application/json',
                data: JSON.stringify(data),
            }).done(successCallback).fail(failureCallback);
        },

        /** This method generates a POST HTTP request to `url` with
            data encoded as multipart/form-data.

            It supports the following prototypes:

            - reqPOSTBlob(url, data)
            - reqPOSTBlob(url, data, successCallback)
            - reqPOSTBlob(url, data, successCallback, failureCallback)

            `data` is a `FormData` that holds a binary blob.

            `successCallback` and `failureCallback` must be Javascript
            functions (i.e. instance of type `Function`).
        */
        reqPostBlob: function(url, form, arg2, arg3) {
            var vm = this;
            var successCallback;
            var failureCallback = vm.showErrorMessages;
            if(typeof url != 'string') throw 'url should be a string';
            if(vm._isFunction(arg2)){
                // We are parsing reqPostBlob(url, successCallback)
                // or reqPostBlob(url, successCallback, errorCallback).
                successCallback = arg2;
                if(vm._isFunction(arg3)){
                    // We are parsing
                    // reqPostBlob(url, successCallback, errorCallback)
                    failureCallback = arg3;
                } else if( arg3 !== undefined ) {
                    throw 'arg3 should be a failureCallback function';
                }
            } else if( arg2 !== undefined ) {
                throw 'arg2 should be successCallback function';
            }
            return jQuery.ajax({
                method: 'POST',
                url: url,
                beforeSend: function(xhr, settings) {
                    var authToken = vm._getAuthToken();
                    if( authToken ) {
                        xhr.setRequestHeader("Authorization",
                            "Bearer " + authToken);
                    } else {
                        if( !vm._csrfSafeMethod(settings.type) ) {
                            var csrfToken = vm._getCSRFToken();
                            if( csrfToken ) {
                                xhr.setRequestHeader("X-CSRFToken", csrfToken);
                            }
                        }
                    }
                },
                contentType: false,
                processData: false,
                data: form,
            }).done(successCallback).fail(failureCallback);
        },

        /** This method generates a PUT HTTP request to `url` with
            contentType 'application/json'.

            It supports the following prototypes:

            - reqPUT(url, data)
            - reqPUT(url, data, successCallback)
            - reqPUT(url, data, successCallback, failureCallback)
            - reqPUT(url, successCallback)
            - reqPUT(url, successCallback, failureCallback)

            `data` when it is specified is a dictionnary of (key, value) pairs
            that is passed as a JSON encoded body.

            `successCallback` and `failureCallback` must be Javascript
            functions (i.e. instance of type `Function`).
        */
        reqPut: function(url, arg, arg2, arg3){
            var vm = this;
            var data, successCallback;
            var failureCallback = vm.showErrorMessages;
            if(typeof url != 'string') throw 'url should be a string';
            if(vm._isFunction(arg)){
                // We are parsing reqPut(url, successCallback)
                // or reqPut(url, successCallback, errorCallback).
                successCallback = arg;
                if(vm._isFunction(arg2)){
                    // We are parsing reqPut(url, successCallback, errorCallback)
                    failureCallback = arg2;
                } else if (arg2 !== undefined){
                    throw 'arg2 should be a failureCallback function';
                }
            } else if(vm._isObject(arg)){
                // We are parsing reqPut(url, data)
                // or reqPut(url, data, successCallback)
                // or reqPut(url, data, successCallback, errorCallback).
                data = arg;
                if(vm._isFunction(arg2)){
                    // We are parsing reqPut(url, data, successCallback)
                    // or reqPut(url, data, successCallback, errorCallback).
                    successCallback = arg2;
                    if(vm._isFunction(arg3)){
                        // We are parsing reqPut(url, data, successCallback, errorCallback)
                        failureCallback = arg3;
                    } else if (arg3 !== undefined){
                        throw 'arg3 should be a failureCallback function';
                    }
                } else if (arg2 !== undefined){
                    throw 'arg2 should be a successCallback function';
                }
            } else if (arg !== undefined){
                throw 'arg should be a data Object or a successCallback function';
            }

            return jQuery.ajax({
                method: 'PUT',
                url: url,
                beforeSend: function(xhr, settings) {
                    var authToken = vm._getAuthToken();
                    if( authToken ) {
                        xhr.setRequestHeader("Authorization",
                            "Bearer " + authToken);
                    } else {
                        if( !vm._csrfSafeMethod(settings.type) ) {
                            var csrfToken = vm._getCSRFToken();
                            if( csrfToken ) {
                                xhr.setRequestHeader("X-CSRFToken", csrfToken);
                            }
                        }
                    }
                },
                contentType: 'application/json',
                data: JSON.stringify(data),
            }).done(successCallback).fail(failureCallback);
        },
        /** This method generates a PATCH HTTP request to `url` with
            contentType 'application/json'.

            It supports the following prototypes:

            - reqPATCH(url, data)
            - reqPATCH(url, data, successCallback)
            - reqPATCH(url, data, successCallback, failureCallback)
            - reqPATCH(url, successCallback)
            - reqPATCH(url, successCallback, failureCallback)

            `data` when it is specified is a dictionnary of (key, value) pairs
            that is passed as a JSON encoded body.

            `successCallback` and `failureCallback` must be Javascript
            functions (i.e. instance of type `Function`).
        */
        reqPatch: function(url, arg, arg2, arg3){
            var vm = this;
            var data, successCallback;
            var failureCallback = vm.showErrorMessages;
            if(typeof url != 'string') throw 'url should be a string';
            if(vm._isFunction(arg)){
                // We are parsing reqPatch(url, successCallback)
                // or reqPatch(url, successCallback, errorCallback).
                successCallback = arg;
                if(vm._isFunction(arg2)){
                    // We are parsing reqPatch(url, successCallback, errorCallback)
                    failureCallback = arg2;
                } else if (arg2 !== undefined){
                    throw 'arg2 should be a failureCallback function';
                }
            } else if(vm._isObject(arg)){
                // We are parsing reqPatch(url, data)
                // or reqPatch(url, data, successCallback)
                // or reqPatch(url, data, successCallback, errorCallback).
                data = arg;
                if(vm._isFunction(arg2)){
                    // We are parsing reqPatch(url, data, successCallback)
                    // or reqPatch(url, data, successCallback, errorCallback).
                    successCallback = arg2;
                    if(vm._isFunction(arg3)){
                        // We are parsing reqPatch(url, data, successCallback, errorCallback)
                        failureCallback = arg3;
                    } else if (arg3 !== undefined){
                        throw 'arg3 should be a failureCallback function';
                    }
                } else if (arg2 !== undefined){
                    throw 'arg2 should be a successCallback function';
                }
            } else if (arg !== undefined){
                throw 'arg should be a data Object or a successCallback function';
            }

            return jQuery.ajax({
                method: 'PATCH',
                url: url,
                beforeSend: function(xhr, settings) {
                    var authToken = vm._getAuthToken();
                    if( authToken ) {
                        xhr.setRequestHeader("Authorization",
                            "Bearer " + authToken);
                    } else {
                        if( !vm._csrfSafeMethod(settings.type) ) {
                            var csrfToken = vm._getCSRFToken();
                            if( csrfToken ) {
                                xhr.setRequestHeader("X-CSRFToken", csrfToken);
                            }
                        }
                    }
                },
                contentType: 'application/json',
                data: JSON.stringify(data),
            }).done(successCallback).fail(failureCallback);
        },
        /** This method generates a DELETE HTTP request to `url` with a query
            string built of a `queryParams` dictionnary.

            It supports the following prototypes:

            - reqDELETE(url)
            - reqDELETE(url, successCallback)
            - reqDELETE(url, successCallback, failureCallback)

            `successCallback` and `failureCallback` must be Javascript
            functions (i.e. instance of type `Function`).
        */
        reqDelete: function(url, arg, arg2){
            var vm = this;
            var successCallback;
            var failureCallback = vm.showErrorMessages;
            if(typeof url != 'string') throw 'url should be a string';
            if(vm._isFunction(arg)){
                // We are parsing reqDelete(url, successCallback)
                // or reqDelete(url, successCallback, errorCallback).
                successCallback = arg;
                if(vm._isFunction(arg2)){
                    // We are parsing reqDelete(url, successCallback, errorCallback)
                    failureCallback = arg2;
                } else if (arg2 !== undefined){
                    throw 'arg2 should be a failureCallback function';
                }
            } else if (arg !== undefined){
                throw 'arg should be a successCallback function';
            }

            return jQuery.ajax({
                method: 'DELETE',
                url: url,
                beforeSend: function(xhr, settings) {
                    var authToken = vm._getAuthToken();
                    if( authToken ) {
                        xhr.setRequestHeader("Authorization",
                            "Bearer " + authToken);
                    } else {
                        if( !vm._csrfSafeMethod(settings.type) ) {
                            var csrfToken = vm._getCSRFToken();
                            if( csrfToken ) {
                                xhr.setRequestHeader("X-CSRFToken", csrfToken);
                            }
                        }
                    }
                },
            }).done(successCallback).fail(failureCallback);
        },
        /** This method generates multiple queries, and execute
            success/failure callbacks when all have completed.

            It supports the following prototypes:

            - reqMultiple(queryArray)
            - reqMultiple(queryArray, successCallback)
            - reqMultiple(queryArray, successCallback, failureCallback)

            `successCallback` and `failureCallback` must be Javascript
            functions (i.e. instance of type `Function`).
        */
        reqMultiple: function(queryArray, successCallback, failureCallback) {
            var vm = this;
            var ajaxCalls = [];
            if( !successCallback ) {
                successCallback = function() {};
            }
            if( !failureCallback ) {
                failureCallback = vm.showErrorMessages;
            }
            for(var idx = 0; idx < queryArray.length; ++idx ) {
                ajaxCalls.push(function () {
                    return $.ajax({
                        method: queryArray[idx].method,
                        url: queryArray[idx].url,
                        data: JSON.stringify(queryArray[idx].data),
                        beforeSend: function(xhr, settings) {
                            var authToken = vm._getAuthToken();
                            if( authToken ) {
                                xhr.setRequestHeader("Authorization",
                                                     "Bearer " + authToken);
                            } else {
                                if( !vm._csrfSafeMethod(settings.type) ) {
                                    var csrfToken = vm._getCSRFToken();
                                    if( csrfToken ) {
                                        xhr.setRequestHeader("X-CSRFToken", csrfToken);
                                    }
                                }
                            }
                        },
                        contentType: 'application/json',
                    });
                }());
            }
            jQuery.when(ajaxCalls).done(successCallback).fail(failureCallback);
        },
    }
}


var itemMixin = {
    mixins: [
        httpRequestMixin
    ],
    data: function() {
        return {
            item: {},
            itemLoaded: false,
        }
    },
    methods: {
        get: function(){
            var vm = this;
            if(!vm.url) return;
            var cb = vm[vm.getCb];
            if( !cb ) {
                cb = function(res){
                    vm.item = res
                    vm.itemLoaded = true;
                }
            }
            vm.reqGet(vm.url, cb);
        },
        validateForm: function(){
            var vm = this;
            var isEmpty = true;
            var fields = $(vm.$el).find('[name]').not(//XXX jQuery
                '[name="csrfmiddlewaretoken"]');
            for( var fieldIdx = 0; fieldIdx < fields.length; ++fieldIdx ) {
                var field = $(fields[fieldIdx]); // XXX jQuery
                var fieldName = field.attr('name');
                var fieldValue = field.attr('type') === 'checkbox' ?
                    field.prop('checked') : field.val();
                if( vm.formFields[fieldName] !== fieldValue ) {
                    vm.formFields[fieldName] = fieldValue;
                }
                if( vm.formFields[fieldName] ) {
                    // We have at least one piece of information
                    // about the plan already available.
                    isEmpty = false;
                }
            }
            return !isEmpty;
        },
    },
}


var filterableMixin = {
    data: function(){
        return {
            params: {
                q: '',
            },
            mixinFilterCb: 'get',
        }
    },
    methods: {
        filterList: function(){
            if(this.params.q) {
                if ("page" in this.params){
                    this.params.page = 1;
                }
            }
            if(this[this.mixinFilterCb]){
                this[this.mixinFilterCb]();
            }
        },
    },
}


var paginationMixin = {
    data: function(){
        return {
            params: {
                page: 1,
            },
            itemsPerPage: this.$itemsPerPage,
            ellipsisThreshold: 4,
            getCompleteCb: 'getCompleted',
            getBeforeCb: 'resetPage',
            qsCache: null,
            isInfiniteScroll: false,
        }
    },
    methods: {
        resetPage: function(){
            var vm = this;
            if(!vm.ISState) return;
            if(vm.qsCache && vm.qsCache !== vm.qs){
                vm.params.page = 1;
                vm.ISState.reset();
            }
            vm.qsCache = vm.qs;
        },
        getCompleted: function(){
            var vm = this;
            if(!vm.ISState) return;
            vm.mergeResults = false;
            if(vm.pageCount > 0){
                vm.ISState.loaded();
            }
            if(vm.params.page >= vm.pageCount){
                vm.ISState.complete();
            }
        },
        paginationHandler: function($state){
            var vm = this;
            if(!vm.ISState) return;
            if(!vm.itemsLoaded){
                // this handler is triggered on initial get too
                return;
            }
            // rudimentary way to detect which type of pagination
            // is active. ideally need to monitor resolution changes
            vm.isInfiniteScroll = true;
            var nxt = vm.params.page + 1;
            if(nxt <= vm.pageCount){
                vm.$set(vm.params, 'page', nxt);
                vm.mergeResults = true;
                vm.get();
            }
        },
        // For pagination buttons
        onClick: function(pageNumber) {
            var vm = this;
            vm.$set(vm.params, 'page', pageNumber);
            vm.get();
        }
    },
    computed: {
        totalItems: function(){
            return this.items.count
        },
        pageCount: function(){
            var nbFullPages = Math.ceil(this.totalItems / this.itemsPerPage);
            if( nbFullPages * this.itemsPerPage < this.totalItems ) {
                ++nbFullPages;
            }
            return nbFullPages;
        },
        minDirectPageLink: function() {
            var vm = this;
            var halfEllipsisThreshold = Math.ceil(vm.ellipsisThreshold / 2);
            if( halfEllipsisThreshold * 2 == vm.ellipsisThreshold ) {
                --halfEllipsisThreshold;
            }
            var minDPL = Math.max(
                1, vm.params.page - halfEllipsisThreshold);
            var maxDPL = Math.min(
                vm.params.page + halfEllipsisThreshold, vm.pageCount);
            return ( maxDPL == vm.pageCount ) ? Math.max(
                vm.pageCount - vm.ellipsisThreshold + 1, 1) : minDPL;
        },
        maxDirectPageLink: function() {
            var vm = this;
            var halfEllipsisThreshold = Math.ceil(vm.ellipsisThreshold / 2);
            if( halfEllipsisThreshold * 2 == vm.ellipsisThreshold ) {
                --halfEllipsisThreshold;
            }
            var minDPL = Math.max(
                1, vm.params.page - halfEllipsisThreshold);
            var maxDPL = Math.min(
                vm.params.page + halfEllipsisThreshold, vm.pageCount);
            return ( minDPL == 1 ) ? Math.min(
                vm.ellipsisThreshold, vm.pageCount) : maxDPL;
        },
        directPageLinks: function() {
            var vm = this;
            var pages = [];
            for( var idx = vm.minDirectPageLink;
                 idx <= vm.maxDirectPageLink; ++idx ){
                pages.push(idx);
            }
            return pages;
        },
        ISState: function(){
            if(!this.$refs.infiniteLoading) return;
            return this.$refs.infiniteLoading.stateChanger;
        },
        qs: function(){
            return this.getQueryString({page: null});
        },
    }
}


var sortableMixin = {
    data: function(){
        var defaultDir = this.$sortDirection || 'desc';
        var dir = (defaultDir === 'desc') ? DESC_SORT_PRE : '';
        var o = this.$sortByField || 'created_at';
        return {
            params: {
                o: dir + o,
            },
            mixinSortCb: 'get'
        }
    },
    methods: {
        sortDir: function(field){
            return this.sortFields[field]
        },
        sortRemoveField: function(field){
            var vm = this;
            var fields = vm.sortFields;
            delete fields[field];
            vm.$set(vm.params, 'o', vm.fieldsToStr(fields));
        },
        sortRemove: function(){
            var vm = this;
            vm.$set(vm.params, 'o', '');
        },
        sortSet: function(field, dir) {
            var vm = this;
            var fields = vm.sortFields;
            var oldDir = fields[field];
            if(!oldDir || (oldDir && oldDir !== dir)){
                if(!(dir === 'asc' || dir === 'desc')){
                    // if no dir was specified - reverse
                    dir = oldDir === 'asc' ? 'desc' : 'asc';
                }
                fields[field] = dir;
                var o = vm.fieldsToStr(fields);
                vm.$set(vm.params, 'o', o);
                if(vm[vm.mixinSortCb]){
                    vm[vm.mixinSortCb]();
                }
            }
        },
        sortBy: function(field){
            var vm = this;
            var oldDir = vm.sortDir(field);
            vm.$set(vm.params, 'o', '');
            vm.sortSet(field, oldDir === 'asc' ? 'desc' : 'asc');
        },
        fieldsToStr: function(fields){
            var res = [];
            Object.keys(fields).forEach(function(key){
                var dir = fields[key];
                var field = '';
                if(dir === 'desc'){
                    field = DESC_SORT_PRE + key;
                } else {
                    field = key;
                }
                res.push(field);
            });
            return res.join(',');
        },
        sortIcon: function(fieldName){
            var res = 'fa fa-sort';
            var dir = this.sortDir(fieldName);
            if(dir){
                res += ('-' + dir);
            }
            return res;
        }
    },
    computed: {
        sortFields: function(){
            var vm = this;
            var res = {};
            if(vm.params.o){
                var fields = (typeof vm.params.o === 'string') ?
                    vm.params.o.split(',') : vm.params.o;
                fields.forEach(function(e){
                    if(!e) return;
                    if(e[0] === DESC_SORT_PRE){
                        res[e.substring(1)] = 'desc';
                    } else {
                        res[e] = 'asc';
                    }
                });
            }
            return res;
        },
    },
}


var itemListMixin = {
    mixins: [
        httpRequestMixin,
        paginationMixin,
        filterableMixin,
        sortableMixin
    ],
    data: function(){
        return this.getInitData();
    },
    methods: {
        getInitData: function(){
            var data = {
                url: null,
                itemsLoaded: false,
                items: {
                    results: [],
                    count: 0
                },
                mergeResults: false,
                params: {
                    // The following dates will be stored as `String` objects
                    // as oppossed to `moment` or `Date` objects because this
                    // is how uiv-date-picker will update them.
                    start_at: null,
                    ends_at: null,
                    // The timezone for both start_at and ends_at.
                    timezone: 'local'
                },
                getCb: null,
                getCompleteCb: null,
                getBeforeCb: null,
            }
            if( this.$dateRange ) {
                if( this.$dateRange.start_at ) {
                    data.params['start_at'] = moment(
                        this.$dateRange.start_at).format("YYYY-MM-DD");
                }
                if( this.$dateRange.ends_at ) {
                    // uiv-date-picker will expect ends_at as a String
                    // but DATE_FORMAT will literally cut the hour part,
                    // regardless of timezone. We don't want an empty list
                    // as a result.
                    // If we use moment `endOfDay` we get 23:59:59 so we
                    // add a full day instead.
                    data.params['ends_at'] = moment(
                        this.$dateRange.ends_at).add(1,'days').format("YYYY-MM-DD");
                }
                if( this.$dateRange.timezone ) {
                    data.params['timezone'] = this.$dateRange.timezone;
                }
            }
            return data;
        },
        get: function(){
            var vm = this;
            if(!vm.url) return
            if(!vm.mergeResults){
                vm.itemsLoaded = false;
            }
            var cb = null;
            if(vm[vm.getCb]){
                cb = function(res){
                    vm[vm.getCb](res);

                    if(vm[vm.getCompleteCb]){
                        vm[vm.getCompleteCb]();
                    }
                }
            } else {
                cb = function(res){
                    if(vm.mergeResults){
                        res.results = vm.items.results.concat(res.results);
                    }
                    vm.items = res;
                    vm.itemsLoaded = true;

                    if( res.detail ) {
                        vm.showMessages([res.detail], "warning");
                    }

                    if(vm[vm.getCompleteCb]){
                        vm[vm.getCompleteCb]();
                    }
                }
            }
            if(vm[vm.getBeforeCb]){
                vm[vm.getBeforeCb]();
            }
            vm.reqGet(vm.url, vm.getParams(), cb);
        },
        getParams: function(excludes){
            var vm = this;
            var params = {};
            for( var key in vm.params ) {
                if( vm.params.hasOwnProperty(key) && vm.params[key] ) {
                    if( excludes && key in excludes ) continue;
                    if( key === 'start_at' || key === 'ends_at' ) {
                        params[key] = moment(vm.params[key], "YYYY-MM-DD").toISOString();
                    } else {
                        params[key] = vm.params[key];
                    }
                }
            }
            return params;
        },
        getQueryString: function(excludes){
            var vm = this;
            var sep = "";
            var result = "";
            var params = vm.getParams(excludes);
            for( var key in params ) {
                if( params.hasOwnProperty(key) ) {
                    result += sep + key + '=' + params[key].toString();
                    sep = "&";
                }
            }
            if( result ) {
                result = '?' + result;
            }
            return result;
        },
    },
};


var TypeAhead = Vue.extend({
    mixins: [
        httpRequestMixin
    ],
    data: function data() {
        return {
            url: null,
            items: [],
            current: -1,
            loading: false,
            minChars: 4,
            query: '',
            queryParamName: 'q',
            selectFirst: false,
        };
    },
    methods: {
        activeClass: function activeClass(index) {
            return {active: this.current === index};
        },

        cancel: function() {},

        down: function() {
            var vm = this;
            if( vm.current < vm.items.length - 1 ) {
                vm.current++;
            } else {
                vm.current = -1;
            }
        },

        hit: function() {
            var vm = this;
            if (vm.current !== -1) {
                vm.onHit(vm.items[vm.current]);
            }
        },

        onHit: function onHit() {
            Vue.util.warn('You need to implement the `onHit` method', this);
        },

        reset: function() {
            var vm = this;
            vm.items = [];
            vm.query = '';
            vm.loading = false;
        },

        setActive: function setActive(index) {
            var vm = this;
            vm.current = index;
        },

        up: function() {
            var vm = this;
            if (vm.current > 0) {
                vm.current--;
            } else if (vm.current === -1) {
                vm.current = vm.items.length - 1;
            } else {
                vm.current = -1;
            }
        },

        update: function update() {
            var vm = this;
            vm.cancel();
            if (!vm.query) {
                return vm.reset();
            }
            if( vm.minChars && vm.query.length < vm.minChars ) {
                return;
            }
            vm.loading = true;
            var params = {};
            params[vm.queryParamName] = vm.query;
            vm.reqGet(vm.url, params,
            function (resp) {
                if (resp && vm.query) {
                    var data = resp.data.results;
                    data = vm.prepareResponseData ? vm.prepareResponseData(data) : data;
                    vm.items = vm.limit ? data.slice(0, vm.limit) : data;
                    vm.current = -1;
                    vm.loading = false;
                    if (vm.selectFirst) {
                        vm.down();
                    }
                }
            }, function() {
                // on failure we just do nothing.
            });
        },
    },
    computed: {
        hasItems: function hasItems() {
            return this.items.length > 0;
        },
        isEmpty: function isEmpty() {
            return !this.query;
        },
        isDirty: function isDirty() {
            return !!this.query;
        }
    },
});

    // attach properties to the exports object to define
    // the exported module properties.
    exports.messagesMixin = messagesMixin;
    exports.httpRequestMixin = httpRequestMixin;
    exports.itemMixin = itemMixin;
    exports.itemListMixin = itemListMixin;
    exports.TypeAhead = TypeAhead;
}));
