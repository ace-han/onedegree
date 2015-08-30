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
        		, deleteNodeCB: deleteNodeCB
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
        
        function saveTreeChangeStatus(changedNodes){
        	// this maybe slow if the amount of the nodes is large
        	vm.lastEditData = angular.element.jstree.reference(vm.treeInstance).get_json();
        	var msgs = ['Change applied. Nodes:'];
        	if(!angular.isArray(changedNodes)){
        		changedNodes = [changedNodes];
        	}
        	angular.forEach(changedNodes, function(e, i){
        		msgs.push(e.text + '('+e.id + ')\n');
        	});
        	humane.log(msgs.join(' '));
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
        
        // delegate the menu settings
        function deleteNodeCB(event, data) {
        	// TODO, for the simplicity, just hard delete it for the time being
        	treeTagService.removeNodes(data.node)
				.then(saveTreeChangeStatus, rollbackTreeNodeOperation);
        	
        }
        
        function renameNodeCB(event, data) {
        	// since slug need to be unique in server, 
        	// and no other place in this tree view to rename the slug
        	// might as well do it so
        	data.node.reslugify = true;	
        	treeTagService.updateNode(  data.node )
        				.then(saveTreeChangeStatus, rollbackTreeNodeOperation);
        }
		
        function moveNodeCB(event, data) {
        	treeTagService.moveNode(  data.node, data.parent, data.position )
							.then(saveTreeChangeStatus, rollbackTreeNodeOperation);
        }
    }

});
