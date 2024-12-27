data = open("urls.json", 'r').readlines()
results_file = open("urls.txt", 'w')
for line in data:
    try:
        line = line.strip().rstrip()
        host = line.split('{"host": "', 1)[1].split('"')[0]
        port = line.split('"port": ', 1)[1].split(',')[0]
        results_file.write(f"{host}:{port}\n")
        print(f"{host}:{port}")
    except Exception as err:
        print(f"{line} ==> {err}")
results_file.close()
