import json

with open('exJson1.json') as f: 
                data = f.read()
                js = json.loads(data) 
                print(js)
