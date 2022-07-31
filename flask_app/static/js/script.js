var app = angular.module('myApp', []);
var url = "http://127.0.0.1:5000";




var timeCount;
var failureCount;
var pieChartData;
var dataModalEvents;
var doughnutChart;
var datamodalChart;
var lineChart;
var stackBarChart;
var cookieName = "dbs"



toastr.options = {
    "closeButton": true,
    "debug": false,
    "newestOnTop": false,
    "progressBar": true,
    "positionClass": "toast-top-right",
    "preventDuplicates": true,
    "onclick": null,
    "showDuration": "300",
    "hideDuration": "1000",
    "timeOut": "5000",
    "extendedTimeOut": "1000",
    "showEasing": "swing",
    "hideEasing": "linear",
    "showMethod": "fadeIn",
    "hideMethod": "fadeOut"
}



app.controller('myCtrl', function($scope, $http) {

    $scope.operations = {
        SpDiffDef: {task_id:"", task_status:""},
        missing_tables: {task_id:"", task_status:""},
        missing_sps: {task_id:"", task_status:""},
        table_def: {task_id:"", task_status:""},
        diff_inparam: {task_id:"", task_status:""}
    };

    $scope.setConnection = function(sourcename, sourcehost, sourceusername, sourcepassword, sourcedatabase, destinationname, destinationhost, destinationusername, destinationpassword, destinationdatabase) {
        console.log("Creating Connections to database ...");
        var data = { sourcename: sourcename, sourcehost: sourcehost, sourceusername: sourceusername, sourcepassword: sourcepassword, sourcedatabase: sourcedatabase, destinationname: destinationname, destinationhost: destinationhost, destinationusername: destinationusername, destinationpassword: destinationpassword, destinationdatabase: destinationdatabase };
        console.log(data);
        $http.post(url + '/connectdbs', JSON.stringify(data))
            .then(function(response) {
                    if (response.data) {
                        msg = response.data.message
                        status = response.data.status
                        console.log(response.data);
                        setCookie(cookieName, JSON.stringify(data), "1")
                        onSuccess(msg, status);
                    }
                },
                function(response) {
                    console.log(response);
                    var paragraph = document.getElementById("message");
                    var text = document.createTextNode(response);
                });

    };

    function setCookie(cname, cvalue, exdays) {
        const d = new Date();
        d.setTime(d.getTime() + (exdays * 24 * 60 * 60 * 1000));
        let expires = "expires=" + d.toUTCString();
        document.cookie = cname + "=" + cvalue + ";" + expires + ";path=/";
    };

    function getCookie(cookieName) {
        let cookie = {};
        document.cookie.split(';').forEach(function(el) {
            let [key, value] = el.split('=');
            cookie[key.trim()] = value;
        })
        return cookie[cookieName];
    };

    function clearBox(elementID) {
        document.getElementById(elementID).innerHTML = "";
    };

    function setData(data, elementid) {
        document.getElementById(elementid).innerHTML = data
            // console.log(elementid, data)
    };

    function assignData(data, prefix) {
        setData(data.sourcename, prefix + "_src_name")
        setData(data.sourcehost, prefix + "_src_host")
        setData(data.sourcedatabase, prefix + "_src_database")

        setData(data.destinationname, prefix + "_dst_name")
        setData(data.destinationhost, prefix + "_dst_host")
        setData(data.destinationdatabase, prefix + "_dst_database")
    };

    function setStatus(task_id, key, txt) {
        $http.get(url + '/simple_task_status/' + task_id)
            .then(function(response) {
                console.log('Task : ' +txt + " : " +  task_id +' in process, Status :  ',response?.data)
                temp_status = response.data;
                //setCookie(task_id,temp_status,1);
                setTaskStatus(key, temp_status);
            }, function(response) {
                console.log(response);
            });
    };

    function setTaskStatus(key, status){
        $scope.operations[key].task_status = status;
    };

    function getTaskStatus_getSpDiffDef(key){
        return $scope.operations[key].task_status;
    };

    function getTaskStatus_get_table_def(key){
        return $scope.operations[key].task_status;
    };

    function getTaskStatus_get_diff_inparam(key){
        return $scope.operations[key].task_status;
    };

    function setTaskId(key, taskid){
        $scope.operations[key].task_id = taskid;
    };

    function checkExistingStatus(key){
        if ($scope.operations[key].task_status === "SUCCESS"){
            return true;
        }else{
            return false;
        };
    };

    function getTaskId(key){
        return $scope.operations[key].task_id;
    };


    function getSpDiffDefResult(task_id) {
        $http.get(url + '/simple_task_result/' + task_id)
            .then(function(response) {
                console.log('Task : '+ "SP Definition Difference : " + task_id + ' result :');
                console.log(response.data)
                if (response.data) {
                    document.getElementById('toHideSpdf').style.display = "none";
                    if (response.data != "[]") {
                        for (var i = 0; i < response.data.length; i++) {
                            var div = document.createElement('div');
                            div.id = "spname" + i;
                            div.innerHTML = '<div class="row mt-4"> <div class="col-sm-6 text-center"><p>' + response.data[i].src_sp + '</p></div> <div class="col-sm-6 text-center"><p>' + response.data[i].dst_sp + '</p></div></div>'
                            document.getElementById('difftable').appendChild(div);
                            var div = document.createElement('div');
                            div.id = i;
                            div.innerHTML = response.data[i].difftbl;
                            div.className = 'border pad';
                            document.getElementById('difftable').appendChild(div);
                        }
                    }
                    if(response.data.length == 0){
                        // When there is no difference
                        var div = document.createElement('div');
                        div.id = "spname_zx";
                        div.innerHTML = '<h5>Yay, Everything Looks Good !!</h5>'
                        document.getElementById('difftable').appendChild(div);
                    }
                }
            }, function(response) {
                console.log(response.data);
            });
        return $scope.result;
    };

    $scope.getSpDiffDef = function() {
        clearBox('difftable')
        document.getElementById('toHideSpdf').style.display = "flex";
        console.log("In call");
        cookie = getCookie(cookieName)
        data = JSON.parse(cookie)
        assignData(data, "spdf")

        id = getTaskId("SpDiffDef");
        if(id === ""){
            $http.post(url + '/spsdiffdef', cookie)
            .then(function(response) {
                    if (response.data) {
                        taskId = response?.data?.task_id;
                        console.log('Task "SP Definition Difference" Submitted with Id : ',taskId);
                        // setCookie(taskId,"",1);
                        setTaskId("SpDiffDef",taskId);

                        var refreshId = setInterval(function() {
                            setStatus(taskId,"SpDiffDef","SP Definition Difference");
                            console.log($scope.operations);
                            //if (getCookie(taskId) == "SUCCESS") 
                            if (getTaskStatus_getSpDiffDef("SpDiffDef") == "SUCCESS") {
                                clearInterval(refreshId);
                                getSpDiffDefResult(taskId);
                            }
                        }, 10000);

                    }
                },
                function(response) {
                    console.log(response);
                });
        } else {
            if(checkExistingStatus("SpDiffDef")){
                getSpDiffDefResult(id);
            };
        };


        



    };

    $scope.get_missing_tables = function() {
        console.log("In missingtbls call");
        clearBox('missing_tables')
        document.getElementById('toHideMst').style.display = "flex";
        cookie = getCookie(cookieName)
        data = JSON.parse(cookie)
        assignData(data, "mst")
        $http.post(url + '/missingtables', cookie)
            .then(function(response) {
                    if (response.data) {
                        console.log(response.data);
                        if (response.data != "{}") {

                            document.getElementById('toHideMst').style.display = "none";
                            var div = document.createElement('div');
                            div.id = "missing_tables";
                            div.innerHTML = response.data.diff_tbl;
                            div.className = 'border pad';
                            document.getElementById('missing_tables').appendChild(div);

                        }
                    }
                },
                function(response) {
                    console.log(response);
                });

    };

    $scope.get_missing_sps = function() {
        console.log("In missingsps call");
        cookie = getCookie(cookieName)
        clearBox('missing_sps')
        document.getElementById('toHideMsp').style.display = "flex";
        data = JSON.parse(cookie)
        assignData(data, "msp")
        $http.post(url + '/missingsps', cookie)
            .then(function(response) {
                    if (response.data) {
                        console.log(response.data);
                        if (response.data != "{}") {
                            document.getElementById('toHideMsp').style.display = "none";
                            var div = document.createElement('div');
                            div.id = "missing_sps";
                            div.innerHTML = response.data.diff_tbl;
                            div.className = 'border pad';
                            document.getElementById('missing_sps').appendChild(div);

                        }
                    }
                },
                function(response) {
                    console.log(response);
                });

    };

    function get_table_defResult(task_id){

        $http.get(url + '/simple_task_result/' + task_id)
            .then(function(response) {
                console.log('Task : Table Def Difference : ' + task_id + ' result :');
                console.log(response.data);
                if (response.data) {
                    document.getElementById('toHideTdf').style.display = "none";
                    console.log(response.data);
                    if (response.data != "{}") {

                        for (var i = 0; i < response.data.length; i++) {
                            var div = document.createElement('div');
                            div.id = "tab_def" + i;
                            div.innerHTML = '<div class="row mt-4"> <div class="col-sm-6 text-center"><p>' + response.data[i].src_tbl + '</p></div> <div class="col-sm-6 text-center"><p>' + response.data[i].dst_tbl + '</p></div></div>'
                            document.getElementById('table_definitions').appendChild(div);
                            var div = document.createElement('div');
                            div.id = i;
                            div.innerHTML = response.data[i].difftbl;
                            div.className = 'border pad';
                            document.getElementById('table_definitions').appendChild(div);
                        }
            
                    }
                    if(response.data.length == 0){
                        // When there is no difference
                        var div = document.createElement('div');
                        div.id = "tab_def_zx";
                        div.innerHTML = '<h5>Yay, Everything Looks Good !!</h5>'
                        document.getElementById('table_definitions').appendChild(div);
                    }
                }
            }, function(response) {
                console.log(response.data);
            });
        return $scope.result;
        
    };

    $scope.get_table_def = function(task_id) {
        console.log("In tables def call");
        cookie = getCookie(cookieName);
        clearBox('table_definitions');
        document.getElementById('toHideTdf').style.display = "flex";
        data = JSON.parse(cookie);
        assignData(data, "tbd");

        id3 = getTaskId("table_def");

        if (id3 === ""){
            $http.post(url + '/tablesdiffdef', cookie)
            .then(function(response) {
                    if (response.data) {
                        taskId = response?.data?.task_id;
                        console.log('Task "Table Def Difference" Submitted with Id : ',taskId);
                         //setCookie(taskId,"",1);
                        setTaskId("table_def",taskId);
                        var refreshId = setInterval(function() {
                            setStatus(taskId,"table_def", "Table Def Difference");
                            console.log($scope.operations);
                            // if (getCookie(taskId) == "SUCCESS") 
                            if (getTaskStatus_get_table_def("table_def") == "SUCCESS") {
                                clearInterval(refreshId);
                                get_table_defResult(taskId);
                            }
                        }, 10000);
                        }
                },
                function(response) {
                    console.log(response);
                });
        }else{
            if(checkExistingStatus("table_def")){
                get_table_defResult(id3);
            };
        };
        

    };

    function get_diff_inparam_Result(task_id) {
        $http.get(url + '/simple_task_result/' + task_id)
            .then(function(response) {
                console.log('Task : SP InParam Difference : ' + task_id + ' result :');
                console.log(response.data)
                if (response.data) {
                    document.getElementById('toHideSpin').style.display = "none";
                    console.log(response.data);
                    if (response.data != "{}") {

                        for (var i = 0; i < response.data.length; i++) {
                            var div = document.createElement('div');
                            div.id = "spname_param" + i;
                            div.innerHTML = '<div class="row mt-4"> <div class="col-sm-6 text-center"><p>' + response.data[i].src_sp + '</p></div> <div class="col-sm-6 text-center"><p>' + response.data[i].dst_sp + '</p></div></div>'
                            document.getElementById('sp_in_params').appendChild(div);
                            var div = document.createElement('div');
                            div.id = i;
                            div.innerHTML = response.data[i].difftbl;
                            div.className = 'border pad';
                            document.getElementById('sp_in_params').appendChild(div);
                        }

                    }
                    if(response.data.length == 0){
                        // When there is no difference
                        var div = document.createElement('div');
                        div.id = "spname_pram_zx";
                        div.innerHTML = '<h5>Yay, Everything Looks Good !!</h5>'
                        document.getElementById('sp_in_params').appendChild(div);
                    }
                }
            }, function(response) {
                console.log(response.data);
            });
        return $scope.result;
    };

    $scope.get_diff_inparam = function() {
        console.log("In diff in param call");
        cookie = getCookie(cookieName);
        clearBox('sp_in_params');
        document.getElementById('toHideSpin').style.display = "flex";
        data = JSON.parse(cookie);
        assignData(data, "spin");

        id2 = getTaskId("diff_inparam");

        if(id2 === ""){
            $http.post(url + '/spsdiffinparam', cookie)
            .then(function(response) {
                if (response.data) {
                    taskId = response?.data?.task_id;
                    console.log('Task "SP InParam Difference" Submitted with Id : ',taskId);
                    //setCookie(taskId,"",1);
                    setTaskId("diff_inparam",taskId);
                    var refreshId = setInterval(function() {
                        setStatus(taskId,"diff_inparam", "SP InParam Difference");
                        console.log($scope.operations);
                        // if (getCookie(taskId) == "SUCCESS") 
                        if (getTaskStatus_get_diff_inparam("diff_inparam") == "SUCCESS") {
                            clearInterval(refreshId);
                            get_diff_inparam_Result(taskId);
                        }
                    }, 10000);

                }
                },
                function(response) {
                    console.log(response);
                });
        }else{

            if(checkExistingStatus("diff_inparam")){
                get_diff_inparam_Result(id2);
            };
            
        };
        

    };


});



