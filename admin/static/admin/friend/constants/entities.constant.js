define([
    '../module'
    , '../namespace'
    , './phoneContactRecordEntity.initializer'
],
function (module, namespace
		, contactRecordEntityInitializer) {
    'use strict';

    // special for tag module in ng-admin entity definition via an init method 
    var name = namespace + '.entities';
    var constant = {
    		init: init
    }
    module.constant(name, constant);
    
    return constant;

    function init(nga, admin, rootMenuItem, baseApiUrl, entityMap){
    	

        var moduleMenu = nga.menu()
							  .title('Friend')
							  .link('/friend')
							  .icon('<span class="fa fa-user-plus"></span>');
        var moduleBabseApiUrl = baseApiUrl + '/friend/';
        
        contactRecordEntityInitializer.init(nga, admin, moduleMenu, moduleBabseApiUrl, entityMap);
        
        rootMenuItem.addChild( moduleMenu);
    }

});
