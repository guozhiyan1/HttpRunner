import os


def all_path(dirname):
    result = []
    for maindir, subdir, file_name_list in os.walk(dirname):
        # print("1:", maindir) #当前主目录
        # print("2:", subdir) #当前主目录下的所有目录
        # print("3:", file_name_list)  #当前主目录下的所有文件
        for filename in file_name_list:
            apath = os.path.join(maindir, filename)#合并成一个完整路径
            result.append(apath)
    return result


print(all_path("testcase/smoking"))

url_list = []

for path in all_path("testcase/smoking"):

    with open(path, encoding="utf-8") as f:
        for i in f.readlines():
            if "    url: " in i:
                url_list.append(i.strip("            url: ").rstrip())

print(url_list)
print(len(url_list))

