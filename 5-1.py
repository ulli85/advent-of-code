def check_update(rules: dict, updatestr: str) -> bool:
    update = updatestr.split(',')
    if len(update) > 1:  # update musi byt delsi jak jedno cislo
        for i in range(1, len(update)):
            for j in range(0, i):
                if update[i] in rules and update[j] in rules[update[i]]:
                    return False
    return True


def get_middle_number(updatestr: str) -> int:
    numbers = (updatestr.split(','))
    index = int((len(numbers) - 1) / 2)
    return int(numbers[index])


f = open("aoc2024-5-1-input.txt", "r")
content = f.read()
lines = content.splitlines()
rules = {}
idx = 0
for line in lines:
    idx += 1
    if line.find('|') > 0:
        rule = line.split('|')
        if rule[0] in rules:
            rules[rule[0]].add(rule[1])
        else:
            rules[rule[0]] = {rule[1]}
    if line == '':
        break

result = 0
for update in lines[-len(lines) + idx:]:
    if check_update(rules, update):
        result += get_middle_number(update)
print(result)
