
# open "Historia transakcji.csv" and load it into a list
with open("Historia transakcji.csv", "r", encoding="UTF-8") as f:
    lines = f.readlines()

for line in lines:
    line = line.replace('"', '').replace("\ufeff", "").replace("\n", "")
transactions = {}
headers = lines[0].split(";")
lines.pop(0)

# revert lines list
lines.reverse()
start = 0
finish = 0
sum = 0
for line in lines:
    if "NEU-PLN" in line:
        line = line.split(";")
        if line[2] == '"Kupno"':
            sum -= float(line[6].replace(",", ".").replace('"', ""))
            start += float(line[6].replace(",", ".").replace('"', ""))
        if line[2] == '"Sprzedaż"':
            sum += float(line[6].replace(",", ".").replace('"', ""))
            finish += float(line[6].replace(",", ".").replace('"', ""))

print(f"On plus: {round(sum ,2)} PLN")
