
require.config({
    baseUrl: '/static/bower_components', //By default load any module IDs from
 // waitSeconds: The number of seconds to wait before giving up on loading a script. Setting it to 0 disables the timeout. The default is 7 seconds.
    waitSeconds: 0, 
    paths: {
    	/*
    	 * paths: path mappings for module names not found directly under baseUrl. 
    	 * The path settings are assumed to be relative to baseUrl, 
    	 * unless the paths setting starts with a "/" or has a URL protocol in it ("like http:"). 
    	 * Using the above sample config, "some/module"'s script tag will be src="/another/path/some/v1.0/module.js".
    	 */
    	
    	// here add quote in "" or '' for those with hypen dash
    	// default key equals to bower.json's name in the module
    	// the name defined here will be used in requirejs's define directive
    	// e.g.:
    	// define(['angular-bootstrap', 'angular-resource'])
    	'jquery': 'jquery/dist/jquery.min'
		, 'angular': 'angular/angular'	// since it's bower.json defines main: xxx

        , 'humane': 'humane/humane'
	    , 'ng-admin': 'ng-admin/build/ng-admin.min'
		, 'jstree': 'jstree/dist/jstree'
		, 'ng-js-tree': 'ng-js-tree/dist/ngJsTree'
    	, 'admin': '../admin'	//since baseUrl is bower_component. Inside the admin/app.js will do relative path dependencies
    	, 'common': '../common'
    	//, xxx: 'xxx'
    },
    shim: {
    	// read each bower.json to get dependencies info 
    	'jquery': {exports: 'jquery'}
    	, 'angular': {exports: 'angular', deps: ['jquery']} // deps on jquery to ensure jsTree workable

    	, 'ng-js-tree': {deps: ['jquery', 'angular', 'jstree']}

    	// in this case just need to define(['ng-admin'], function(){}); will get all dependencies loaded
        , 'ng-admin': {deps: ['jquery', 'angular']}
        , 'admin/app': {deps: ['ng-js-tree', 'humane']}
    }
});

require([
        'angular'
        ,'admin/namespace'
        ,'admin/app'
        ,'admin/routes'
    ],
    function (angular, namespace) {
		angular.element(document).ready(function() {
            // since app/app depends on a lot of other stuff (by requirejs),
            // so we just need to bootstrap ['app'] then all stuff in this project is up
			angular.bootstrap(document, [namespace]);
		});
		
    });
