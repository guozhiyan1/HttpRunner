def make_validate():
    with open("validate", "r+", encoding="utf-8") as f:
        for i in f.readlines():
            s = i.strip().replace("\"", "").split(":")[0]
            print("- " + s + ": "+ "content.body.0." + s)


if __name__ == "__main__":
    make_validate()