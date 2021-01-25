from tools import gmc_mysql
from data.sql_dict import *
from data import basic_dict
import pymysql
from config import config


class RunSql(object):
    """
    获取和执行sql
    """

    def __init__(self, sql_dict, *args, **kwargs):
        self.dict = sql_dict
        self.sql_string = args
        self.value_dicts = kwargs
        self.db = pymysql.connect(config.get_conf("mysql", "host"),
                                  config.get_conf("mysql", "username"),
                                  config.get_conf("mysql", "password"))
        self.sql = []

    def run_sql(self):
        """
        连接数据库，执行sql
        """
        cursor = self.db.cursor(pymysql.cursors.DictCursor)
        # cursor.execute(sql)
        result = cursor.fetchall()
        self.db.commit()
        self.db.close()
        return result

    def get_sql_string(self):
        """
        通过方法中传入的字符串获取sql
        """
        new_sql = []
        for i in self.sql_string:
            i = globals()[i]
            new_sql += i
        print(new_sql)
        return new_sql

    def replace_sql(self):
        """
        根据生成的字典，替换sql
        """
        sql_list = self.get_sql_string()
        for i in self.value_dicts:
            self.dict[i] = self.value_dicts[i]
        for j in sql_list:
            for s in self.dict:
                if type(self.dict[s]) == int:
                    j = j.replace(f"[{s}]", f"{self.dict[s]}")
                else:
                    j = j.replace(f"[{s}]", f'"{self.dict[s]}"')
            self.sql.append(j)

    def get_sql_result(self):
        """
        链接数据库，执行sql
        """
        self.replace_sql()
        result_list = []
        for i in self.sql:
            result_list += gmc_mysql.get_database(i)
        return result_list

    def validation_sql(self):
        result = self.get_sql_result()
        print(result, self.dict)
        if result:
            for i in result:
                for j in i:
                    print("对比值", str(i[j]), str(self.dict[j]))
                    if str(i[j]) != str(self.dict[j]):
                        return False
            return True


if __name__ == '__main__':
    sql_data_dicts = basic_dict.sql_data_dicts
    s = RunSql(sql_data_dicts, "search_inhospital_patient_bed")
    print(s.validation_sql())