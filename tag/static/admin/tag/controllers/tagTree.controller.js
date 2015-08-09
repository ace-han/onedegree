define([
    '../module'
    , '../namespace'
],
function (module, namespace) {
    'use strict';

    var name = namespace + '.TreeTagController';

    module.controller(name, TreeTagController);
                
    TreeTagController.$inject = ['$http', '$q', '$window', '$timeout' ];

    return TreeTagController;

    function TreeTagController($http, $q, $window, $timeout) {
        var vm = this;

        
        
    }


});
