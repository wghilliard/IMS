'use strict';

/**
 * @ngdoc service
 * @name imsApp.MainService
 * @description
 * # MainService
 * Service in the imsApp.
 */
angular.module('imsApp')
    .service('MainService', function ($http, landingService) {
        // AngularJS will instantiate a singleton by calling "new" on this function
        this.logout = function () {
            return $http.get('/api/logout').then(function () {
                return;
            })
        };

        this.delete = function (username, password) {
           return $http({
                method: 'POST',
                url: 'api/delete',
                data: {
                    'username': username,
                    'password': password
                }
            }).then(function (response) {

                //console.log(response.data);
                return response.data;
            });
        };


        this.check_status = function () {
            return $http.get('/api/generate').then(function (reponse) {
                return reponse.data;
            })
        };

        this.fetchSchedules = function () {
            //var url = '/api/schedules/' + landingService.username;
            return $http.get('/api/schedules').then(function (response) {
                //console.log(response.data);
                return response.data;
            });
        };

        this.postScheduleData = function (blocks, courses, sleep, study, commute) {
            var url = '/api/generate';
            return $http({
                method: 'POST',
                url: url,
                data: {
                    'username': landingService.username,
                    'block_outs': blocks,
                    'classes': courses,
                    'commute': commute,
                    'sleep': sleep,
                    'study': study.toString()
                }
                //,
                //headers: {'Content-Type': 'application/x-www-form-urlencoded'}
            }).then(function (response) {
                //console.log(response.data);
                return response.data;
            });

            //return {
            //    status: 'started'
            //};
        };

        this.deleteSchedule = function (id) {
            return $http.get('/api/schedules/' + id).then(function (response) {
                //console.log(response.data);
                return response.data;
            });
        };


        //this.getScheduleData = function () {
        //    var url = '/api/schedules';
        //    //$http({
        //    //  method: 'GET',
        //    //  url: url,
        //    //  headers: {'Content-Type': 'application/x-www-form-urlencoded'}
        //    //}).then( function (response){
        //    //  return response.data;
        //    //});
        //
        //    return {
        //        status: 'started'
        //    };
        //};


    });
