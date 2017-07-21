


function getServerClientsInfo(params , context , callback){
    $.post(context + "/redisInfo/getServerClientsInfo.do", params ,
        function(data){
            if (data && data.success) {
                alert(data.msg);
            } else {
                alert(data.msg);
            }

            if (callback) {
                callback();
            }
            console.log(data); //  2pm

        }, "json");
}


function getServerPersistenceInfo(params , context , callback){
    $.post(context + "/redisInfo/getServerPersistenceInfo.do", params ,
        function(data){
            if (data && data.success) {
                alert(data.msg);
            } else {
                alert(data.msg);
            }

            if (callback) {
                callback();
            }
            console.log(data); //  2pm

        }, "json");
}


function getServerReplicationInfo(params , context , callback){
    $.post(context + "/redisInfo/getServerReplicationInfo.do", params ,
        function(data){
            if (data && data.success) {
                alert(data.msg);
            } else {
                alert(data.msg);
            }

            if (callback) {
                callback();
            }
            console.log(data); //  2pm

        }, "json");
}


function getServerCPUInfo(params , context, callback){
    $.post(context + "/redisInfo/getServerCPUInfo.do", params ,
        function(data){
            if (data && data.success) {
                alert(data.msg);
            } else {
                alert(data.msg);
            }


            if (callback) {
                callback();
            }

            console.log(data); //  2pm

        }, "json");
}


function getServerClusterInfo(params , context , callback){
    $.post(context + "/redisInfo/getServerClusterInfo.do", params ,
        function(data){
            if (data && data.success) {
                alert(data.msg);
            } else {
                alert(data.msg);
            }


            if (callback) {
                callback();
            }

            console.log(data); //  2pm

        }, "json");
}


function getServerKeyspaceInfo(params, context , callback){
    $.post(context + "/redisInfo/getServerKeyspaceInfo.do", params ,
        function(data){
            if (data && data.success) {
                alert(data.msg);
            } else {
                alert(data.msg);
            }

            if (callback) {
                callback();
            }

            console.log(data); //  2pm

        }, "json");
}


function getServerMemoryInfo(params , context , callback){
    $.post(context + "/redisInfo/getServerMemoryInfo.do", params ,
        function(data){
            if (data && data.success) {
                alert(data.msg);
            } else {
                alert(data.msg);
            }

            if (callback) {
                callback();
            }

            console.log(data); //  2pm

        }, "json");
}
