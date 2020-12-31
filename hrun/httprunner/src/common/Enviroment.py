"""
获取公共变量
"""
import configparser
import os


def get_enviroment(section):
    """
    获取环境变量
    :param section:
    :return:
    """
    root_dir = os.path.abspath('.')  # 获取执行所在目录
    configPath = os.path.join(root_dir, "config.ini")
    config = configparser.ConfigParser()
    config.read(configPath, encoding='utf-8')
    return dict(config.items(section))


if __name__ == '__main__':
    x = get_enviroment("test")
    print(x)