from miner import AlphaMiner

# file path to txt file with logs
file_path = r'C:\Studia\S8\MiAPB\alpha_miner_project_4\logs\log4.txt'

# reading txt file and appending logs table
logs = []
with open(file_path, 'r') as file:
    for line in file:
        logs.append(line.replace('\n', '').split(' '))

# checking the logs list in console
for row in logs:
    print(row)

f = AlphaMiner(logs)
print(f.events)
print(f.matrix)
f.show()
print(f.start_events)
print(f.end_events)

relation = f.get_relation_type('A', 'B')
print(relation)