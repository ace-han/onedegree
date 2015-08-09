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
    , './tag/entity'
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
    , tagEntityInit) {
    
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
                 function(NgAdminConfigurationProvider,
                		 tagEntity) {
        	var key;
        	var nga = NgAdminConfigurationProvider;
            var admin = nga.application('ng-admin backend demo', false) // application main title and debug disabled
                .baseApiUrl('http://localhost:8090/'); // main API endpoint
            
            var entityNames = ['tag'], 
            	entityMap = {};
            for(key in entityNames){
            	entityMap[ entityNames[key] ] = nga.entity( entityNames[key] );
            }

            
            tagEntityInit(nga, entityMap);
            // rest entities init stuff
            
            for( key in entityMap){
            	admin.addEntity( entityMap[key] );
            }
            
            nga.configure(admin);
        }])
        .run(function () {
          
        })
    return app;
});