'use strict';

// Auth Controller for the login/Signup page
gymTweeter.controller("AuthCtrl", function ($scope, $location, $http) {
  $scope.radioModel = "Login";
  $scope.showConfirm = false;

  $scope.$watch("radioModel", function (newValue, oldValue) {
    switch($scope.radioModel) {
      case "Login" : $scope.showConfirm = false;
                     $scope.authUrl = "/user/login";
                     break;
      case "Signup": $scope.showConfirm = true;
                     $scope.authUrl = "/user/register";
                     break;
    }
  });

  $scope.checkCredentials = function () {
    $http({
      method: 'POST',
      url: $scope.authUrl,
      data: $scope.user
    }).success(function(data) {
        $location.path("home");
    });
  };
});

// Controller for the user's home page
gymTweeter.controller("HomeCtrl", function ($scope, $resource) {
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

// Controller to retrieve the User's Details
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

// Controller for posting a tweet
gymTweeter.controller("TweetPostCtrl", function ($scope, $location, $http) {
  $scope.postTweet = function () {
    $http({
      method: 'POST',
      url: "/tweet/add",
      data: {
        content: $scope.tweet_text,
        csrfmiddlewaretoken: readCookie("csrftoken")
      }
    }).success(function(data) {
      $scope.tweet_text = "";
      $scope.$emit('tweeted');
    });
  }
});

// Controller for the currentuser-only tweets
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
