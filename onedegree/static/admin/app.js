define([
    'angular'
    , './namespace'
    // add necessary app as you wish
    , './tag/namespace'
//    , './account/namespace'
//    , './contact/namespace'
//    , './search/namespace'
//    , './group/namespace'
//    , './common/namespace'
//    , './quanquan/namespace'
    // would be entity for diff app entity c-tor
    , './tag/entities/treeTagEntity'
    // for the convenience of invocation
    , 'ng-admin'
    , './tag/module.require'
//    , './account/module.require'
//    , './contact/module.require'
//    , './search/module.require'
//    , './group/module.require'
//    , './common/module.require'
//    , './quanquan/module.require'
],
function (angular, namespace
    , tagNamespace
    , treeTagEntityInit) {
    
    /* 
        Admin official entry point
    */

    'use strict';

    var app = angular.module(namespace, 
        ['ng-admin'
        //, 'ct.ui.router.extras.future', 'ct.ui.router.extras.statevis' // this two should be manually added
        //, 'angularMoment'

        
        // below enable those namespace to be injected
        , tagNamespace
//        , contactNamespace, searchNamespace
//        , groupNamespace, commonNamespace
//        , quanquanNamespace
        ])
        .config(['NgAdminConfigurationProvider', 
                 function(NgAdminConfigurationProvider) {
        	var key;
        	var nga = NgAdminConfigurationProvider;
        	var baseApiUrl = 'http://localhost:8090/api/v1/admin';
            var admin = nga.application('ng-admin backend demo', false) // application main title and debug disabled
                .baseApiUrl(baseApiUrl); // main API endpoint
            
            var entityNames = ['tag'], 
            	entityMap = {};
            for(key in entityNames){
            	entityMap[ entityNames[key] ] = nga.entity( entityNames[key] );
            }

            
            treeTagEntityInit(nga, entityMap);
            // rest entities init stuff
            
//            for( key in entityMap){
//            	admin.addEntity( entityMap[key] );
//            }
            
            
            var tagModuleMenu = nga.menu()
								  .title('Tag')
								  .link('/tag')
								  .icon('<span class="fa fa-tags"></span>');
            
            var treeTag = nga.entity('tree-tags')
					            .baseApiUrl(baseApiUrl + '/tag/')
            					.label('Tree Tags')
//            					.url(function(entityName, viewType, identifierValue, identifierName) {
//            						return '/tag/tree-tags/' + entityName + '_' + viewType + '?' + identifierName + '=' + identifierValue; // Can be absolute or relative
//            					});
            
            treeTag.listView()
	            .title('All tree tags') // default title is "[Entity_name] list"
	            .description('List of tree tags with infinite pagination') // description appears under the title
	            .infinitePagination(true) // load pages as the user scrolls
	            .fields([
	                nga.field('id').label('ID'), // The default displayed name is the camelCase field name. label() overrides id
	                nga.field('name'), // the default list field type is "string", and displays as a string
	                nga.field('slug')
	            ])
	            .listActions(['show', 'edit', 'delete']);
            admin.addEntity( treeTag )
            admin.menu(nga.menu()
            		 		.addChild(
            		 				tagModuleMenu
            		 					.addChild(nga.menu(treeTag)
            		 							// entity's default route defined in ng-admin already
            		 							// if we do need this route url setting, might as well define another set routing provider
            		 							//.link('/tag/tree-tags')
            		 							.icon('<span class="fa fa-tree"></span>'))
            				 )
            		
            		);
            nga.configure(admin);
        }])
        .run(function () {
          
        })
    return app;
});