import pymysql
import pymysql.cursors
from django.http import JsonResponse
from django.shortcuts import render

from django.shortcuts import render
from django.http import HttpResponse, HttpResponseBadRequest, HttpResponseForbidden
from django.views.decorators.csrf import csrf_exempt
from django.conf import settings

from linebot import LineBotApi, WebhookParser
from linebot.exceptions import InvalidSignatureError, LineBotApiError
from linebot.models import MessageEvent, TextSendMessage

line_bot_api = LineBotApi(settings.LINE_CHANNEL_ACCESS_TOKEN)
parser = WebhookParser(settings.LINE_CHANNEL_SECRET)


# mysqlhost = "gigabytenandteam.ddns.net"
# mysqlport = 33307

# mysqlhost = "192.168.50.5"
# mysqlport = 3307

# mysqlhost = "nandsorting.ddns.net"
# mysqlport = 33306

mysqlhost = "10.1.8.91"  # "gigabytenandteam.ddns.net"
mysqlport = 3306  # 33307

mysqluser = "hywu"
mysqlpw = "kOsJX0GfsqIzeukj"


@csrf_exempt
def callback(request):
    if request.method == 'POST':
        signature = request.META['HTTP_X_LINE_SIGNATURE']
        body = request.body.decode('utf-8')

        try:
            events = parser.parse(body, signature)  # 傳入的事件
        except InvalidSignatureError:
            return HttpResponseForbidden()
        except LineBotApiError:
            return HttpResponseBadRequest()

        for event in events:
            if isinstance(event, MessageEvent):  # 如果有訊息事件
                line_bot_api.reply_message(  # 回復傳入的訊息文字
                    event.reply_token,
                    TextSendMessage(text=event.message.text)
                )
        return HttpResponse()
    else:
        return HttpResponseBadRequest()

# Create your views here.
def hello_view(request):
    return render(request, 'hello_django.html', {
        'data': "Hello Django ",
    })


# 資料讀取
def getdata(DBName, TableName):
    conn = pymysql.connect(host=mysqlhost, port=mysqlport, user=mysqluser, passwd=mysqlpw,
                           db=DBName, charset='utf8', cursorclass=pymysql.cursors.DictCursor)
    with conn.cursor() as cursor:
        # cursor.execute("SELECT * FROM sortingreport_000")
        cursor.execute("SELECT * FROM %s" % TableName)
        data = cursor.fetchall()
        COLUMNS = [i[0] for i in cursor.description]  # for all Columns name
        output = [list(dict(i).values()) for i in data]
        conn.close()
        # COLUMNS.remove('PNPDeviceID')
    return output, COLUMNS


def get_sorting_alldatabase():
    conn = pymysql.connect(host=mysqlhost, port=mysqlport, user=mysqluser, passwd=mysqlpw,
                           charset='utf8', cursorclass=pymysql.cursors.DictCursor)
    with conn.cursor() as cursor:
        count = cursor.execute("SHOW DATABASES LIKE '%sorting_%'")
        print("alldatabase: %d" % count)
        data = cursor.fetchall()
        alldatabase = [list(dict(i).values())[0] for i in data]
        conn.close()
    return alldatabase


def get_sorting_alldatatable_byDBName(nowdatabasename):
    conn = pymysql.connect(host=mysqlhost, port=mysqlport, user=mysqluser, passwd=mysqlpw,
                           db=nowdatabasename, charset='utf8', cursorclass=pymysql.cursors.DictCursor)
    with conn.cursor() as cursor:
        count = cursor.execute("SHOW TABLES")
        print("getalltable: %d" % count)
        data = cursor.fetchall()
        table_list = [list(dict(i).values())[0] for i in data]
        conn.close()
    return table_list


def index_Test(request):
    alldatabase = get_sorting_alldatabase()
    nowdatabasename = alldatabase[0]
    alldatatable = get_sorting_alldatatable_byDBName(nowdatabasename)
    global logstatus
    logstatus = "index_Test getdata Start"
    output, COLUMNS = getdata(nowdatabasename, alldatatable[0])
    logstatus = "index_Test getdata End"
    return render(request, 'index_Test.html', locals())


