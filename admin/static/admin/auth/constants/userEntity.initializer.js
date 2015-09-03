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
    	var entityName = 'users'
    	var entity = nga.entity(entityName)
				        .baseApiUrl(moduleBaseApiUrl)
						.label('User')
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
	        .title('All registed users') // default title is "[Entity_name] list"
	        .description('List of registed users') // description appears under the title
	        .infinitePagination(false) // (deprecated)load pages as the user scrolls. using pagination to reduce page load
	        .fields([
	            nga.field('id').label('ID') // The default displayed name is the camelCase field name. label() overrides id
	            , nga.field('username') // the default list field type is "string", and displays as a string
	            , nga.field('nickname')
	            , nga.field('email', 'email')
	            , nga.field('is_active', 'boolean')
	            		.label('active')
	            , nga.field('last_login', 'datetime')
	            , nga.field('date_joined', 'date')
	            , nga.field('is_staff', 'boolean')
	            		.label('Staff')
	            , nga.field('is_superuser', 'boolean')
	            		.label('Admin')
	        ])
	        .filters([
                nga.field('q', 'template')
                    .label('')
                    .pinned(true)
                    .template('<div class="input-group"><input type="text" ng-model="value" placeholder="Search" class="form-control"></input><span class="input-group-addon"><i class="glyphicon glyphicon-search"></i></span></div>')
                , nga.field('is_staff', 'boolean')
                    .label('Staff')
                , nga.field('is_superuser', 'boolean')
                    .label('Super User'),
            ])
	        .listActions(['edit', 'delete']);
    	
    	entity.creationView()
	        .fields([
	            nga.field('username')					// the default list field type is "string", and displays as a string
	            	.validation({ required: true }) 
	            , nga.field('password', 'password')
	            	.validation({ required: true }) 
	            , nga.field('nickname')
	            , nga.field('email', 'email')
	        ]);
    	
    	entity.editionView()
        	.fields([
					nga.field('username')					// the default list field type is "string", and displays as a string
						.validation({ required: true })
					, nga.field('password', 'password')
						.validation({ required: true })
					, nga.field('nickname')
					, nga.field('email', 'email')
        	        ]);
    	
    	moduleMenu
			.addChild(
					nga.menu(entity)
						.icon('<span class="fa fa-user"></span>')
					);
		
    	
    	admin.addEntity( entity );
    	
    	entityMap[ entityName ] = entity;
    }
    
})