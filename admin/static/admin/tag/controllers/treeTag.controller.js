define([
    'angular'
    , '../module'
    , '../namespace'
],
function (angular, module, namespace) {
    'use strict';

    var name = namespace + '.TreeTagController';

    module.controller(name, TreeTagController);
                
    TreeTagController.$inject = ['$timeout', 'common.HumaneService', 'treeTagJson', 'tag.TreeTagService' ];

    return TreeTagController;

    function TreeTagController($timeout, humane, treeTagJson, treeTagService) {
    	
    	var lastEditData = treeTagJson;
    	var treeData = [];
    	var treeConfig = treeTagService.getTreeConfig();
    	
        var vm = this, 
        	controller = {
        		ignoreChanges: false
        		, newNode: {}
        		, lastEditData: lastEditData
        		, treeData: treeData
        		, treeConfig: treeConfig
        		, applyModelChanges: applyModelChanges
        		, reCreateTree: reCreateTree
        		, readyCB: readyCB
        		, createNodeCB: createNodeCB
        		, renameNodeCB: renameNodeCB
        		, moveNodeCB: moveNodeCB
        		
        	};
        
        angular.copy(lastEditData, treeData);
        
        
        angular.extend(vm, controller);
        
        return vm;
        
        // should do move all the operations to service level
        // controller holds a copy for the lasttime edit jstreeData
        // any change to the treeData will directly reflected in the tree...
        // if anything does not work out on service level recreate the tree with lasttime edit jstreeData
        // for tree re-recreation ngJsTree has it's own way (using version property in config)
        // only notification on failure operations
        
        function applyModelChanges() {
            return !vm.ignoreChanges;
        }
        
        function saveTreeStatus(newNode){
        	// special for newly added node, without notification
        	vm.lastEditData = angular.element.jstree.reference(vm.treeInstance).get_json();
        }
        
        function saveTreeChangeStatus(changedNode){
        	// this maybe slow if the amount of the nodes is large
        	vm.lastEditData = angular.element.jstree.reference(vm.treeInstance).get_json();
        	humane.log('Change applied. ' + changedNode.text + '('+changedNode.id + ')');
        }
        
        function rollbackTreeNodeOperation(error){
        	reCreateTree();
            humane.error('Server Change failed! ' + angular.toJson(error.data) ); 
        }
        
        function reCreateTree() {
            vm.ignoreChanges = true;
            angular.copy(vm.lastEditData, vm.treeData);
            vm.treeConfig.version++;
        }

        function readyCB() {
            $timeout(function() {
                vm.ignoreChanges = false;
                var jstreeInst = angular.element.jstree.reference(vm.treeInstance);
                jstreeInst.open_all();
            });
        }
        
        function createNodeCB(event, data) {
        	treeTagService.addNode(data.node, data.node.parent)
        					.then(saveTreeStatus, rollbackTreeNodeOperation);
        }
        
        function renameNodeCB(event, data) {
        	console.log('renameNodeCB');
        	console.log(event);
        	console.log(data);
        }
		
        function moveNodeCB(event, data) {
        	console.info('moveNodeCB');
        	/*
        	data = {
        			node: node
        			old_instance: $.jstree.plugins.dnd
                	old_parent: "1",
                	old_position: 1,
                	parent: "2",
                	position: 0,
        	}
        	*/
        	var jstreeInst = data.instance;
			if(!jstreeInst.get_node(data.old_parent).children.length){
				jstreeInst.set_type(data.old_parent, 'leaf');
			}
			if(jstreeInst.get_type(data.parent) === 'leaf'){
				jstreeInst.set_type(data.parent, 'node');
			}
			jstreeInst.open_node(data.parent);
        }
		
        // delegate the menu settings
//        function deleteNodeCB(event, data) {
//        	console.info(data.node.text);
//        	
//        	//treeTagService.removeNode(data.node)
//				//.then(saveTreeChangeStatus, rollbackTreeNodeOperation);
//        	
//        }        
    }

});
