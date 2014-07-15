angular.module('trine.services', [])

.factory('TransactionService', ['$resource', function($resource) {

return $resource('/api/v1/quick-key/transaction/', {}, {
      get: {
        method: 'GET',
        params: { },
        headers: { 'Content-Type': 'application/json;charset=utf-8' }
      }
    });
}]).factory('TagsService', ['$resource', function($resource) {

return $resource('/api/v1/quick-key/tag/', {}, {
      get: {
        method: 'GET',
        params: { },
        headers: { 'Content-Type': 'application/json;charset=utf-8' }
      }
    });
}]).factory('_', function() {
    return window._;
});