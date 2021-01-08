import json
with open("interface", encoding="utf-8") as f:
    dicts = json.load(f)
    paths = dicts["paths"]
    basepath = dicts["basePath"]
    new_dict = {}
    for k in paths:
        key = basepath + k
        try:
            if paths[k].get("post"):
                new_dict[key] = paths[k]["post"]["summary"]
            else:
                new_dict[key] = paths[k]["get"]["summary"]
        except:
            print(paths[k])


with open("all_interface", "a+", encoding="utf-8", ) as f:
    for i in new_dict:
        f.write(f"{i}  {new_dict[i]}\n")

