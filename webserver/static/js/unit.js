(function() 
{
    var app = angular.module("unit", []);
    
    app.directive("unitsPanel", function()
    {
        return {
            restrict : "E",
            templateUrl : "/static/html/unitspanel.html",
            controller : [ "$http", function($http)
            {
                var controller = this;
                this.mode = "view";
                this.searchField = {};
                this.postField = {};
                this.selectedUnit = {};
                this.newUnit = {};
                this.unitslist = [];

                $http.get("/unitslist").success(function(data)
                {
                    controller.unitslist = data["units"];
                });

                this.updateList = function()
                {
                    $http.get("/unitslist").success(function(data)
                    {
                        controller.unitslist = data["units"];
                    });
                };


                this.setSelectedUnit = function(unit)
                {
                    this.selectedUnit = unit;        
                };
                
                this.search = function(){
                    var query = [];
                    for(var key in this.searchField)
                    {
                        if(this.searchField[key].trim() != "")
                        {
                            query.push(key+"="+this.searchField[key]);
                        }
                    }
                    $http.get("/unitslist?"+query.join("&")).success(function(data)
                            {
                                controller.unitslist = data["units"];
                                controller.selectedUnit = {};
                                controller.mode = "view";
                            });
                };

                this.save = function(){
                    if(this.mode == "edit")
                    {
                        $http.put("/updateunit", this.selectedUnit).success(function(data)
                            {
                            });
                        this.mode = "view";
                    }
                };

                this.addNewUnit = function(){
                    if(this.mode == "new")
                    {
                        $http.post("/newunit", this.newUnit).success(function(data)
                            {
                                $http.get("/unitslist").success(function(data)
                                {
                                    controller.unitslist = data["units"];
                                });
                            });
                        this.mode = "view";
                    }
                };

                this.setMode = function(mode){
                    if(mode == "new")
                    {
                        this.mode = mode;
                    }
                    else if(mode == "edit")
                    {
                        if(typeof this.selectedUnit["_id"] != 'undefined')
                        {
                            this.mode = "edit";
                        }
                    }
                    else if(mode == "view")
                    {
                        this.mode = mode;
                    }
                };

            }],
            controllerAs: "unitsCtrl",
        };
    });
})();
