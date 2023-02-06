$("#tx_daterange").daterangepicker({
    startDate: "2023-02-01",
    endDate: "2023-02-11",
    locale: {
        format: 'YYYYMMDD',
        separator: " "
    }
});
const lb_Status = document.getElementById('lb_Status');
const tx_daterange = document.getElementById('tx_daterange');

const tx_searchPN = document.getElementById('tx_searchPN');

$(document).ready(function () {
    datatablename_change();
    $('#bt_upload').on('click', uploadMultiFiles);
    $('#tx_searchPN').on('input', updateValue);
    $('#bt_searchPN').on('click', search_table_by_value);
    $('#databasename').on('change', databasename_change);

    $("#datatablename").on('change', datatablename_change);
});

function updateValue(e) {
    // alert("key: " + e.key)
    // alert("key: " + this.value)
    // console.log(this.value + " " + this.value.length);
    //console.log("tx_daterange: " + $(tx_daterange).val());

    if (this.value.length > 28) {
        this.select();
        search_table_by_value();
    }

    // if(e.key == 'Enter')
    //     $("#bt_searchPN").click()
}

function search_table_by_value(e) {
    var searchPN = $(tx_searchPN).val(); //获取选中的项
    var hide_index = 0;
    var dateValueStr = $(tx_daterange).val();
    // var val = this.value;
    // alert("searchPN: " + searchPN)
    console.log("searchPN: " + searchPN);

    $(lb_Status).text("Found Start.");
    // 选择id=db_link的元素时触发该ajax请求，调用/comparison/get_table接口
    $.ajax({
        url: '/search_data_row/',
        data: {"searchPN": searchPN, "dateValueStr": dateValueStr},
        type: 'GET',
        dataType: 'json',
        success: function (data) {
            var content = '';
            console.log("data['output'].length: " + data['output'].length);
            tx_searchPN.select();
            if (data['output'].length == 0) {
                $(lb_Status).text("Nonfound.");
                $('#TableShow').html('')
                return
            }

            content += '<tr>';
            $.each(data['COLUMNS'], function (i, item) {
                // 调用接口后返回list数据[u'account_role', u'account_user'],循环遍历该list拼接选项的内容
                // if (item == 'PNPDeviceID')
                //     hide_index = Number(i) + 1;

                content += '<th id=' + item + '>' + item + '</th>'
                // alert(i);
                // alert(COLUMNS);
            });
            content += '</tr>';
            $.each(data['output'], function (i, row) {
                // 调用接口后返回list数据[u'account_role', u'account_user'],循环遍历该list拼接选项的内容
                content += '<tr>';
                $.each(row, function (index, value) {
                    content += '<td  align="center">' + value + '</td>'
                });
                content += '</tr>';
            });
            // 将拼接好的内容作为id=db_table这个select元素的内容
            $('#TableShow').html(content)
            // ("hide_index " + hide_index);
            $('#TableShow tr > *:nth-child(' + hide_index + ')').hide();
            $(lb_Status).text("Find " + data['output'].length + " matches.");
        },
    })
}

function databasename_change() {
    var options = $("#databasename option:selected"); //获取选中的项
    var db_link_id = options.val(); //获取选中的值
    // alert("ok");
    // aalert(db_link_id);

    // 选择id=db_link的元素时触发该ajax请求，调用/comparison/get_table接口
    $.ajax({
        url: '/get_table/',
        data: {"db_link_id": db_link_id},
        type: 'GET',
        dataType: 'json',
        success: function (data) {
            var content = '';

            $.each(data, function (i, item) {
                // 调用接口后返回list数据[u'account_role', u'account_user'],循环遍历该list拼接选项的内容
                content += '<option>' + item + '</option>'
            });
            // 将拼接好的内容作为id=db_table这个select元素的内容
            $('#datatablename').html(content)
            datatablename_change();
        },
    })
}

function datatablename_change() {
    var options = $("#databasename option:selected"); //获取选中的项
    var db_Name = options.val(); //获取选中的值
    options = $("#datatablename option:selected"); //获取选中的项
    var db_Table = options.val(); //获取选中的值
    var hide_index = 0;
    // alert("ok");
    // alert(db_Name + " " + db_Table);
    console.log("db_Name: " + db_Name + " db_Table: " + db_Table)
    // var val = this.value;
    // alert(val)
    $(lb_Status).text("Get Data wait.");
    // 选择id=db_link的元素时触发该ajax请求，调用/comparison/get_table接口
    $.ajax({
        url: '/get_table_data/',
        data: {"db_Name": db_Name, "db_Table": db_Table},
        type: 'GET',
        dataType: 'json',
        success: function (data) {
            var content = '';

            content += '<tr>';
            $.each(data['COLUMNS'], function (i, item) {
                // 调用接口后返回list数据[u'account_role', u'account_user'],循环遍历该list拼接选项的内容
                if (item == 'PNPDeviceID')
                    hide_index = Number(i) + 1;

                content += '<th id=' + item + '>' + item + '</th>'
                // alert(i);
                // alert(COLUMNS);
            });
            content += '</tr>';
            $.each(data['output'], function (i, row) {
                // 调用接口后返回list数据[u'account_role', u'account_user'],循环遍历该list拼接选项的内容
                content += '<tr>';
                $.each(row, function (index, value) {
                    content += '<td  align="center">' + value + '</td>'
                });
                content += '</tr>';
            });
            // 将拼接好的内容作为id=db_table这个select元素的内容
            $('#TableShow').html(content)
            // alert("hide_index " + hide_index);
            $('#TableShow tr > *:nth-child(' + hide_index + ')').hide();
        },
    })
    $(lb_Status).text("Get Data OK.");
}


function uploadMultiFiles() {
    console.log("uploadMultiFiles");
    var form_data = new FormData();
    var ins = document.getElementById('multiFiles').files.length;
    console.log("ins: " + ins);
    if (ins == 0) {
        $('#msg').html('<div class="alert alert-danger" role="alert">Select at least one file</div>');
        return;
    }
    for (var x = 0; x < ins; x++) {
        form_data.append("files[]", document.getElementById('multiFiles').files[x]);
    }
    console.log(form_data);

    csrf_token = $('input[name="csrfmiddlewaretoken"]').val();

    // console.log(csrf_token);

    form_data.append("csrfmiddlewaretoken", csrf_token);

    $.ajax({
        url: '/multi_Files_Upload/', // point to server-side URL
        dataType: 'json', // what to expect back from server
        cache: false,
        contentType: false,
        processData: false,
        //data: {'data': form_data, 'csrfmiddlewaretoken': csrf_token},
        data: form_data,
        type: 'post',

        success: function (response) { // display success response
            $('#msg').html(response.msg);
        },
        // error: function (response) {
        //     $('#msg').html(response.message); // display error response
        // }
    })
}

/*$(document).ready(function () {
    function refresh() {
        $.getJSON("/get_now_Status/", function (ret) {
            console.log("outstatus: " + ret)
            $(lb_Status).text(ret);
        })
    }

    setInterval(refresh, 100)
})*/