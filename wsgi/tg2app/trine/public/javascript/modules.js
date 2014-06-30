var trine = angular.module('trine', ['ngRoute', 'ngResource']);

trine.config(['$routeProvider', function ($routeProvider) {
	$routeProvider.when('/', {
		controller: 'HomeController',
		templateUrl: 'views/home.html'
	})
}]);