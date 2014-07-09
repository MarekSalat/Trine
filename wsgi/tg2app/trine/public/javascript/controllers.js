angular.module('trine.controllers', [])
	.controller('HomeController', ['$q', '$scope', 'TransactionService', 'TagsService', 
		function($q, $scope, TransactionService, TagsService) {
			$scope.data = {};
			$scope.data.clicked = false;

			if (!$scope.data.transactions) { 
			 	$scope.data.transactions = TransactionService.get({});
			}	

			if (!$scope.data.tags) {
				$scope.data.tags = TagsService.get({});
			}

			$scope.loadItems = function ($query, requiredType) {
				var deferred = $q.defer();
				var tags = [];

				setTimeout(function() {
			      for (i = 0; i < $scope.data.tags.value_list.length; i++) { 
			      	var name = $scope.data.tags.value_list[i].name;
			      	var type = $scope.data.tags.value_list[i].type;

			      	if (type != requiredType) {
			      		continue;
			      	}

			      	if (name.indexOf($query) > -1) {
						tags.push({ text: '' + name + '' });
					}
				}

				deferred.resolve(tags);
				}, 50);

				return deferred.promise;
			};

			$scope.loadIncomeItems = function ($query) {
				return $scope.loadItems($query, 'INCOME');
			};

			$scope.loadExpenseItems = function ($query) {
				return $scope.loadItems($query, 'EXPENSE');
			};

			$scope.data.showJson = function () {
				$scope.data.clicked = !$scope.data.clicked;
			}
}]);