
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
    	"jquery": "jquery/dist/jquery.min"
		, "angular": "angular/angular"	// since it's bower.json defines main: xxx
		, "angular-bootstrap": "angular-bootstrap/ui-bootstrap-tpls" // bootstrap no required?
		// "angular-bootstrap/ui-bootstrap"  // ui-bootstrap-tpls = ui-bootstrap + html defined templates
		, 'angular-resource': "angular-resource/angular-resource"
		, 'angular-sanitize': "angular-sanitize/angular-sanitize"
		, 'angular-ui-codemirror': "angular-ui-codemirror/ui-codemirror"
		, 'angular-ui-router': "angular-ui-router/release/angular-ui-router"
		, 'angular-numeraljs': "angular-numeraljs/dist/angular-numeraljs"
		, 'humane': "humane/humane"
		, 'inflection': "inflection/inflection.min"
		, 'lodash': "lodash/dist/lodash"
		, 'ng-file-upload': "ng-file-upload/ng-file-upload-all"
		, 'ngInflection': "ngInflection/dist/ngInflection"
		, 'nprogress': "nprogress/nprogress"
		, 'restangular': "restangular/dist/restangular"
		, 'textAngular': "textAngular/dist/textAngular.min"
		, 'papaparse': "papaparse/papaparse"
		, 'numeral': "numeral/min/numeral.min"
		, 'codemirror': "codemirror/lib/codemirror"
		, 'codemirror-closebrackets': "codemirror/addon/edit/closebrackets"
		, 'codemirror-lint': "codemirror/addon/lint/lint"
		, 'jsonlint': "jsonlint/lib/jsonlint"
		, 'codemirror-json-lint': "codemirror/addon/lint/json-lint"
		, 'codemirror-active-line': "codemirror/addon/selection/active-line"
		, 'codemirror-javascript': "codemirror/mode/javascript/javascript"

		, 'angular-cookies': "angular-cookies/angular-cookies"
		, 'bootstrap': "bootstrap/dist/js/bootstrap"
		, 'bootstrap-sass-official': "bootstrap-sass-official/assets/javascripts/bootstrap"	//actually these two are the same
		, 'es5-shim': "es5-shim/es5-shim"
		, 'json3': "json3/lib/json3"
		, 'papaparse': 'papaparse/papaparse'
		, 'ng-admin': "ng-admin/build/ng-admin-only.min"
		, 'requirejs-text': "requirejs-text/text"
		, 'ui-select': 'angular-ui-select/dist/select'
	
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
    	, 'codemirror': {exports: 'codemirror'}
    	, 'numeral': {exports: 'numeral'}
    	, 'lodash': {exports: 'lodash'}
    	, 'angular-cookies': {exports: 'angular-cookies', deps: ['angular']}
    	, 'bootstrap': {exports: 'bootstrap', deps: ['jquery']}
    	, 'bootstrap-sass-official': {exports: 'bootstrap-sass-official', deps: ['jquery']}
    	, 'es5-shim': {exports: 'es5-shim'}
    	, 'humane': {exports: 'humane'}
    	, 'json3': {exports: 'json3'}
    	, 'jsonlint': {exports: 'jsonlint'}
    	, 'lodash': {exports: 'lodash'}
    	, 'requirejs-text': {exports: 'requirejs-text'}
    	, 'papaparse': {exports: 'papaparse'}
    	, 'inflection': {exports: 'inflection'}
    	, 'jstree': {exports: 'jstree'}
    	, 'angular-bootstrap': { deps: ['angular']}
    	, 'angular-resource': { deps: ['angular']}
    	, 'angular-sanitize': { deps: ['angular']}
    	, 'angular-ui-codemirror': { deps: ['angular', 'codemirror']}
    	, 'angular-ui-router': { deps: ['angular']}
    	, 'angular-numeraljs': { deps: ['angular', 'numeral']}
    	, 'ng-file-upload': { deps: ['angular']}
    	, 'ngInflection': { deps: ['angular', 'inflection']}
    	, 'nprogress': { deps: ['angular']}
    	, 'restangular': { deps: ['angular', 'lodash']}
    	, 'textAngular': { deps: ['angular']}
    	, 'ui-select': { deps: ['angular']}
    	, 'ng-js-tree': {deps: ['jquery', 'angular', 'jstree']}

    	// in this case just need to define(['ng-admin'], function(){}); will get all dependencies loaded
    	, 'ng-admin': { deps: [
						'jquery', 
						, 'angular'
						, 'angular-bootstrap'
						, 'angular-cookies'
						, 'angular-numeraljs'
						, 'angular-resource'
						, 'angular-sanitize'
						, 'angular-ui-codemirror'
						, 'angular-ui-router'
						, 'bootstrap'
						, 'bootstrap-sass-official', // should be already duplicate
						, 'es5-shim'
						, 'humane'
						, 'json3'
						, 'jsonlint'
						, 'ng-file-upload'
						, 'ngInflection'
						, 'nprogress'
						, 'requirejs-text'
						, 'restangular'
						, 'textAngular'
						, 'papaparse'
						, 'ui-select'
    					, 'ng-js-tree'
    				] }
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
