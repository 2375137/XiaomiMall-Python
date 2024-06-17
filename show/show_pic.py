import json


def get_shop(cat_id):
    # print(json.loads(read_scan_data())[str(cat_id)])
    with open("./show/show_pic.json", 'rt', encoding='utf-8') as f:
        content = f.read()
        f.close()
    if cat_id == "PC":
        return json.loads(content)["PC"]
    else:
        return json.loads(content)["mobile"]
