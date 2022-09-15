import pymysql
import pymysql.cursors
from django.http import JsonResponse
from django.shortcuts import render

mysqlhost = "192.168.50.5"  # "gigabytenandteam.ddns.net"
mysqlport = 3307  # 33307
mysqluser = "hywu"
mysqlpw = "kOsJX0GfsqIzeukj"


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
        #COLUMNS.remove('PNPDeviceID')
    return output, COLUMNS


def index_Test(request):
    conn = pymysql.connect(host=mysqlhost, port=mysqlport, user=mysqluser, passwd=mysqlpw,
                           charset='utf8', cursorclass=pymysql.cursors.DictCursor)
    with conn.cursor() as cursor:
        print(cursor.execute("SHOW DATABASES LIKE '%sorting_%'"))
        data = cursor.fetchall()
        alldatabase = [list(dict(i).values())[0] for i in data]
        conn.close()

    nowdatabasename = alldatabase[0]
    conn = pymysql.connect(host=mysqlhost, port=mysqlport, user=mysqluser, passwd=mysqlpw,
                           db=nowdatabasename, charset='utf8', cursorclass=pymysql.cursors.DictCursor)
    with conn.cursor() as cursor:
        print(cursor.execute("SHOW TABLES"))
        data = cursor.fetchall()
        table_list = [list(dict(i).values())[0] for i in data]
        conn.close()

    output, COLUMNS = getdata(nowdatabasename, table_list[0])
    return render(request, 'index_Test.html',
                  {'data': output, 'COLUMNS': COLUMNS, 'alldatabase': alldatabase, 'alldatatable': table_list})
    # return render(request, 'index_Test.html',
    #               {'alldatabase': alldatabase, 'alldatatable': table_list})

def get_table(request):
    """
    当选择数据库连接时，联动查询出该库的表，供下拉选择
    :return:
    """
    if request.method == 'GET':
        # 获得前台传递来的id，查询对应的数据库连接信息
        db_link_id = request.GET.get('db_link_id')
        print('从前台获得的id为：%s' % db_link_id)

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
        print(table_list)
        return JsonResponse(table_list, safe=False)


def get_table_data(request):
    if request.method == "GET":
        nowdatabasename = request.GET['db_Name']
        table = request.GET['db_Table']
        output, COLUMNS = getdata(nowdatabasename, table)
        return JsonResponse(data={"COLUMNS": COLUMNS, "output": output}, safe=False)
