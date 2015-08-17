define([
    './module'
    , './namespace'
]
,function (tagModule, tagNamespace) {
    'use strict';
    return tagModule.config([
        '$stateProvider'
        , '$urlRouterProvider'
        , function($stateProvider, $urlRouterProvider){
        	//var quanquanNamespace = 'quanquan';
        	$stateProvider.state('tree-tags-tree', {
        		parent: 'main',
                url: '/tree-tags/tree'
                , cache: false
                , views: {
                  '': {
                    templateUrl: '/static/admin/tag/templates/tree_view.html'
                    //, controller: groupNamespace + '.GroupController as groupController'
                  }
                }
        	})
        }
    ])
})