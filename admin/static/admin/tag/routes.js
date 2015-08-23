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
        	$stateProvider.state('tree-tags-tree', {
        		parent: 'main', // this main is defined in ng-admin
                url: '/tree-tags/tree'
                , cache: false
                , resolve:{
                	treeTagJson: ['tag.TreeTagService', function(treeTagService){
                		return treeTagService.getAllTreeTags();
                	}]
                }
                , views: {
                  '': {
                    templateUrl: '/static/admin/tag/templates/tree_view.html'
                    , controller: tagNamespace + '.TreeTagController as treeTagController'
                  }
                }
        	})
        }
    ])
})