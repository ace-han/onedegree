define([
	
]
,function () {
    'use strict';
    return treeTagEntityInit;
    
    function treeTagEntityInit(nga, entityMap){
    	// nga is NgAdminConfigurationProvider
    	if(! ('tag' in entityMap) ){
    		throw 'No tag defined in entityMap';
    	}
    	var tag = entityMap['tag'];
    	// do the real setup for target
    	//...
    	
    }
})