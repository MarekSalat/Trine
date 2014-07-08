angular.module('trine')
	.directive('dTransaction', function ()
	{
		return {
	  		restrict: 'E',
	  		scope: {
	  			amount: '@amount',
	  			date: '@date',
	  			guid: '@guid'
	  		},
      		templateUrl: 'directives/transaction.html',
      		link: function (scope, element, attrs) {
      			if (attrs.incomes) {
            	scope.incomes = angular.fromJson(attrs.incomes);	
            	}

            	if (attrs.expenses) {	
            	scope.expenses = angular.fromJson(attrs.expenses);		
            	}
      		},
      		controller: function($scope) {
  				$scope.dateParsed = Date.parse($scope.date);
      		}
      }    
    });