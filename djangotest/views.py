import pymysql
import pymysql.cursors
from django.shortcuts import render

# Create your views here.
def hello_view(request):
    return render(request, 'hello_django.html', {
        'data': "Hello Django ",
    })
# Create your views here.
# 資料讀取
def index_Test(request):
    conn = pymysql.connect(host="gigabytenandteam.ddns.net", port=33307, user="hywu", passwd="kOsJX0GfsqIzeukj", db="sorting_20220421", charset='utf8', cursorclass=pymysql.cursors.DictCursor)
    with conn.cursor() as cursor:
        cursor.execute("SELECT * FROM sortingreport_000")
        data = cursor.fetchall()
        COLUMNS = [i[0] for i in cursor.description]#for all Columns name
        output = [list(dict(i).values()) for i in data]
    return render(request, 'index_Test.html', {'data': output ,'COLUMNS':COLUMNS})