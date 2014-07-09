var trine = angular.module('trine', ['ngRoute', 'ngResource', 'trine.services', 'trine.directives', 'trine.controllers']);

trine.config(['$routeProvider', function ($routeProvider) {
	$routeProvider.when('/', {
		controller: 'HomeController',
		templateUrl: 'views/home.html'
	})
}]);