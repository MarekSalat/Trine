angular.module('trine.directives', ['ngTagsInput'])
	.directive('dTransaction', ['_', function (_)
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

            	scope.dateParsed = Date.parse(scope.date);
      		}
      }    
    }]).directive('dTag', ['_', function (_) {
        return {
            restrict: 'E',
            scope: {
                name: '@name',
                type: '@type',
                incomeTags: '=',
                expenseTags: '='
            },
            templateUrl: 'directives/tag.html',
            link: function (scope, element, attrs) {
                scope.typeLower = scope.type.toLowerCase();

                scope.addToTags = function () {
                    var value = {text: scope.name};

                    if (scope.incomeTags) {
                        if (_.where(scope.incomeTags, value).length === 0) {
                            scope.incomeTags.push(value);
                        }
                        else {
                            scope.incomeTags = _.filter(scope.incomeTags, function (tag) { return tag.text !== scope.name});
                        }
                    }

                    if (scope.expenseTags) {
                        if (_.where(scope.expenseTags, value).length === 0) {
                            scope.expenseTags.push(value);
                        }
                        else {
                            scope.expenseTags = _.filter(scope.expenseTags, function (tag) { return tag.text !== scope.name});
                        }
                    }
                }
            }
        }}]);