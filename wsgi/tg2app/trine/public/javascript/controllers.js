angular.module('trine.controllers', [])
	.controller('HomeController', ['$q', '$scope', 'TransactionService', 'TagsService', '_',
		function($q, $scope, TransactionService, TagsService, _) {
            $scope.data = {};
			$scope.data.clicked = false;

			if (!$scope.data.transactions) { 
			 	TransactionService.get({}, function (data) {
                    $scope.data.transactions = data.value_list;
                });
			}	

			if (!$scope.data.tags) {
				TagsService.get({}, function (data) {
                    $scope.data.tags = data.value_list;

                    $scope.data.income = _.filter($scope.data.tags, function (tag) { return tag.type == 'INCOME'; });
                    $scope.data.expense = _.filter($scope.data.tags, function (tag) { return tag.type == 'EXPENSE'; });
                });
			}

			$scope.loadItems = function ($query, requiredType) {
				var deferred = $q.defer();
				var tags = [];

				setTimeout(function() {
                    _.each($scope.data.tags, function (tag) {
                        if (tag.type == requiredType) {
                            if (tag.name.indexOf($query) > -1) {
                                tags.push({ text: tag.name });
                            }
                        }
                    });

                deferred.resolve(tags);
				}, 10);

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

            $scope.saveTransaction = function () {
                var transaction = {
                    amount: $scope.data.new.amount,
                    date: Math.floor(Date.now() / 1000),
                    incomeTagGroup: _.pluck($scope.data.new.incomeTags, 'text'),
                    expenseTagGroup: _.pluck($scope.data.new.expenseTags, 'text')
                };

                TransactionService.post(transaction, function (result) {
                    $scope.data.transactions.push(result.value);
                });
            };
}]);