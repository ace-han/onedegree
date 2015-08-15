define([
	// should not depend on any other module?
]
,function () {
    'use strict';
    return {
    	init: init
    }
    
    function init(nga, admin, moduleMenu, moduleBaseApiUrl, entityMap){
    	// some entityMap for dependency checking
//    	if(! ('tag' in entityMap) ){
//    		throw 'No tag defined in entityMap';
//    	}
    	var entityName = 'tree-tags'
    	var treeTag = nga.entity(entityName)
				        .baseApiUrl(moduleBaseApiUrl)
						.label('Tree Tags');
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
    	
    	moduleMenu
			.addChild(nga.menu(treeTag)
					// entity's default route defined in ng-admin already
					// if we do need this route url setting, might as well define another set routing provider
					//.link('/tag/tree-tags')
					.icon('<span class="fa fa-tree"></span>'));
    	admin.addEntity( treeTag );
    	
    	entityMap[ entityName ] = treeTag;
    }
    
})