angular.module('trine')
	.controller('HomeController', ['$scope', 'TransactionService', 
		function($scope, TransactionService) {
			$scope.data = {};
			if (!$scope.data.data) { 
			 	$scope.data.data = TransactionService.get({});
			}	
}]);