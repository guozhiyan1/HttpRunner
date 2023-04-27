import os


def get_base_file(root_path, all_files=[]):
    """
    递归函数，遍历该文档目录和子目录下的所有文件，获取其path
    """
    files = os.listdir(root_path)
    for file in files:
        if not os.path.isdir(root_path + '/' + file):  # not a dir
            all_files.append(root_path + '/' + file)
        else:  # is a dir
            get_base_file((root_path + '/' + file), all_files)
    return all_files


def get_root_path(env):
    """
    获取主路径
    """
    print(os.path.abspath(os.path.dirname(os.getcwd())))
    return os.path.abspath(os.path.dirname(os.getcwd())) + "/testcase/" + env + "/smoking"


def get_file_path(all_files):
    """
    拆分用例集和具体用例
    """
    file_dict = []
    basic = {"id": 0,
             "group_name": None,
             "testcase": None}
    for i, j in enumerate(all_files):
        j = j.split("smoking")[1].rsplit('/', 1)
        basic['id'] = i
        basic['group_name'], basic['testcase'] = j
        file_dict.append(basic)
    return file_dict


if __name__ == '__main__':
    path = get_root_path("GMC")
    file_dict = get_base_file(path)

    print(get_file_path(file_dict))