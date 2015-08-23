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
    	
    	var originalData = treeTagJson;
    	var treeData = [];
    	var treeConfig = treeTagService.getTreeConfig();
    	
        var vm = this, 
        	controller = {
        		ignoreChanges: false
        		, newNode: {}
        		, originalData: originalData
        		, treeData: treeData
        		, treeConfig: treeConfig
        		, applyModelChanges: applyModelChanges
        		, reCreateTree: reCreateTree
        		, simulateAsyncData: simulateAsyncData 
        		, addNewNode: addNewNode
        		, setNodeType: setNodeType
        		, readyCB: readyCB
        		, createNodeCB: createNodeCB
        		, pasteCB: pasteCB
        		, moveNodeCB: moveNodeCB
        		, deleteNodeCB: deleteNodeCB
        		
        	};
        
        angular.copy(originalData, treeData);
        
        
        angular.extend(vm, controller);
        
        return vm;
        
        // should do move all the operations to service level
        // controller holds a copy for the lasttime edit jstreeData
        // if anything does not work out on service level recreate the tree with lasttime edit jstreeData
        // or re-assign the jstreeData to controller.treeData and vm.ignoreChanges=false to do the re-recreation
        var newId = 1;
        
        function applyModelChanges() {
            return !vm.ignoreChanges;
        }
        
        function reCreateTree() {
            vm.ignoreChanges = true;
            angular.copy(vm.originalData,vm.treeData);
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


        function setNodeType() {
            var item = _.findWhere(this.treeData, { id : this.selectedNode } );
            item.type = this.newType;
            //toaster.pop('success', 'Node Type Changed', 'Changed the type of node ' + this.selectedNode);
            console.info('Node Type Changed', 'Changed the type of node ' + this.selectedNode);
        }

        function readyCB() {
            $timeout(function() {
                vm.ignoreChanges = false;
                //toaster.pop('success', 'JS Tree Ready', 'Js Tree issued the ready event')
                console.info('JS Tree Ready', 'Js Tree issued the ready event')
            });
        }
        
        function createNodeCB(event, data) {
        	console.info('createNodeCB');
        	humane.log('createNodeCB');
        	var jstreeInst = data.instance;
			jstreeInst.set_type(data.node, 'leaf');
			if(jstreeInst.get_type(data.parent) === 'leaf'){
				jstreeInst.set_type(data.parent, 'node');
			}
			jstreeInst.open_node(data.parent); // might as well do so instead of open_all
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
