trine.controller('HomeController', ['$scope', 'TransactionService', function($scope, TransactionService) {
	$scope.data = {};
	$scope.data.welcome = 'hellllloooo';
	TransactionService.get({}, function (data) {
		$scope.data.data = data;
	});
}]);