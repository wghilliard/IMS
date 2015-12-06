'use strict';

/**
 * @ngdoc overview
 * @name imsApp
 * @description
 * # imsApp
 *
 * Main module of the application.
 */
angular
    .module('imsApp', [
        'ngRoute',
        'ui.bootstrap',
        'mgcrea.ngStrap'
    ])
    .config(function ($routeProvider) {
        $routeProvider

            .when('/main', {
                templateUrl: 'static/app/views/main.html',
                controller: 'MainCtrl',
                controllerAs: 'main'
            })
            .when('/about', {
                templateUrl: 'static/app/views/about.html',
                controller: 'AboutCtrl',
                controllerAs: 'about'
            })
            .when('/landing', {
                templateUrl: 'static/app/views/landing.html',
                controller: 'LandingCtrl',
                controllerAs: 'landing'
            })
            .otherwise({
                redirectTo: '/landing'
            });
    }).filter('capitalize', function () {
    return function (input) {
        return (!!input) ? input.charAt(0).toUpperCase() + input.substr(1).toLowerCase() : '';
    };
});
