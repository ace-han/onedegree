define([
    '../module'
    , '../namespace'
    , './userEntity.initializer'
],
function (module, namespace
		, userEntityInitializer) {
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
							  .title('Auth')
							  .link('/auth')
							  .icon('<span class="fa fa-unlock-alt"></span>');
        var moduleBaseApiUrl = baseApiUrl + '/auth/';
        userEntityInitializer.init(nga, admin, moduleMenu, moduleBaseApiUrl, entityMap);
        
        
        rootMenuItem.addChild( moduleMenu)
    }

});
