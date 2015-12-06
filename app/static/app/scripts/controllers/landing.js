'use strict';

/**
 * @ngdoc function
 * @name imsApp.controller:LandingCtrl
 * @description
 * # LandingCtrl
 * Controller of the imsApp
 */
angular.module('imsApp')
    .controller('LandingCtrl', function ($scope, $location, landingService) {
        $scope.stage = '1';

        var current_check = function () {
            landingService.who().then(function (data) {
                console.log(data.username);
                if (data.username !== 'anonymous') {
                    landingService.username = data.username;
                    $location.path("/main");

                }
            })
        };

        current_check();

        $scope.check = function () {
            //console.log('2.0');
            landingService.checkUsername($scope.username).then(function (data) {
                //console.log('data', data);
                if (data.status === 'success') {
                    //User is registered.

                    $scope.stage = '2.1';

                    //$scope.username = username;
                } else {
                    //User is not registered.
                    $scope.stage = '2.2';
                }
                //console.log($scope.stage);
            });

        };

        $scope.login = function () {
            landingService.authenticate($scope.username, $scope.password).then(function (data) {
                if (data.status === 'success') {
                    $scope.error = '';
                    landingService.username = $scope.username;
                    $location.path("/main");
                } else {
                    $scope.error = 'Incorrect password.';
                }
            });


        };

        $scope.register = function () {
            if ($scope.ver_password === $scope.password) {
                $scope.error = '';
                landingService.register($scope.username, $scope.password).then(function (data) {
                    if (data.status === 'success') {
                        landingService.username = $scope.username;
                        $location.path('/main');
                    } else {
                        $scope.error = 'Something went wrong! :(';
                    }
                });

            } else {
                $scope.error = 'Passwords don\'t match!';
            }

        };
    });