def get_table(request):
    """
    当选择数据库连接时，联动查询出该库的表，供下拉选择
    :return:
    """
    if request.method == 'GET':
        # 获得前台传递来的id，查询对应的数据库连接信息
        db_link_id = request.GET.get('db_link_id')
        # print('从前台获得的id为：%s' % db_link_id)

        conn = pymysql.connect(host=mysqlhost, port=mysqlport, user=mysqluser, passwd=mysqlpw,
                               db=db_link_id, charset='utf8', cursorclass=pymysql.cursors.DictCursor)
        cursor = conn.cursor()
        # db_name = "select db_name from comparison_linkdbinfo where id='%s'" % db_link_id
        # print db_name
        # 查询该库中的所有表
        # get_all_table_sql = "select table_name from information_schema.tables where table_schema= '%s'" % db_link_info_dict['db_name']
        cursor.execute("SHOW TABLES")
        data = list(cursor.fetchall())
        table_list = [list(dict(i).values())[0] for i in data]
        # print(table_list)
        return JsonResponse(table_list, safe=False)


def get_table_data(request):
    if request.method == "GET":
        nowdatabasename = request.GET['db_Name']
        table = request.GET['db_Table']
        output, COLUMNS = getdata(nowdatabasename, table)
        return JsonResponse(data={"COLUMNS": COLUMNS, "output": output}, safe=False)


def search_WaferSN_ChipSN(DBName, TableName, waferSN, chipSN):
    conn = pymysql.connect(host=mysqlhost, port=mysqlport, user=mysqluser, passwd=mysqlpw,
                           db=DBName, charset='utf8', cursorclass=pymysql.cursors.DictCursor)

    output = list()
    COLUMNS = list()
    with conn.cursor() as cursor:
        # cursor.execute("SELECT * FROM %s" % TableName)
        count = cursor.execute(
            "SELECT * FROM %s WHERE WaferSN LIKE '%s' AND ChipSN LIKE '%s'" % (
                TableName, waferSN, chipSN))
        print("DBName: %s TableName: %s len(data): %d" % (DBName, TableName, count))
        global logstatus
        logstatus = "DBName: %s TableName: %s len(data): %d" % (DBName, TableName, count)
        if count != 0:
            COLUMNS = [i[0] for i in cursor.description]  # for all Columns name
            data = cursor.fetchall()
            output = [list(dict(i).values()) for i in data]
        conn.close()
        # COLUMNS.remove('PNPDeviceID')
    return output, COLUMNS


def get_database_by_DateRange(DateRange):
    conn = pymysql.connect(host=mysqlhost, port=mysqlport, user=mysqluser, passwd=mysqlpw,
                           charset='utf8', cursorclass=pymysql.cursors.DictCursor)
    with conn.cursor() as cursor:
        DateList = DateRange.split()
        commandstr = "SELECT table_schema,create_time FROM information_schema.tables  WHERE table_schema LIKE '%%sorting_%%' " \
                     "AND create_time > DATE('%s') AND create_time < DATE('%s') GROUP BY TABLE_SCHEMA" % (
                     DateList[0], DateList[1])
        count = cursor.execute(commandstr)
        print("alldatabase: %d" % count)
        data = cursor.fetchall()
        databasebyDateRange = [list(dict(i).values())[0] for i in data]
        conn.close()
    return databasebyDateRange


def search_data_row(request):
    if request.method == "GET":
        searchPN = request.GET['searchPN']
        dateValueStr = request.GET['dateValueStr']
        waferSN = searchPN[-14:-6]
        chipSN = searchPN[-6:]
        alldatabase = get_database_by_DateRange(dateValueStr)
        output = list()
        COLUMNS = list()
        for DBName in alldatabase:
            table_list = get_sorting_alldatatable_byDBName(DBName)
            for TableName in table_list:
                listout, CLOS = search_WaferSN_ChipSN(DBName, TableName, waferSN, chipSN)
                if len(listout) != 0:
                    COLUMNS = CLOS
                    output.extend(listout)

        return JsonResponse(data={"COLUMNS": COLUMNS, "output": output}, safe=False)


def get_now_Status(request):
    return JsonResponse(logstatus, safe=False)

def multi_Files_Upload(request):
    if request.method == 'POST':
        files = request.FILES.getlist('files[]', None)
        print(files)
        return JsonResponse({'msg':'<div class="alert alert-success" role="alert">File successfully uploaded</div>'})