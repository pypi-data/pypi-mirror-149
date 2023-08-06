
#封装一个中转模块函数，用来实现可重复选择不同模块功能



def module_0():
    import time
    time.sleep(0.5)
    
    time.sleep(0.2)
    print("请输入数字\n1登录数据库\n2关闭数据库连接\n3查询\n4插入\n5更新\n6删除\n7调用存储以及使用其他复杂语句(自由度更高)\n8退出,\n9选择数据库,use database xxx的数据库命令,\n10获取帮助help:")
    a_1=int(input())
    if a_1==1:
        #1功能登录
        time.sleep(0.2)
        print("--正在使用登录数据库模块功能--")
        from pymysqlpro import pymysqlpro
        pymysqlpro.module_sign_in()

    elif a_1==2:
        #2功能关闭数据库
        time.sleep(0.2)
        print("--正在使用关闭数据库连接,游标对象功能--")
        from pymysqlpro import pymysqlpro
        pymysqlpro.module_2()
    
    
    
    elif a_1==3:
        #3功能查询语句
        time.sleep(0.2)
        print("--正在使用sql数据库查询语句功能")
        from pymysqlpro import pymysqlpro
        pymysqlpro.module_3() 
    
    
    
    
    elif a_1==4:
        #4功能插入语句
        time.sleep(0.2)
        print("--正在使用插入语句功能--")
        from pymysqlpro import pymysqlpro
        pymysqlpro.module_4()

    elif a_1==5:
        time.sleep(1)
        print("--正在使用更新语句功能--")  
        from pymysqlpro import pymysqlpro
        pymysqlpro.module_5()

    elif a_1==6:
        time.sleep(1)
        print("--正在使用删除语句功能--")
        from pymysqlpro import pymysqlpro
        pymysqlpro.module_6()     
    elif a_1==7:
        time.sleep(1)
        print("--正在使用SQL复杂语句功能--")
        from pymysqlpro import pymysqlpro
        pymysqlpro.module_7()

    elif a_1==8:

        time.sleep(0.2)
        print("--正在使用了命令exit()功能--")

        exit()
    elif a_1==9:
        time.sleep(0.2)
        print("--正在使用use databases命令--")  
        from pymysqlpro import pymysqlpro
        pymysqlpro.module_9_1()
        pymysqlpro.module_9_2()
    elif a_1==10:
        from pymysqlpro import pymysqlpro
        pymysqlpro.pymysqlpro_help()


    else:
        print("输入错误") 
        from pymysqlpro import pymysqlpro
        pymysqlpro.pymysqlpro_help()            
    
    

      

        







    