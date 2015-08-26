define([
    'angular'
    , '../module'
    , '../namespace'
    
],
function (angular, module, namespace) {
    'use strict';

    var name = namespace + '.TreeTagService';

    module.factory(name, TreeTagService);

    TreeTagService.$inject = ['Restangular'];

    return TreeTagService;

    function TreeTagService(Restangular){

    	//var treeTagRestService = Restangular.service('tree-tags', Restangular.all(namespace));
    	//var treeTagRestangular = Restangular.all(namespace).all('tree-tags')
    	//var treeTagRestangular = Restangular.allUrl('tree-tags', 'http://http://localhost:8090/api/v1/admin/tag/tree-tags/');
    	var treeTagRestangular = Restangular.withConfig(function(RestangularConfigurer) {
    		// this one will strip other unnecessary data meta
    		RestangularConfigurer.setFullResponse(false);	
    	  });
//    	var treeTagRestangular = Restangular.setFullResponse(false).all(namespace).all('tree-tags');
    	//var treeTagRestangular = Restangular.all(namespace).all('tree-tags')
    	treeTagRestangular = treeTagRestangular.all(namespace).all('tree-tags');
    	var service = {
        	getAllTreeTags: getAllTreeTags
            , getTreeConfig: getTreeConfig
            , addNode: addNode
            , removeNodes: removeNodes
        }

        return service;
    	
        function getAllTreeTags(){
        	// set the page_size insanely large to retrieve them all
        	return treeTagRestangular.getList({page_size: 100000})
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
        					treeTag.data = {tree_id: treeTag.tree_id};
        				});
        				return treeTags;
        			});
        			//}).$object; // do not do this to break the filtered response-treeTags
        }

        function getTreeConfig(){
        	// write this way already make it new an object every time
        	var treeConfig = {
                    core : {
                        multiple : true,
                        animation: true,
                        error : function(error) {
                        	console.errror('treeCtrl: error from js tree - ' + error);
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
                    plugins: ['types', 'contextmenu', 'unique', 'dnd' ],
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
        		, tree_id: parent.data.tree_id
        	}
        	jstreeInst.set_type(node, 'leaf');
        	if(jstreeInst.get_type(parent) === 'leaf'){
    			jstreeInst.set_type(parent, 'node');
    		}
    		jstreeInst.open_node(parent); // might as well do so instead of open_all
    		
        	return treeTagRestangular.post(newNode)
        					.then(function(data){
//        						node.id = data.id; // huge mistake here, use set_id method!!!
        						jstreeInst.set_id(node, data.id);
        						node.data = {tree_id: data.tree_id};
        						node.slug = data.slug;
        						
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
        	if(!jstreeInst){
        		jstreeInst = angular.element.jstree.reference(nodes[0]);
        	}
        	angular.forEach(nodes, function(node, i){
        		jstreeInst.delete_node(node);
        		if(!jstreeInst.get_node(node.parent).children.length){
    				jstreeInst.set_type(node.parent, 'leaf');
    			}
        	});
        	
			
			
			// only do a put update to set them inactive
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
        
    }
});