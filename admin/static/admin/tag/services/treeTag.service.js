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
        				});
        				return treeTags;
        			});
        			//}).$object; // do not do this to break the filtered response-treeTags
        }

        function getTreeConfig(){
        	var treeConfig = {
                    core : {
                        multiple : false,
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
                    version : 1,
                    plugins : ['types', 'contextmenu', 'unique', 'dnd' ]
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
			return items;
        }

    }
});