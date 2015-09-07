define([
    'angular'
    , '../module'
    , '../namespace'
    , 'common/plugins/jstree.decorators'	// just ensure the decorators plugin get inited
    
],
function (angular, module, namespace) {
    'use strict';

    var name = namespace + '.TreeTagService';

    module.factory(name, TreeTagService);

    TreeTagService.$inject = ['$q', 'Restangular'];

    return TreeTagService;

    function TreeTagService($q, Restangular){

    	//var treeTagRestService = Restangular.service('tree-tags', Restangular.all(namespace));
    	//var treeTagRestangular = Restangular.all(namespace).all('tree-tags')
    	//var treeTagRestangular = Restangular.allUrl('tree-tags', 'http://http://localhost:8090/api/v1/admin/tag/tree-tags/');
    	var treeTagRestangular = Restangular.withConfig(function(RestangularConfigurer) {
    		// this one will strip other unnecessary data meta
    		RestangularConfigurer.setFullResponse(false);	
    	  });
//    	var treeTagRestangular = Restangular.setFullResponse(false).all(namespace).all('tree-tags');
    	//var treeTagRestangular = Restangular.all(namespace).all('tree-tags')
    	//var treeTagRestangular = treeTagRestangular.all(namespace).all('tree-tags');
    	
    	var treeTagCollectionRestangular = treeTagRestangular.all(namespace).all('tree-tags');
    	var treeTagInstanceRestangular = function(treeTagId){
   			return treeTagRestangular.all(namespace).one('tree-tags', treeTagId);
    		
    	}
    	
    	var service = {
        	getAllTreeTags: getAllTreeTags
            , getTreeConfig: getTreeConfig
            , addNode: addNode
            , removeNodes: removeNodes
            , updateNode: udpateNode
            , moveNode: moveNode
            , updateNodes: updateNodes
            , moveNodes: moveNodes
        }

        return service;
    	
        function getAllTreeTags(){
        	// set the page_size insanely large to retrieve them all
        	return treeTagCollectionRestangular.customGETLIST('cumulative_count', {page_size: 100000})
        			.then(function(response){
        				var treeTags = response;
        				angular.forEach(treeTags, function(treeTag, index){
        					// descendant count
        					var descendantCount = Math.floor((treeTag.rght-treeTag.lft-1)/2);
        					//treeTag.isLeaf = (descendantCount==0);
        					//treeTag.icon = (descendantCount>0)? 'fa fa-tags': 'fa fa-tag';
        					treeTag.type = (descendantCount>0)? 'node': 'leaf';
        					treeTag.text = treeTag.name;
        					treeTag.parent = treeTag.parent || '#';
        					treeTag.data = {cumulative_count: treeTag.cumulative_count};
        				});
        				return treeTags;
        			});
        			//}).$object; // do not do this to break the filtered response-treeTags
        }

        function getTreeConfig(){
        	// write this way already make it new an object every time
        	var treeConfig = {
                    core : {
                        multiple : false,	//TODO only single one for the time being
                        animation: true,
                        error : function(error) {
                        	console.error('treeCtrl: error from js tree - ' + angular.toJson(error) );
                        },
                        check_callback : function(operation, node, node_parent, node_position, more){
//        					var inst = $.jstree.reference(node);
//        					var inst = vm.treeInstance.jstree(true); // no more vm reference in the service
        					var inst = angular.element.jstree.reference(node);
        					if(operation == 'move_node' && !node_parent.parent && node_position != 2){
        						// only insert into root, neither before nor after
        						// position 2 means inside, 0 before, 1 after 
        						return false;
        					}

        					if(operation == 'delete_node' && !node_parent.parent){
        						// Root should not be deleted in multi selection 
        						return false;
        					}
        					return true;
        				},
                        worker : true
                    },
                    types: {
                        "leaf": {
                            icon: 'fa fa-tag'
                        }
                        , 'node': {
                            icon: 'fa fa-tags'
                        }
                    },
                    contextmenu: {select_node: false, items: customizedMenu},
                    dnd: {inside_pos: 'last', check_while_dragging: true},
                    decorators: {
						'.jstree-anchor': function(nodeId, liContainer, targetElem){
								targetElem = $(targetElem);
								// this ==> jstreeInst
								var node = this.get_json(nodeId, {no_children:true, no_id: true, no_state: true});
								targetElem.after('<span >( ' + (node.data.cumulative_count || 0)+ ' )</span>');
						}
					},
                    plugins: ['types', 'contextmenu', 'unique', 'dnd', 'decorators' ],
                    version: 1
                };
        	return treeConfig;
        }
        
        function customizedMenu(node){
//        	var inst = $.jstree.reference(node);
//        	var inst = vm.treeInstance.jstree(true);
        	var inst = angular.element.jstree.reference(node);
			
			var items = angular.element.jstree.defaults.contextmenu.items();
			items.rename.shortcut = 113,
			items.rename.shortcut_label = 'F2';
			
			items.remove.shortcut = 46,
			items.remove.shortcut_label = 'Del';
			
			if(inst.get_path(node).length == 1){
				// Root should not be deleted
				delete items.remove;
			}
			delete items.ccp; // for simplicity, no Edit Function just dnd plugin will do the trick
			return items;
        }

        function addNode(node, parent, jstreeInst){
        	// assumption is that parentNode is never '#' (null in jstree)
        	if(!jstreeInst){
        		jstreeInst = angular.element.jstree.reference(node);
        	}
        	if(!angular.isObject(parent)){
        		// it's an ParentID
        		parent = jstreeInst.get_json(parent, {no_children: true, no_state: true})
        	}
        	var newNode = {
        		name: node.text
        		, parent: parent.id
//        		, tree_id: parent.data.tree_id
        	}
        	jstreeInst.set_type(node, 'leaf');
        	if(jstreeInst.get_type(parent) === 'leaf'){
    			jstreeInst.set_type(parent, 'node');
    		}
    		jstreeInst.open_node(parent); // might as well do so instead of open_all
    		
        	return treeTagCollectionRestangular.post(newNode)
        					.then(function(data){
//        						node.id = data.id; // huge mistake here, use set_id method!!!
        						jstreeInst.set_id(node, data.id);
//        						node.data = {tree_id: data.tree_id};
//        						node.slug = data.slug;
        						
        						return node;	// return the newly added node
        					}
        					// if we do handle the error here it becomes a promise.resolve
        					// let the controller do the job
//        					, function(error){
//        						return error.data;
//        					}
        					)
        					
    		
        }
        
        function removeNodes(nodes, jstreeInst){
        	var ids = [];
        	if(!angular.isArray(nodes)){
        		nodes = [nodes];
        	}
        	if(!jstreeInst){
        		jstreeInst = angular.element.jstree.reference(nodes[0]);
        	}
        	angular.forEach(nodes, function(node, i){
        		if(!jstreeInst.get_node(node.parent).children.length){
    				jstreeInst.set_type(node.parent, 'leaf');
    			}
        		ids.push(node.id);
        	});
        	return treeTagCollectionRestangular.remove({id: ids})
        						.then(function(){
        							return nodes;
        						});
			//TODO only do a put update to set them inactive
			// not in a on delete_node event but with a menu delete event
//			return treeTagRestangular.put(node)
//									.then(function(data){
//						//				node.id = data.id; // huge mistake here, use set_id method!!!
//										jstreeInst.set_id(node, data.id);
//										node.data = {tree_id: data.tree_id};
//										node.slug = data.slug;
//										
//										return node;	// return the newly added node
//									})
        }
        
        function udpateNode(node, jstreeInst){
        	if(!jstreeInst){
        		jstreeInst = angular.element.jstree.reference(node);
        	}
        	var obj = {}
				, needUpdate = false;
        	var validAttrs = {'id': true
        					, 'text': true
        					, 'slug': true
        					, 'parent': true
        					, 'reslugify': true // special for rename as a temp solution
        					};
        	for(var attr in node){
        		if(!(attr in validAttrs)){
    				continue;
    			}
    			var attrValue = node[attr];
    			if(attr=='parent' && attrValue == '#'){
    				attrValue = null;
    			} else if(attr == 'text') {
    				attr = 'name';
    			}
    			obj[attr] = attrValue;
    			needUpdate = true;
        	}
        	if( needUpdate ){
        		return treeTagInstanceRestangular(node.id).patch(obj)
							.then(function(){
								return node;
							});
        	} else {
        		var deferred = $q.defer();
        		deferred.resolve(node);
        		return deferred.promise;
        	}
        }
        
        function moveNode(node, parent, position, jstreeInst){
        	/* jstree
        	data = {
        			node: node
        			old_instance: $.jstree.plugins.dnd
                	old_parent: "1",
                	old_position: 1,
                	parent: "2",
                	position: 0 index among the siblings
        	}
        	*/
        	/* mptt
        	'first-child'
        	The instance being moved should have target set as its new parent and be placed as its first child in the tree structure.
        	'last-child'
        	The instance being moved should have target set as its new parent and be placed as its last child in the tree structure.
        	'left'
        	The instance being moved should have target‘s parent set as its new parent and should be placed directly before target in the tree structure.
        	'right'
        	The instance being moved should have target‘s parent set as its new parent and should be placed directly after target in the tree structure.
        	*/
        	var elem;
        	if(!jstreeInst){
        		jstreeInst = angular.element.jstree.reference(node);
        	}
        	var parentNode = jstreeInst.get_node(parent);
        	// first-child to a parent target or right to a sibling target 
        	if(position == 0){
        		elem = {
    				target: parent=='#'? null: parent
            		, position: 'first-child'
        		}
        		
        	} else {
        		// get_json was way too detail for this operation
        		// var parentNode = jstreeInst.get_json(parent, {no_data: true, no_state: true});
        		
        		elem = {
        				target: parentNode.children[ position-1 ]
                		, position: 'right'
            		}
        	}
        	jstreeInst.open_node(parentNode);
        	return treeTagInstanceRestangular(node.id).customPUT(
        													elem	// post body
        													, 'move'	// route
        													// , {}	 // query parameter
        													// , {}	 // headers 
        													)
												.then(function(data){
													return node;
												});
        }
        
        // below plural-formed operations are great time cost for the time being
        // mainly because djangorestframework-bulk has a bug that doing bulk update will get failure on unique validation
        // refer to https://github.com/miki725/django-rest-framework-bulk/issues/30
        // TODO 
        function updateNodes(nodes, jstreeInst){
        	var nodeArray = [];
        	if(!angular.isArray(nodes)){
        		nodes = [nodes];
        	}
        	if(!jstreeInst){
        		jstreeInst = angular.element.jstree.reference(nodes[0]);
        	}
        	var validAttrs = {'id': true, 'text': true, 'slug': true, 'parent': true};
        	angular.forEach(nodes, function(node, i){
        		var obj = {}
        			, needUpdate = false;
        		for(var attr in node){
        			if(!(attr in validAttrs)){
        				continue;
        			}
        			var attrValue = node[attr];
        			if(attr=='parent' && attrValue == '#'){
        				attrValue = null;
        			} else if(attr == 'text') {
        				attr = 'name';
        			}
        			obj[attr] = attrValue;
        			needUpdate = true;
        		}
        		if(needUpdate){
        			nodeArray.push(obj);
        		}
        	});
        	
        	if( nodeArray.length>0 ){
        		return treeTagCollectionRestangular.patch(nodeArray)
							.then(function(){
								return nodes;
							});
        	} else {
        		var deferred = $q.defer();
        		deferred.resolve(nodes);
        		return deferred.promise;
        	}
        	
        }
        
        function moveNodes(nodes, jstreeInst){
        	throw 'Not implemented';
        }
        
    }
});