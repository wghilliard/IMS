'use strict';

/**
 * @ngdoc service
 * @name imsApp.LandingService
 * @description
 * # LandingService
 * Service in the imsApp.
 */
angular.module('imsApp')
    .factory('landingService', function ($http) {
        // AngularJS will instantiate a singleton by calling "new" on this function
        var landingService = {};
        landingService.checkUsername = function (username) {
            return $http({
                method: 'POST',
                url: '/api/username',
                data: $.param({'username': username}),
                headers: {'Content-Type': 'application/x-www-form-urlencoded'}
            }).then(function (response) {
                return response.data;
            });
        };

        landingService.who = function (){
            return $http.get('/api/who').then(function(response){
                //console.log(response.data);
                return response.data
            })
        };

        landingService.authenticate = function (username, password) {
            //TODO: test this
            return $http({
                method: 'POST',
                url: '/api/login',
                data: $.param({'username': username, 'password': password}),
                headers: {'Content-Type': 'application/x-www-form-urlencoded'}
            }).then(function (response) {
                //console.log(response.data);
                return response.data;
            });
            //this.username = username;
            //return 'true';
        };

        landingService.register = function (username, password) {
            //TODO: test this
            return $http({
                method: 'POST',
                url: '/api/register',
                data: $.param({'username': username, 'password': password}),
                headers: {'Content-Type': 'application/x-www-form-urlencoded'}
            }).then(function (response) {
                //console.log(response.data);
                return response.data;
            });
            //this.username = username;
            //return 'true';
        };

        return landingService;
    });
