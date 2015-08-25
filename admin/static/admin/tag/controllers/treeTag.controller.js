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
        		, simulateAsyncData: simulateAsyncData 
        		, addNewNode: addNewNode
        		, readyCB: readyCB
        		, createNodeCB: createNodeCB
        		, pasteCB: pasteCB
        		, moveNodeCB: moveNodeCB
        		, deleteNodeCB: deleteNodeCB
        		
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
        
        function saveTreeStatus(changedNode){
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

        function simulateAsyncData() {
            vm.promise = $timeout(function(){
                vm.treeData.push({ id : (newId++).toString(), parent : vm.treeData[0].id, text : 'Async Loaded' })
            },3000);
        }
        
        function addNewNode() {
            vm.treeData.push({ id : (newId++).toString(), parent : vm.newNode.parent, text : vm.newNode.text });
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
        					.then(saveTreeStatus, rollbackTreeNodeOperation)
        }
        
        function pasteCB(event, data) {
        	console.info('pasteCB');
        	var jstreeInst = data.instance;
			for(var i=0; i<data.node.length; i++){
				if(!jstreeInst.get_node(data.node[i].parent).children.length){
					jstreeInst.set_type(data.node[i].parent, 'leaf');
				}
			}
			
			if(jstreeInst.get_type(data.parent) === 'leaf'){
				jstreeInst.set_type(data.parent, 'node');
			}
			jstreeInst.open_node(data.parent);
        }
		
        function moveNodeCB(event, data) {
        	console.info('moveNodeCB');
        	var jstreeInst = data.instance;
			if(!jstreeInst.get_node(data.old_parent).children.length){
				jstreeInst.set_type(data.old_parent, 'leaf');
			}
			if(jstreeInst.get_type(data.parent) === 'leaf'){
				jstreeInst.set_type(data.parent, 'node');
			}
			jstreeInst.open_node(data.parent);
        }
		
        function deleteNodeCB(event, data) {
        	console.info('deleteNodeCB');
        	var jstreeInst = data.instance;
			if(!jstreeInst.get_node(data.node.parent).children.length){
				jstreeInst.set_type(data.node.parent, 'leaf');
			}
        }        
    }

});
