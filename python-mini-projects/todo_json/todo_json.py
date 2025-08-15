import json, os

F = "todo.json"
tasks = []

if os.path.exists(F):
    with open(F) as fh:
        try:
            tasks = json.load(fh)
        except json.JSONDecodeError:
            tasks = []

while True:
    action = input("[A]dd, [L]ist, [Q]uit: ").lower()
    if action == "a":
        task = input("Task: ").strip()
        if task:
            tasks.append(task)
    elif action == "l":
        if tasks:
            for i, t in enumerate(tasks, 1):
                print(f"{i}. {t}")
        else:
            print("(no tasks yet)")
    elif action == "q":
        break

with open(F, "w") as fh:
    json.dump(tasks, fh, indent=2)
print("Tasks saved to", F)
