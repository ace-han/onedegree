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
    	humane.timeout = 3000;
        humane.clickToClose = true;
        humane.baseCls = 'humane-flatty';
        humane.addnCls = 'humane-flatty-info';
        humane.info = humane.spawn({ addnCls: 'humane-flatty-info' });
        humane.success = humane.spawn({ addnCls: 'humane-flatty-success' });
        humane.error = humane.spawn({ addnCls: 'humane-flatty-error' });
        return humane;
    }
});