angular.module('trine')
	.controller('HomeController', ['$scope', 'TransactionService', 
		function($scope, TransactionService) {
			$scope.data = {};
			$scope.data.clicked = false;

			if (!$scope.data.data) { 
			 	$scope.data.data = TransactionService.get({});
			}	

			$scope.data.showJson = function () {
				$scope.data.clicked = !$scope.data.clicked;
			}
}]);