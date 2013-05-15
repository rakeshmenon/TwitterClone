/**
 * User: Rakesh Menon
 * Date: 4/22/13
 * Time: 5:47 PM
 */

gymTweeter.directive("timeAgo", function() {
  return {
    restrict: 'A',
    link:function (scope, element, attrs) {
      attrs.$observe("timeAgo", function(value) {
        element.text(moment(new Date(value)).fromNow());
      })
    }
  }
});