define([
	// should not depend on any other module?
]
,function () {
    'use strict';
    return {
    	init: init
    }
    
    function init(nga, admin, moduleMenu, moduleBaseApiUrl, entityMap){
    	var entityName = 'profiles';
    	var entity = nga.entity(entityName)
				        .baseApiUrl(moduleBaseApiUrl)
						.label('Profile')
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
    	var cities = [
           	       {value: 'beijing', label: 'Beijing'},
        	       {value: 'shanghai', label: 'Shanghai'},
        	       {value: 'guangzhou', label: 'Guangzhou'},
        	       {value: 'shenzhen', label: 'Shenzhen'},
        	 ];
    	entity.listView()
	        .title('All profiles') // default title is "[Entity_name] list"
	        .description('List of profiles') // description appears under the title
	        .infinitePagination(false) // (deprecated)load pages as the user scrolls. using pagination to reduce page load
	        .fields([
	            nga.field('id').label('ID') // The default displayed name is the camelCase field name. label() overrides id
	            , nga.field('user', 'reference')
		        	.label('User')
		        	.targetEntity(entityMap['users'])
		        	.targetField(nga.field('username'))
//		        	.remoteComplete(true)	// in list view should retrieve foreign keys in once
	            , nga.field('phone_num')
	            , nga.field('gender', 'choice')
	            	.choices([
							{ value: null, label: 'Unknown' },
							{ value: '0', label: 'Female' },
							{ value: '1', label: 'Male' },
	            		])
	            , nga.field('city', 'choice')
//	            	.choices(function(entry){
//	            		// function choices need to return an array
//	            		var city = entry.values.city || '';
//	            		return [{value: city, label: city.toUpperCase()}];
//	            	})
	            	.choices(cities)
	            , nga.field('high_school', 'reference')
				        	.label('High School')
				        	.targetEntity(entityMap['schools'])
				        	.targetField(nga.field('name'))
				, nga.field('college', 'reference')
				        	.label('College')
				        	.targetEntity(entityMap['schools'])
				        	.targetField(nga.field('name'))
	            	
	        ])
	        .filters([
                nga.field('q', 'template')
                    .label('')
                    .pinned(true)
                    .template('<div class="input-group"><input type="text" ng-model="value" placeholder="Search" class="form-control"></input><span class="input-group-addon"><i class="glyphicon glyphicon-search"></i></span></div>')
                 , nga.field('gender', 'choice')
	            	.choices([
							{ value: null, label: 'Unknown' },
							{ value: '0', label: 'Female' },
							{ value: '1', label: 'Male' },
	            		])
                 , nga.field('city', 'choice')
	            	.choices(cities)
                , nga.field('high_school', 'reference')
		        	.label('High School')
		        	.targetEntity(entityMap['schools'])
		        	.targetField(nga.field('name'))
		        	.remoteComplete(true)
		        , nga.field('college', 'reference')
		        	.label('College')
		        	.targetEntity(entityMap['schools'])
		        	.targetField(nga.field('name'))
		        	.remoteComplete(true)
            ])
	        .listActions(['edit', 'delete']);
    	
    	entity.creationView()
	        .fields([
	            nga.field('user', 'reference')
		        	.label('User')
		        	.targetEntity(entityMap['users'])
		        	.targetField(nga.field('username'))
		        	.remoteComplete(true)
	            , nga.field('phone_num')
	            	.validation({required: true})
	            , nga.field('gender', 'choice')
	            	.choices([
							{ value: null, label: 'Unknown' },
							{ value: '0', label: 'Female' },
							{ value: '1', label: 'Male' },
	            		])
	            , nga.field('city', 'choice')
	            	.choices(cities)
	            , nga.field('whatsup', 'text')
	            	.label('What\'s up')
	            , nga.field('high_school', 'reference')
				        	.label('High School')
				        	.targetEntity(entityMap['schools'])
				        	.targetField(nga.field('name'))
				        	.remoteComplete(true)
				, nga.field('college', 'reference')
				        	.label('College')
				        	.targetEntity(entityMap['schools'])
				        	.targetField(nga.field('name'))
				        	.remoteComplete(true)
				, nga.field('occupations', 'reference_many')
				        	.targetEntity(entityMap['tree-tags'])
				        	.targetField(nga.field('name'))
				        	.remoteComplete(true
				        			, {
					        		refreshDelay: 300
					        		, searchQuery: function(search){
					        			return {q: search};
					        		}
					        }
				        	)        	
				, nga.field('tags', 'reference_many')
			        	.label('Tags')
			        	.targetEntity(entityMap['tags'])
			        	.targetField(nga.field('name'))
			        	.remoteComplete(true
			        			, {
				        		refreshDelay: 300
				        		, searchQuery: function(search){
				        			return {q: search};
				        		}
				        }
			        	)
	        ]);
    	
    	entity.editionView()
        	.fields([
					nga.field('user', 'reference')
			        	.label('User')
			        	.targetEntity(entityMap['users'])
			        	.targetField(nga.field('username'))
			        	.remoteComplete(true)
		            , nga.field('phone_num')
		            	.validation({required: true})
		            , nga.field('gender', 'choice')
		            	.choices([
								{ value: null, label: 'Unknown' },
								{ value: '0', label: 'Female' },
								{ value: '1', label: 'Male' },
		            		])
		            , nga.field('city', 'choice')
		            	.choices(cities)
		            , nga.field('whatsup', 'text')
		            	.label('What\'s up')
		            , nga.field('high_school', 'reference')
					        	.label('High School')
					        	.targetEntity(entityMap['schools'])
					        	.targetField(nga.field('name')
//					        			// this may need ES6 to do so, not worth it right now
//					        			.map(function addLevel(value, entry) {
//					        				var padding = '';
//					        				for(var i=0; i<3; i++){
//					        					padding += '-';
//					        				}
//							                return padding + value;
//							            })
							            )
							    .permanentFilters({ type: 'high_school'})
					        	.remoteComplete(true)
					, nga.field('college', 'reference')
					        	.label('College')
					        	.isDetailLink(false)
					        	.targetEntity(entityMap['schools'])
					        	.targetField(nga.field('name'))
					        	.permanentFilters({ type: 'college'})
					        	.remoteComplete(true)
					, nga.field('occupations', 'reference_many')
				        	.targetEntity(entityMap['tree-tags'])
				        	.targetField(nga.field('name'))
				        	.remoteComplete(true
				        			, {
					        		refreshDelay: 300
					        		, searchQuery: function(search){
					        			return {q: search};
					        		}
					        }
				        	)        	
					, nga.field('tags', 'reference_many')
				        	.label('Tags')
				        	.targetEntity(entityMap['tags'])
				        	.targetField(nga.field('name'))
				        	.remoteComplete(true
				        			, {
					        		refreshDelay: 300
					        		, searchQuery: function(search){
					        			return {q: search};
					        		}
					        }
				        	)
				        	
        	        ]);
        	        
    	
    	moduleMenu
			.addChild(
					nga.menu(entity)
						.icon('<span class="fa fa-black-tie"></span>')
					);
		
    	
    	admin.addEntity( entity );
    	
    	entityMap[ entityName ] = entity;
    }
    
})