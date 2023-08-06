#自定义查询模块



def mysql_select(sql,host,user,password,db_name):
    from pandas import DataFrame
    from tqdm import tqdm
    import time
    import pymysql
    import pandas
    db=db_name
    cur_1=pymysql.connect(
        host=host,
        user=user,
        password=password,
        database=db
        )
    cursor=cur_1.cursor()
    a=sql[0:6].upper()
    list_1=['SELECT']
    if a in list_1:
        try:
            cursor.execute(sql)
            cur_2=cursor.fetchall()
            count_1=0
            for row in cur_2:
                count_1+=1
            print("总计：",count_1, "\n进度条开始祈祷:")  
            for i in tqdm(range(count_1)):
                time.sleep(0.5)   
            cur_3=DataFrame(list(cur_2))
            print(cur_3)
            print("SELECT字段正确,sql语法应该可以使用")
        except:
            print("SELECT字段正确,但是语法可能错误")
        cur_1.close()
    else:
        print("查询字符SELECT使用错误")




#