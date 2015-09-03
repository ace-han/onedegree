define([
    '../module'
    , '../namespace'
    , './schoolEntity.initializer'
    , './profileEntity.initializer'
],
function (module, namespace
		, userEntityInitializer
		, profileEntityInitializer) {
    'use strict';

    // special for tag module in ng-admin entity definition via an init method 
    var name = namespace + '.entities';
    var constant = {
    		init: init
    }
    module.constant(name, constant);
    
    return constant;

    function init(nga, admin, rootMenuItem, baseApiUrl, entityMap){
    	

        var authModuleMenu = nga.menu()
							  .title('Account')
							  .link('/account')
							  .icon('<span class="fa fa-users"></span>');

        userEntityInitializer.init(nga, admin, authModuleMenu, baseApiUrl + '/account/', entityMap);
        profileEntityInitializer.init(nga, admin, authModuleMenu, baseApiUrl + '/account/', entityMap);
        
        rootMenuItem.addChild( authModuleMenu)
    }

});
