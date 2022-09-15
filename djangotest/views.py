import pymysql
import pymysql.cursors
from django.http import JsonResponse
from django.shortcuts import render

mysqlhost = "gigabytenandteam.ddns.net"
mysqlport = 33307

# Create your views here.
def hello_view(request):
    return render(request, 'hello_django.html', {
        'data': "Hello Django ",
    })


# Create your views here.
# 資料讀取
def index_Test(request):

    conn = pymysql.connect(host=mysqlhost, port=mysqlport, user="hywu", passwd="kOsJX0GfsqIzeukj",
                           db="sorting_20220421", charset='utf8', cursorclass=pymysql.cursors.DictCursor)
    with conn.cursor() as cursor:
        cursor.execute("SELECT * FROM sortingreport_000")
        data = cursor.fetchall()
        COLUMNS = [i[0] for i in cursor.description]  # for all Columns name
        output = [list(dict(i).values()) for i in data]
        conn.close()

    conn = pymysql.connect(host=mysqlhost, port=mysqlport, user="hywu", passwd="kOsJX0GfsqIzeukj",
                           charset='utf8', cursorclass=pymysql.cursors.DictCursor)
    with conn.cursor() as cursor:
        print(cursor.execute("SHOW DATABASES LIKE '%sorting_%'"))
        data = cursor.fetchall()
        alldatabase = [list(dict(i).values()) for i in data]
        conn.close()
    return render(request, 'index_Test.html', {'data': output, 'COLUMNS': COLUMNS, 'alldatabase': alldatabase})

def get_table(request):
    """
    当选择数据库连接时，联动查询出该库的表，供下拉选择
    :return:
    """
    if request.method == 'GET':
        # 获得前台传递来的id，查询对应的数据库连接信息
        db_link_id = request.GET.get('db_link_id')
        print('从前台获得的id为：%s' % db_link_id)

        conn = pymysql.connect(host=mysqlhost, port=mysqlport, user="hywu", passwd="kOsJX0GfsqIzeukj",
                           db=db_link_id, charset='utf8', cursorclass=pymysql.cursors.DictCursor)
        cursor = conn.cursor()
        # db_name = "select db_name from comparison_linkdbinfo where id='%s'" % db_link_id
        # print db_name
        # 查询该库中的所有表
        #get_all_table_sql = "select table_name from information_schema.tables where table_schema= '%s'" % db_link_info_dict['db_name']
        cursor.execute("SHOW TABLES")
        data = list(cursor.fetchall())
        table_list = [list(dict(i).values()) for i in data]
        print (table_list)
        return JsonResponse(table_list, safe=False)