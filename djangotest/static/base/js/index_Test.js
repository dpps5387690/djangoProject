$("#tx_daterange").daterangepicker({
    startDate: "2022-09-01",
    endDate: "2022-09-15",
    locale: {
        format: 'YYYYMMDD',
        separator: " "
    }
});

const tx_daterange = document.getElementById('tx_daterange');

const lb_Status = document.getElementById('lb_Status');

const tx_searchPN = document.getElementById('tx_searchPN');
tx_searchPN.addEventListener('input', updateValue);

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

const bt_searchPN = document.getElementById('bt_searchPN');
bt_searchPN.addEventListener('click', search_table_by_value);

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
            // ("hide_index " + hide_index);
            $('#TableShow tr > *:nth-child(' + hide_index + ')').hide();
            $(lb_Status).text("Find " + data['output'].length + " matches.");
        },
    })
}

$("#databasename").change(function () {
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
        },
    })
    $("#datatablename").change();
})
$(document).ready(function () {
    $("#datatablename").change();
})
$("#datatablename").change(function () {
    var options = $("#databasename option:selected"); //获取选中的项
    var db_Name = options.val(); //获取选中的值
    options = $("#datatablename option:selected"); //获取选中的项
    var db_Table = options.val(); //获取选中的值
    var hide_index = 0;
    // alert("ok");
    // alert(db_Name + " " + db_Table);

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
})

/*$(document).ready(function () {
    function refresh() {
        $.getJSON("/get_now_Status/", function (ret) {
            console.log("outstatus: " + ret)
            $(lb_Status).text(ret);
        })
    }

    setInterval(refresh, 100)
})*/