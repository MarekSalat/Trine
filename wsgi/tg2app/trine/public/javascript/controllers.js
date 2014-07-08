angular.module('trine')
	.controller('HomeController', ['$scope', 'TransactionService', 'testValue', 
		function($scope, TransactionService, testValue) {
			$scope.data = {};
			$scope.data.welcome = 'hellllloooo';

			$scope.data.clic = testValue;

			if (!$scope.data.data) { 
			 	$scope.data.data = TransactionService.get({});
			}	
}]);