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
    	var entityName = 'tags'
    	var entity = nga.entity(entityName)
				        .baseApiUrl(moduleBaseApiUrl)
						.label('Customized Tags')
	    		        .url(function(entityName, viewType, entityId){
	    		        	// add a suffix to this to avoid new error
	    		        	// refer to https://github.com/marmelab/ng-admin/issues/392?_pjax=%23js-repo-pjax-container
	    		        	// but above link's arguments are outdated, plz debug it with sourcemap to see the function signature
	    		        	// baseApiUrl could be retrieved via this._baseApiUrl and it's already '/' suffixed
	    		        	var url = entityName + '/';
	    		        	if(entityId){
	    		        		url += entityId;
	    		        	}
	    		        	return url;
	    		        });
    	
    	entity.listView()
	        .title('All customized tags') // default title is "[Entity_name] list"
	        .description('List of tags with infinite pagination') // description appears under the title
	        .infinitePagination(false) // (deprecated)load pages as the user scrolls. using pagination to reduce page load
	        .fields([
	            nga.field('id').label('ID') // The default displayed name is the camelCase field name. label() overrides id
	            , nga.field('name') // the default list field type is "string", and displays as a string
	            , nga.field('slug')
	        ])
	        .filters([
                nga.field('q', 'template')
                    .label('')
                    .pinned(true)
                    .template('<div class="input-group"><input type="text" ng-model="value" placeholder="Search" class="form-control"></input><span class="input-group-addon"><i class="glyphicon glyphicon-search"></i></span></div>')
            ])
	        .listActions(['edit', 'delete']);
    	
    	entity.creationView()
	        .fields([
	            nga.field('name')					// the default list field type is "string", and displays as a string
	            	.validation({ required: true }) 
	            , nga.field('slug')
	        ]);
    	
    	entity.editionView()
        	.fields([
					nga.field('name')					// the default list field type is "string", and displays as a string
						.validation({ required: true })
					, nga.field('slug')
						.validation({ required: true })
        	        ]);
    	
    	
    	moduleMenu
			.addChild(nga.menu(entity)
					// entity's default route defined in ng-admin already
					// if we do need this route url setting, might as well define another set routing provider
					//.link('/tag/tree-tags')
					.icon('<span class="fa fa-tags"></span>')
					.active(function(path) {
    		            return path.indexOf('/tags') === 0;
    		        }));
		
    	
    	admin.addEntity( entity );
    	
    	entityMap[ entityName ] = entity;
    }
    
})