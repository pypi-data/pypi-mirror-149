
    
#----------------------------------------------------
import time
from tqdm import tqdm,trange
from pandas import DataFrame
import pymysql
#------------------------------------------------------
def pymysqlpro_help():
    print("\n\n先登录,选择数据库,再进行查询,插入,更新,删除,调用存储过程以及其他复杂语句操作,包括前面的DML和DQL语句",
    "\n还有很多地方需要优化,以后有机会再慢慢更新！","\nversion='2.0'")
    print("\n里面输出的表格都是pandas的dataframe格式的,\n为什么没读出列名是因为没空弄了,累死我了,我还是个大学狗啊啊啊啊！")
    time.sleep(2)
    
    from pymysqlpro import order_pymysqlpro
    order_pymysqlpro.module_0()



#-----------------------------------------------------------------------------------------------------

def module_sign_in():    
    print("\n接下来输入的东西都不用加单双引号,\n自动转换成字符串格式!\n注意不要在输入语句前面加入空格,否则不能正常运行!")
    
       
    time.sleep(0.2)
    hostname_1 = input("\n请输入host主机名,一般默认127.0.0.1:")
    
    time.sleep(0.2)
    username_1 = input("\n请输入用户名,一般默认root:")

    time.sleep(0.2)
    password_1 = input("\n请输入数据库密码:")

    time.sleep(0.2)
    
   

    
    
    module_1(hostname_1,username_1,password_1)

#模块一：封装登录服务器函数并返回一个游标对象模块

def module_1(host,user,password):
    
    #输入必要信息登录
    global cur_1
    cur_1=pymysql.connect(
        host=host,
        user=user,
        password=password,
        
        )        
    global cursor
    cursor=cur_1.cursor()
    print("\n--尝试连接MYSQL数据库--")
    time.sleep(1)
    print("\n--开始连接数据库MYSQL,请等待--")
    module_1_1()    
    

#模块1.1：封装验证数据库连接是否成功并返回结果模块    
def module_1_1():

    def module_1_1_1():

        
        sql="select version();"
        cursor.execute(sql)
        cur_2=cursor.fetchall()
        cur_select_version=DataFrame(list(cur_2))
        cur_select_version.columns=['MySql版本']
        print(cur_select_version)
        global a_3
        a_3=0
        
    module_1_1_1()
    a_4=a_3+1
    if a_4==1:
        print("\n数据库连接成功") 
    else:
        print("\n数据库连接失败")
    from pymysqlpro import order_pymysqlpro
    order_pymysqlpro.module_0()
              

#------------------------------------------------------------------------------------------------
   

   

#模块二：关闭python对mysql数据库的游标
def module_2():
    cur_1.close()
    from pymysqlpro import order_pymysqlpro
    order_pymysqlpro.module_0()

#-------------------------------------------------------------------------------------------------
#模块三：查询语句模块封装函数：
def module_3():
    
    sql=input("\n请输入SQL查询select语句")
    a=sql[:6].upper()
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

                time.sleep(0.001)   
            cur_3=DataFrame(list(cur_2))
            print(cur_3)
            print("SELECT字段正确,sql语法应该可以使用")
        except:
            print("SELECT字段正确,但是语法可能错误")
    else:
        print("查询字符SELECT使用错误")
    from pymysqlpro import order_pymysqlpro
    order_pymysqlpro.module_0()

#简洁3.1查看某表全部（）
def module_3_1(a_6):
    a_5="select * from "
    a_6=a_6
    a_7=a_5+a_6
    try:
        cursor.execute(a_7)
        cur_2=cursor.fetchall()
        show_1=DataFrame(list(cur_2))
        print(show_1)
    except:
        print("输入的表名错误")    



#---------------------------------------------------------------------------------
#模块四：插入语句
def module_4():

    a_6=input("请输入要插入的表名：")
    try:
        
        module_3_1(a_6)
    except:
        return 0    

    
    
    time.sleep(0.5)

    sql=input("\n请输入SQL插入insert语句")
    a=sql[:6].upper()
    list_1=['INSERT']
    if a in list_1:
        try:
            cursor.execute(sql)
            cur_1.commit()
            print("插入成功")
            try:
                module_3_1(a_6)
            except:
                return 0   


        except:
            cur_1.rollback()
            print("插入失败") 
    else:
        print("输入语句有错误")
    from pymysqlpro import order_pymysqlpro
    order_pymysqlpro.module_0()             


#---------------------------------------------------------------------------------------------------------
#模块五：更新update语句

def module_5():
    
    a_6=input("请输入要进行更新某行数据的表名：")
    try:
        
        module_3_1(a_6)
    except:
        return 0    

    
    
    time.sleep(0.5)

    sql=input("\n请输入SQL更新update语句")
    a=sql[:6].upper()
    list_1=['UPDATE']
    if a in list_1:
        try:
            cursor.execute(sql)
            cur_1.commit()
            print("更新成功")
            try:
                module_3_1(a_6)
            except:
                return 0   


        except:
            cur_1.rollback()
            print("更新失败") 
    else:
        print("输入语句有错误")
    from pymysqlpro import order_pymysqlpro
    order_pymysqlpro.module_0()
#----------------------------------------------------------------------------------------------------------    
#模块六 删除：  
def module_6():
    
    a_6=input("请输入要删除某行数据的的表名：")
    try:
        
        module_3_1(a_6)
    except:
        return 0    

    
    
    time.sleep(0.5)

    sql=input("\n请输入SQL删除delete语句")
    a=sql[:6].upper()
    list_1=['DELETE']
    if a in list_1:
        try:
            cursor.execute(sql)
            cur_1.commit()
            print("删除成功")
            try:
                module_3_1(a_6)
            except:
                return 0   


        except:
            cur_1.rollback()
            print("删除失败") 
    else:
        print("输入语句有错误")
    from pymysqlpro import order_pymysqlpro
    order_pymysqlpro.module_0()  


#----------------------------------------------------------------------------------------------                                 
#模块七：复杂高级语句
def module_7():
    
    a_6=input("请输入要查看的表名：")
    try:
        
        module_3_1(a_6)
    except:
        return 0    

    
    
    time.sleep(0.5)

    sql=input("\n请输入SQL语句")
    
    
    try:
        cursor.execute(sql)
        cur_1.commit()
        print("成功输入")
        try:  
            module_3_1(a_6)
        except:
            return 0   


    except:
        cur_1.rollback()
        print("失败,不过rollback了,数据应该没事") 
   
    from pymysqlpro import order_pymysqlpro
    order_pymysqlpro.module_0()              


#-----------------------------------------------------------------------------------------------------------
    
#模块九：选择数据库
#9.1展示所有的数据库
def module_9_1():
    sql="show databases;"
    cursor.execute(sql)
    cur_2=cursor.fetchall()
    show_1=DataFrame(list(cur_2))
    show_1.columns=['所有数据库的名称']
    print("\n所有数据库名称列表")
    print(show_1)

#9.2选择数据库
def module_9_2():        
    a_5=input("\n选择输入数据库名字")
    a_6="use "
    a_7=a_6+a_5
    try:
         cursor.execute(a_7)
         print(a_7)
         cursor.execute("show tables;")
         cur_2=cursor.fetchall()
         show_1=DataFrame(list(cur_2))
         show_1.columns=['所有表的名称']
         print("\n所选择的库的表名称列表")
         print(show_1)
    except:
        print("\n没有输入的这个数据库名字,或者输入有错误")

    from pymysqlpro import order_pymysqlpro
    order_pymysqlpro.module_0()       



            
       
