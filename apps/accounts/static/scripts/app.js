'use strict';

function readCookie(name) {
  var nameEQ = name + "=";
  var ca = document.cookie.split(';');
  for(var i = 0; i < ca.length; i++) {
    var c = ca[i];
    while (c.charAt(0) === ' ') c = c.substring(1, c.length);
    if (c.indexOf(nameEQ) === 0) return c.substring(nameEQ.length, c.length);
  }
  return null;
}

var gymTweeter = angular.module('GymTweeterApp', ['ngResource', 'ui.bootstrap']);

/**
 * Route configuration
 */
gymTweeter.config(function ($routeProvider, $httpProvider) {
  $routeProvider
    .when('/', {
      templateUrl: '/static/views/main.html',
      controller: 'AuthCtrl'
    })
    .when('/home/', {
      templateUrl: '/static/views/home.html',
      controller: 'HomeCtrl'
    })
    .when('/me/', {
      templateUrl: '/static/views/me.html',
      controller: 'SelfCtrl'
    })
    .when('/user/:id', {
      templateUrl: '/static/views/user.html',
      controller: 'UserDetailsCtrl'
    })
    .otherwise({
      redirectTo: '/'
    });

  // Use x-www-form-urlencoded Content-Type
  $httpProvider.defaults.headers.post['Content-Type'] = 'application/x-www-form-urlencoded;charset=utf-8';

  // Tranform JSON params to Parameter string for server comprehension
  $httpProvider.defaults.transformRequest = function(data){

    if (data === undefined) {
        return data;
    }

    return $.param(data);
  };
});
