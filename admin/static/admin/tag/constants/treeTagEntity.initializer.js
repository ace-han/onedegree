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
						.label('Tree Tags (Tabular View)');
    	
    	treeTag.listView()
	        .title('All tree tags') // default title is "[Entity_name] list"
	        .description('List of tree tags with infinite pagination') // description appears under the title
	        .infinitePagination(false) // (deprecated)load pages as the user scrolls. using pagination to reduce page load
	        .fields([
	            nga.field('id').label('ID'), // The default displayed name is the camelCase field name. label() overrides id
	            nga.field('name'), // the default list field type is "string", and displays as a string
	            nga.field('slug'),
	            nga.field('parent_id', 'reference')
	            	.label('Parent')
	            	.targetEntity(treeTag)
	            	.targetField(nga.field('name')),
	            nga.field('tree_id'),
	            nga.field('level')
	        ])
	        .filters([
                nga.field('q', 'template')
                    .label('')
                    .pinned(true)
                    .template('<div class="input-group"><input type="text" ng-model="value" placeholder="Search" class="form-control"></input><span class="input-group-addon"><i class="glyphicon glyphicon-search"></i></span></div>'),
                nga.field('tree_id')
                    .label('Tree ID')
                    .attributes({'placeholder': 'Filter by tree id'}),
                nga.field('parent_id', 'reference')
                    .label('Parent')
                    .targetEntity(treeTag)
                    .targetField(nga.field('name'))
                    .remoteComplete(true, { refreshDelay: 300 })
                    .attributes({'placeholder': 'Filter by parent name'}),
            ])
	        .listActions(['edit', 'delete']);
    	
    	treeTag.creationView()
	        .fields([
	            nga.field('id').label('ID'), // The default displayed name is the camelCase field name. label() overrides id
	            nga.field('name'), // the default list field type is "string", and displays as a string
	            nga.field('slug'),
	            nga.field('parent_id', 'reference')
	            	.label('Parent')
	            	.targetEntity(treeTag)
	            	.targetField(nga.field('name'))
	            	.validation({ required: true })
	            	.remoteComplete(true, { refreshDelay: 0 }),
	            nga.field('tree_id'),
	            nga.field('level')
	        ]);
    	
    	treeTag.editionView()
        	.fields(treeTag.creationView().fields())
    	
    	
    	moduleMenu
    		.addChild(nga.menu()
    				.title('Tree Tags (Tree View)')
    				.icon('<span class="fa fa-tree"></span>')
    				.link('/tree-tags/tree')
    				.active(function(path) {
    		            return path.indexOf('/tree-tags/tree') === 0;
    		        }))
			.addChild(nga.menu(treeTag)
					// entity's default route defined in ng-admin already
					// if we do need this route url setting, might as well define another set routing provider
					//.link('/tag/tree-tags')
					.icon('<span class="fa fa-th-list"></span>')
					.active(function(path) {
    		            return path.indexOf('/tree-tags') === 0 && path.indexOf('/tree-tags/tree') !== 0;
    		        }));
		
    	
    	admin.addEntity( treeTag );
    	
    	entityMap[ entityName ] = treeTag;
    }
    
})