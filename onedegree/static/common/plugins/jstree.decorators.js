define('common/plugins/jstree.decorators'
       , ['jquery']
       ,  function($) {
   $.jstree.defaults.decorators = {
		 // <selector, handler(node, targetElem)> 
   };
   	
   	// it would keep selected elements under each <li/> persists
   	$.jstree.plugins.decorators = function (options, parent) {
   		
   		this.redraw_node = function(nodeId, deep, is_callback) {
   			var liContainer = parent.redraw_node.call(this, nodeId, deep, is_callback);
   			// after parent.redraw_node.call $node is now an html dom element on <li class="jstree-node"/>
   			if(options){
   				for(var selector in options){
   					// I currently restrict this on children level
   					var targetElem = $(liContainer).children(selector);
   					var handler = options[selector];
   					if(targetElem.length && $.isFunction(handler)){
   						// please be ware of that, the obj is not yet appended to the document
   						handler.call(this, nodeId, liContainer, targetElem);
   					}
   				}
   			}
   			return liContainer;
   		}
   	}
});