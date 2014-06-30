trine.factory('TransactionService', ['$resource', function($resource) {
	return $resource('/api/v1/quick-key/transaction/');
}]);