'use strict';

//Controllers

gymTweeter.controller("UserDetailsCtrl", function ($scope, $location, $resource) {
  $scope.userInfo = $resource(
    '/user/profile', {},
    {
      getUserDetails: {
        method: 'GET'
      }
    }
  );

  $scope.userDetails = $scope.userInfo.getUserDetails();
});

gymTweeter.controller("AuthCtrl", function ($scope, $location, $http) {
  $scope.radioModel = "Login";
  $scope.confirmHidden = "hidden"

  $scope.$watch("radioModel", function (newValue, oldValue) {
    switch($scope.radioModel) {
      case "Login" : $scope.confirmHidden = "hidden";
                     $scope.authUrl = "/user/login";
                     break;
      case "Signup": $scope.confirmHidden = "";
                     $scope.authUrl = "/user/register";
                     break;
    }
  });

  $scope.checkCredentials = function () {
    $http({
      method: 'POST',
      url: $scope.authUrl,
      data: $scope.user,
      headers: {'Content-Type': 'application/x-www-form-urlencoded'}
    }).success(function(data) {
      $location.path("home");
    });
  };
});

gymTweeter.controller("TweetPostCtrl", function ($scope, $location, $http) {
  $scope.postTweet = function () {
    $http({
      method: 'POST',
      url: "/tweet/add",
      data: {
        content: $scope.tweet_text,
        csrfmiddlewaretoken: readCookie("csrftoken")
      },
      headers: {
        'Content-Type': 'application/x-www-form-urlencoded',
      }
    }).success(function(data) {
      $scope.$emit('tweeted');
    });
  }
});

gymTweeter.controller("SelfCtrl", function ($scope, $location, $resource) {
  $scope.userActive = "active";

  $scope.gtweet = $resource(
    '/tweet/self', {},
    {
      get: {
        method: 'GET',
        isArray: false
      }
    }
  );

  $scope.gtweet.get(function(data) {
    $scope.gtweetResult = data;
  });

  $scope.$on('tweeted', function () {
    $scope.gtweet.get(function(data) {
      $scope.gtweetResult = data;
    });
  });
});


gymTweeter.controller("UserCtrl", function ($scope, $location, $resource, $routeParams) {
  $scope.gtweet = $resource(
    'http://search.twitter.com/:action',
    {
      action: "search.json",
      q: $routeParams.id,
      callback: 'JSON_CALLBACK'
    },
    {
      get: {
        method: 'JSONP'
      }
    }
  );

  $scope.gtweetResult = $scope.gtweet.get();
});


gymTweeter.controller("HomeCtrl", function ($scope, $location, $resource) {
  $scope.homeActive = "active";

  $scope.gtweet = $resource(
    '/tweet/all', {},
    {
      get: {
        method: 'GET',
        isArray: false
      }
    }
  );

  $scope.gtweet.get(function(data) {
    $scope.gtweetResult = data;
  });

  $scope.$on('tweeted', function () {
    $scope.gtweet.get(function(data) {
      $scope.gtweetResult = data;
    });
  });
});