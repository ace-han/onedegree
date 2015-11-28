define([
	// should not depend on any other module?
]
,function () {
    'use strict';
    return {
    	init: init
    }
    
    function init(nga, admin, moduleMenu, moduleBaseApiUrl, entityMap){
    	var entityName = 'phone-contact-records';
    	var entity = nga.entity(entityName)
				        .baseApiUrl(moduleBaseApiUrl)
						.label('Phone Contact Record')
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
	        .title('All phone contact records') // default title is "[Entity_name] list"
	        .description('List of phone contact records') // description appears under the title
	        .infinitePagination(false) // (deprecated)load pages as the user scrolls. using pagination to reduce page load
	        .fields([
	            nga.field('id').label('ID') // The default displayed name is the camelCase field name. label() overrides id
	            , nga.field('from_profile', 'reference')
		        	.label('From')
		        	.targetEntity(entityMap['profiles'])
		        	.targetField(nga.field('phone_num'))
//		        	.remoteComplete(true)	// in list view should retrieve foreign keys in once
	            , nga.field('to_profile', 'reference')
		        	.label('To')
		        	.targetEntity(entityMap['profiles'])
		        	.targetField(nga.field('phone_num'))
	            	
	        ])
	        .filters([
                nga.field('q', 'template')
                    .label('')
                    .pinned(true)
                    .template('<div class="input-group"><input type="text" ng-model="value" placeholder="Search" class="form-control"></input><span class="input-group-addon"><i class="glyphicon glyphicon-search"></i></span></div>')
                , nga.field('from_profile', 'reference')
		        	.label('From')
		        	.targetEntity(entityMap['profiles'])
		        	.targetField(nga.field('phone_num'))
		        	.remoteComplete(true)
		        , nga.field('to_profile', 'reference')
		        	.label('To')
		        	.targetEntity(entityMap['profiles'])
		        	.targetField(nga.field('phone_num'))
		        	.remoteComplete(true)
            ])
	        .listActions(['edit', 'delete']);
    	
    	entity.creationView()
	        .fields([
	            nga.field('from_profile', 'reference')
		        	.label('From')
		        	.targetEntity(entityMap['profiles'])
		        	.targetField(nga.field('phone_num'))
		        	.remoteComplete(true)
	            , nga.field('to_profile', 'reference')
		        	.label('To')
		        	.targetEntity(entityMap['profiles'])
		        	.targetField(nga.field('phone_num'))
	        ]);
    	
    	entity.editionView()
        	.fields([
				nga.field('from_profile', 'reference')
		        	.label('From')
		        	.targetEntity(entityMap['profiles'])
		        	.targetField(nga.field('phone_num'))
		        	.remoteComplete(true)
	            , nga.field('to_profile', 'reference')
		        	.label('To')
		        	.targetEntity(entityMap['profiles'])
		        	.targetField(nga.field('phone_num'))
        	        ]);
    	
    	moduleMenu
			.addChild(
					nga.menu(entity)
						.icon('<span class="fa fa-list-ol"></span>')
					);
		
    	
    	admin.addEntity( entity );
    	
    	entityMap[ entityName ] = entity;
    }
    
})