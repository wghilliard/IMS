'use strict';

/**
 * @ngdoc function
 * @name imsApp.controller:MainCtrl
 * @description
 * # MainCtrl
 * Controller of the imsApp
 */
angular.module('imsApp')
    .controller('MainCtrl', function ($scope, $uibModal, $location, $interval, landingService, MainService) {
        var login_check = function () {
            if (landingService.username === undefined) {
                $location.path('/landing');
            } else {
                landingService.who().then(function (data) {
                    if (data.username !== 'anonymous') {
                        console.log(data);
                        landingService.username = data.username;
                        $scope.username = data.username;
                    }

                });

            }
        };


        login_check();

        //$scope.username = 'Tester';
        $scope.stage = '1';
        $scope.schedules = MainService.fetchSchedules();
        $scope.blocks = [];
        $scope.courses = [];
        $scope.model = {
            course: {},
            block: {
                sTime: new Date(1970, 0, 1, "06", "00", "00"),
                eTime: new Date(1970, 0, 1, "07", "00", "00"),
                //eTime: "23:59"
            },
            commute: {
                workToHome: 0,
                workToSchool: 0,
                homeToSchool: 0
            },
            study: 0

        };
        $scope.fetch = {};


        var refresh = function () {
            //console.log("something_happened");
            if (landingService.username !== undefined) {
                MainService.fetchSchedules().then(function (data) {
                    $scope.fetch.schedules = data.schedules;
                })
            }
        };

        $scope.notifications = [];

        var addNotification = function (notification, type) {
            if ($scope.notifications.length === 10) {
                $scope.notifications.pop();
            }
            $scope.notifications.unshift({
                text: notification,
                type: type
            });
        };

        $scope.addBlock = function () {
            if (($scope.model.block.name !== undefined) && ($scope.model.block.location !== undefined)) {
                if ($scope.model.block.sTime < $scope.model.block.eTime) {
                    if ($scope.model.block.repetition !== undefined) {
                        $scope.blocks.unshift({
                            name: $scope.model.block.name,
                            location: $scope.model.block.location,
                            sTime: $scope.model.block.sTime,
                            eTime: $scope.model.block.eTime,
                            repetition: {
                                "mon": $scope.model.block.repetition.mon,
                                "tues": $scope.model.block.repetition.tues,
                                "weds": $scope.model.block.repetition.weds,
                                "thurs": $scope.model.block.repetition.thurs,
                                "fri": $scope.model.block.repetition.fri,
                                "sat": $scope.model.block.repetition.sat,
                                "sun": $scope.model.block.repetition.sun
                            }
                        });
                        console.log($scope.model.block);
                        $scope.model.block = {
                            sTime: new Date(1970, 0, 1, "06", "00", "00"),

                        };
                        addNotification('Block Added!', 'success');
                        $scope.error = undefined;
                    } else {
                        addNotification('One day must be selected at a minimum.', 'danger');
                    }

                } else {
                    addNotification('Start Time must be less than End Time.', 'danger');
                    //$scope.error = 'Start Time must be less than End Time.';
                }
            } else {
                addNotification('Name and Location are required.', 'danger');
                //$scope.error = 'Name and Location are required.';
            }
        };

        $scope.removeBlock = function (index) {
            $scope.blocks.splice(index, 1);
            addNotification('Block Removed!', 'warning');
        };

        $scope.addCourse = function () {
            if (($scope.model.course.name !== undefined) && ($scope.model.course.number !== undefined)) {
                $scope.courses.unshift({
                    name: $scope.model.course.name,
                    number: $scope.model.course.number
                });
                $scope.model.course = {};
                addNotification('Course Added!', 'success');
            } else {
                addNotification('Course Department Name and Course Number are required.', 'danger');
            }
            $scope.model.rec_study = $scope.courses.length * 3;
        };

        $scope.removeCourse = function (index) {
            $scope.courses.splice(index, 1);
            addNotification('Course Removed!', 'warning');
        };

        $scope.$watch(function (scope) {
            return scope.model.sleep;
        }, function (sleep) {
            if (sleep < 6) {

                $scope.model.sleep = 6;

                addNotification('Sleep too low! Must be in range 6-13!', 'warning');
            } else if (sleep > 13) {
                addNotification('Sleep too high! Must be in range 6-13!', 'warning');
                $scope.model.sleep = 13;
            } else if (sleep === undefined) {
                $scope.model.sleep = 6;
            }


        });

        $scope.$watch(function (scope) {
            return scope.model.block.eTime;
        }, function (eTime) {
            console.log(eTime);
            if (eTime === undefined) {
                return;
            }

            if ( eTime < $scope.model.block.sTime) {
                addNotification('End Time not possible!', 'warning');
                //$scope.model.block.sTime = new Date(1970, 0, 1, "23", "00", "00");


            }
        });


        $scope.generateSchedule = function () {

            if ($scope.courses.length !== 0 && $scope.courses !== undefined) {
                MainService.postScheduleData($scope.blocks, $scope.courses, $scope.model.sleep, $scope.model.study, $scope.model.commute).then(function (data) {
                    if (data.status === 'started') {
                        addNotification('Schedule Generation Started!', 'success');
                    } else if (data.status === 'failed') {
                        addNotification(data.error, 'danger');
                    }
                });

            } else {
                addNotification('Minimum of 1 Course needed.', 'warning');
            }


        };

        $scope.get_sched_color = function (bool) {
            if (bool === true) {
                return 'success';
            } else {
                return 'danger';
            }

        };

        $scope.get_color = function (test) {
            switch (test) {
                case 'sleep':
                    return 'grey';
                case 'class':
                    return '#FF880F';
                case 'commute':
                    return '#4385FF';
                case 'study':
                    return '#5DA7BB';
                case 'work':
                    return '#FF5A3D';
                default:
                    return '#ED2EFF';
            }
        };
        $scope.set_sched = function (index) {
            var holder = $scope.fetch.schedules[index];
            $scope.stage = 2;
            $scope.fetch.schedule = {
                "name": holder.name,
                "days": [
                    ["monday", holder.monday],
                    ["tuesday", holder.tuesday],
                    ["wednesday", holder.wednesday],
                    ["thursday", holder.thursday],
                    ["friday", holder.friday],
                    ["saturday", holder.saturday],
                    ["sunday", holder.sunday]
                ],
                "id": holder._id
            };
            console.log($scope.fetch.schedule);
        };

        $scope.cal_min_height = function (t) {
            if (t === 'class') {
                return "90px";
            } else {
                return "50px";
            }
        };

        $scope.logout = function () {
            MainService.logout().then(function () {
                landingService.username = undefined;
                $location.path('/landing');
            });
        };
        $scope.set_stage = function (number) {
            console.log(number);
            $scope.stage = number;
        };


        $interval(function () {
            if (landingService.username !== undefined) {

                MainService.check_status().then(function (data) {
                    refresh();
                    //console.log(data);
                    switch (data.status) {
                        case 'not_started':
                            $scope.status = 'glyphicon-ok';
                            return;
                        case 'failed':
                            addNotification(data.error, 'danger');
                            return;
                        case 'busy':
                            $scope.status = 'glyphicon-time';
                            return;
                        case 'working':
                            $scope.status = 'glyphicon-pencil';
                            return;
                        default:
                            console.log(data);
                            $scope.status = 'glyphicon-asterisk';
                            return;
                    }
                });
            }

        }, 1000);

        $scope.deleteSchedule = function (id) {
            MainService.deleteSchedule(id).then(function (data) {
                if (data.status === 'success') {
                    addNotification('Schedule Deleted!', 'success');
                } else {
                    addNotification('Something went wrong! :(', 'danger');
                }
            });
        };


        $scope.user_modal = function () {
            var modalInstance = $uibModal.open({
                templateUrl: 'static/app/views/templates/image-modal.html',
                controller: 'ModalCtrl',
                resolve: {
                    data: function () {
                        return {
                            username: $scope.username
                        };
                    }
                },
                size: 'lg'

            });

            modalInstance.result.then(function () {
                console.log(landingService.username);
                //login_check();
            });
        };


        refresh();
    });
