define([
    '../module'
    , '../namespace'
    , './treeTagEntity.initializer'
    , './tagEntity.initializer'
],
function (module, namespace
		, treeTagEntityInitializer
		, tagEntityInitializer) {
    'use strict';

    // special for tag module in ng-admin entity definition via an init method 
    var name = namespace + '.entities';

    // via literal objects IIFE(Immediately Invoked Function Expression)
    // refer to http://michalostruszka.pl/blog/2012/12/23/angular-better-constant-values/ 
//    var constant = (function(){
//    	var moduleEntities = {
//    		init: init
//    	};
//    	return moduleEntities;
//    })();
    // since we've already in a function that could take many definitions
    // no need to do IIFE
    var constant = {
    		init: init
    }
    module.constant(name, constant);
    
    return constant;

    function init(nga, admin, rootMenuItem, baseApiUrl, entityMap){
    	

        var moduleMenu = nga.menu()
							  .title('Tag')
							  .link('/tag')
							  .icon('<span class="fa fa-tags"></span>');
        var moduleBaseApiUrl = baseApiUrl + '/tag/';
        treeTagEntityInitializer.init(nga, admin, moduleMenu, moduleBaseApiUrl, entityMap);
        tagEntityInitializer.init(nga, admin, moduleMenu, moduleBaseApiUrl, entityMap);
        
        rootMenuItem.addChild( moduleMenu )
    }

});
