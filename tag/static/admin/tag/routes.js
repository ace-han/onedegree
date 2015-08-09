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
        }
        ])
})