(function() 
{
    var app = angular.module("user", []);

    app.directive("usersPanel", function()
    {
        return {
            restrict : "E",
            templateUrl : "/static/html/userspanel.html",
            controller : [ "$http", function($http)
            {
                var controller = this;
                this.searchField = {};
                this.userslist = [];
                $http.get("/userslist").success(function(data)
                    {
                        controller.userslist = data["users"];
                    });

                this.setSelectedUser = function(user)
                {
                    this.selectedUser = user;
                };

                this.search = function(){
                    $http.get("/users?email="+this.searchField.email).success(function(data)
                        {
                            controller.userslist = data["users"];
                        });
                };
            }],
            controllerAs : "usersCtrl",
        };
    });
})();
