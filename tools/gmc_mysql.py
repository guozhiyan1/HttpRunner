import pymysql
from config import config


def get_database(sql):
    # 打开数据库连接
    db = pymysql.connect(config.get_conf("mysql", "host"),
                         config.get_conf("mysql", "username"),
                         config.get_conf("mysql", "password"))

    # 使用 cursor() 方法创建一个游标对象 cursor
    cursor = db.cursor(pymysql.cursors.DictCursor)
    # 使用 execute()  方法执行 SQL 查询
    cursor.execute(sql)
    result = cursor.fetchall()
    # result = cursor.fetchone()
    # 关闭数据库连接
    db.commit()
    db.close()
    return result


if __name__ == '__main__':
    result = get_database("select *  FROM inhospital_register_db.biz_inhospital_patient limit 10")
    print(result)