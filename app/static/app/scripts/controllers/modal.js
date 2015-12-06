/**
 * Created by wghilliard on 12/5/15.
 */
'use strict';

/**
 * @ngdoc function
 * @name dqmApp.controller:SelectorCtrl
 * @description
 * # SelectorCtrl
 * Controller of the dqmApp
 */
angular.module('imsApp')
    .controller('ModalCtrl', function ($uibModalInstance, $scope, landingService, MainService) {

        $scope.cancel = function(){
            $uibModalInstance.dismiss();
        };

        $scope.delete = function (){
          MainService.delete($scope.username, $scope.password).then(function(data) {
             //$scope.status = data.status;
              console.log(data.status);
              if (data.status === 'success'){

                  landingService.username = undefined;
                  $uibModalInstance.close();
              }

          });
        };
        $scope.username = landingService.username;
        //$scope.url = data.url;
        //$scope.caption = data.caption;

    });