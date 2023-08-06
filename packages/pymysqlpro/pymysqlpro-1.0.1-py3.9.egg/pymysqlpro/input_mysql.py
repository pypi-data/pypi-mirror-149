def inputmysql():
    
    print("接下来输入的东西都不用加单双引号，自动转换成字符串格式！注意！")
    import time
    
    time.sleep(0.5)
    sql = input("请输入SQL语句:")
    
    time.sleep(0.5)
    hostname_1 = input("请输入host主机名,一般默认127.0.0.1:")
    
    time.sleep(0.5)
    username_1 = input("请输入用户名,一般默认root:")

    time.sleep(0.5)
    password_1 = input("请输入数据库密码:")

    time.sleep(0.5)
    databasename_1=input("请输入查询的数据库的名字,mysql语法中的use database_name的意思:")



    from pymysqlpro import pymysqlpro
    pymysqlpro.mysql_select(sql,hostname_1,username_1,password_1,databasename_1)    
    