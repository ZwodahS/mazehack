(function() {
    var app = angular.module("maze", []);
    
    app.controller("MazeController", [ "$http", function($http){
        this.instruction = "";
        this.maze_id = "";
        controller = this;
        this.execute = function(){

            controller.result = ""
            controller.logs = []
            $http.get("/execute/"+this.mazeid+"/"+this.instruction).success(function(data){
                controller.result = data["result"]
                if(data["result_code"] == 200){
                    controller.logs = data["logs"]
                }
            }).error(function(data){
                alert(data["error"])
            });
        };
    }]);

    app.directive("log", function(){
        return {
            restrict : "E",
            templateUrl : "/static/html/log.html",
        };
    })
})();
