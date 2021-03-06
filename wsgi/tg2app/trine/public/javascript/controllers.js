angular.module('trine.controllers', [])
    .controller('HomeController', ['$q', '$scope', 'TransactionService', 'BalancesService', 'UserService', 'TagsService', '_',
        function ($q, $scope, TransactionService, BalancesService, UserService, TagsService, _) {
            $scope.data = {};
            $scope.data.clicked = false;

            if (!$scope.data.transactions) {
                $scope.data.transactions = TransactionService.get({});
            }

            if (!$scope.data.balances) {
                $scope.data.balances = BalancesService.get({});
            }

            if (!$scope.data.user) {
                $scope.data.user = UserService.get({});
            }

            if (!$scope.data.tags) {
                TagsService.get({}, function (data) {
                    $scope.data.tags = data;

                    $scope.data.income = _.filter(data.value_list, function (val) {
                        return val.type == 'INCOME';
                    });
                    $scope.data.expense = _.filter(data.value_list, function (val) {
                        return val.type == 'EXPENSE';
                    });
                });
            }

            $scope.loadItems = function ($query, requiredType) {
                var deferred = $q.defer();
                var tags = [];

                setTimeout(function () {
                    _.each($scope.data.tags.value_list, function (val) {
                        var name = val.name;
                        var type = val.type;

                        if (type == requiredType) {
                            if (name.indexOf($query) > -1) {
                                tags.push({ text: '' + name + '' });
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
                    $scope.data.transactions.value_list.push(result.value);
                });
            };
        }]);