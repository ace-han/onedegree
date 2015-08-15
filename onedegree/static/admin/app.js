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
    //, './tag/entity' // migrate to constant, a constant is an IIFE complex object with method init
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
    ) {
    
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
        .config(['NgAdminConfigurationProvider' 
                 , 'tag.entities'
                 , function(NgAdminConfigurationProvider
                		 , tagModuleEntities) {
        	var nga = NgAdminConfigurationProvider;
        	var baseApiUrl = 'http://localhost:8090/api/v1/admin';
            var admin = nga.application('One Degree Admin Site', true) // application main title and debug disabled
                .baseApiUrl(baseApiUrl); // main API endpoint
            

            // this form is commonjs pattern 
            // and commonjs is not designated to cater web browser
//            var tag = require('tag');
            
            // then I need to resolve menu item modulization...
            // in a simple way, entityMap sounds fine
            // each module's init method defines its menu(with nested menu items defined)
            // and entity definitions within
            // the cross-module entity dependency order might as well be 
            // maintained by the developer for the sake of simplicity 
            var rootMenuItem = nga.menu(), 
            	entityMap = {};
            
            // init methods have no return value, only edit the content of below references
            tagModuleEntities.init(nga, admin, rootMenuItem, baseApiUrl, entityMap);
            
            
            admin.menu(rootMenuItem);
            nga.configure(admin);
        }])
        .run(function () {
          
        })
    return app;
});