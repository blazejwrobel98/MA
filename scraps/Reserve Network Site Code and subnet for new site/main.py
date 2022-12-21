

with open("task.csv", "r") as f:
    tasks = f.read().split("\n")

sum = {}
corr = []
for task in tasks:
    if "Size on the requested subnet:" in task:
        corr.append(task)
        task = task.split(": ")
        if task[1] == "24":
            task[1] = "/24"
        if task[1] == "22":
            task[1] = "/22"
        if task[1] in sum:
            sum[task[1]] += 1
        else:
            sum[task[1]] = 1
full = len(corr)
# sort sum descending
sum = {k: v for k, v in sorted(sum.items(), key=lambda item: item[1], reverse=True)}

for key in sum:
    print(f"{key}: {sum[key]} ({round(sum[key] / full * 100, 2)}%)")
