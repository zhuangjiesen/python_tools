


function formSerializeArrayToJsonByItem(formDom){
        var params = null;
        var formArray  = $(formDom).serializeArray();

        if (formArray && formArray.length > 0) {
            params = {};
            for (var i = 0 ; i < formArray.length ; i++) {


                var formItem = formArray[i];
                var name = formItem['name'];
                var value = formItem['value'];

                if (value && value != '全部' && value.indexOf('全部') < 0) {
                    params[name] = value;
                }

            }

        }


        return params;
}