var onSuccess = function(value, state) {
    Swal.fire({
            title: value,
            text: '',
            icon: state,
            showCancelButton: false,
            cancelButtonColor: '#3085d6'
        })
        .then(function(result) {
            if (result.value) {

                if (state == "success") {
                    document.getElementById('v-pills-missingtables-tab').style.visibility = 'visible';
                    document.getElementById('v-pills-missingsps-tab').style.visibility = 'visible';
                    document.getElementById('v-pills-tabledefinitions-tab').style.visibility = 'visible';
                    document.getElementById('v-pills-spdefinitions-tab').style.visibility = 'visible';
                    document.getElementById('v-pills-spinparams-tab').style.visibility = 'visible';
                    document.getElementById('new-connection').style.visibility = 'visible';
                    document.getElementById('create-connection').style.visibility = 'hidden';

                }

                if (state == "error") {
                    document.getElementById('v-pills-missingtables-tab').style.visibility = 'hidden';
                    document.getElementById('v-pills-missingsps-tab').style.visibility = 'hidden';
                    document.getElementById('v-pills-tabledefinitions-tab').style.visibility = 'hidden';
                    document.getElementById('v-pills-spdefinitions-tab').style.visibility = 'hidden';
                    document.getElementById('v-pills-spinparams-tab').style.visibility = 'hidden';
                }

            }
        });
};