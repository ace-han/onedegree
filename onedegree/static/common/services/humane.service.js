define([
      'humane'
    , '../module'
    , '../namespace'
],
function (humane, module, namespace) {
    'use strict';

    var name = namespace + '.HumaneService';
    
    module.factory(name, HumaneService);

    HumaneService.$inject = [];

    return HumaneService;

    function HumaneService(){
    	humane.timeout = 5000;
        humane.clickToClose = true;
        humane.baseCls = 'humane-flatty';
        humane.addnCls = 'humane-flatty-info';
        return humane;
    }
});