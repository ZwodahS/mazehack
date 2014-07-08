(function() {
    var app = angular.module("maze", []);
    
    app.controller("MazeController", [ "$http", function($http){
        this.instruction = "";
        this.maze_id = "";
        controller = this;
        this.execute = function(){

            controller.result = ""
            controller.logs = []
            url = "";
            if(this.instruction.trim() == ""){
                url =  "/execute/"+this.mazeid;
            }
            else{
                url =  "/execute/"+this.mazeid+"/"+this.instruction;
            }
            $http.get(url).success(function(data){
                controller.result = data["result"]
                if(data["result_code"] == 200){
                    controller.logs = data["logs"]
                }
            }).error(function(data){
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
