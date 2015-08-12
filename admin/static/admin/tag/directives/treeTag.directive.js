
define([
    '../module'
],
function (module) {
    'use strict';
    
    // see to 

    module.directive('cmnFocusMe', cmnFocusMe);

	cmnFocusMe.$inject = ['$timeout'];

    return cmnFocusMe;

	function cmnFocusMe($timeout){
		var directive = {
			restrict: 'A'
			, scope: {trigger: '@cmnFocusMe'}
			, link: linkFunc
		}
		return directive;

		function linkFunc($scope, $element, $attrs, $controller) {
			$scope.$watch('trigger', function(value) {
		        if (value === "true") {
		    		$timeout(function() {
		  				$element[0].focus();
		  			// add a time for like right now make it focus working
		  			// add another attr to delay focus event
         			}, 100);
    			}
			});
		};
	}
});
