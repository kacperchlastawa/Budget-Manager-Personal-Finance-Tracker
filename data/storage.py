import json 

def save_to_file(obj, filename):
    with open(filename, 'w') as file:
        json.dump(obj.to_dict(), file, ensure_ascii=False, indent=4)

def load_from_file(cls, filename):
    try:
        with open(filename, 'r',encoding="utf-8") as file:
            data = json.load(file)
            obj = cls()
            obj.from_dict(data)
            return obj
    except FileNotFoundError:
        print("No previous data found.")
        return cls()