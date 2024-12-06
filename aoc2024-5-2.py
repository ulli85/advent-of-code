from collections import Counter
# https://www.youtube.com/watch?v=ym1ae-vBy6g

def check_update(rules: dict, updatestr: str, fix_one_error: bool) -> tuple:
    update = updatestr.split(',')
    if len(update) > 1:  # update musi byt delsi jak jedno cislo
        for i in range(1, len(update)):
            for j in range(0, i):
                if update[i] in rules and update[j] in rules[update[i]]:
                    if fix_one_error:
                        pom = update[i]
                        update[i] = update[j]
                        update[j] = pom
                    return False, ','.join(update)
    return True, updatestr

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
    check_res = check_update(rules, update, False)
    if check_res[0]:
        continue

    check_res = check_update(rules, update, True)
    while not check_res[0]:
        check_res = check_update(rules, check_res[1], True)
    result += get_middle_number(check_res[1])
print(result)
