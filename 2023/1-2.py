import re
digits = {'oneight': 18, 'twone': 21, 'threeight': 38, 'fiveeight': 58, 'sevenine': 79,
          'eightwo': 82, 'eightree': 83, 'nineight': 98, 'one': 1, 'two': 2, 'three': 3,
          'four': 4, 'five': 5, 'six': 6, 'seven': 7, 'eight': 8, 'nine': 9}

def replace_2_digits(line: str) -> str:
    for key in digits.keys():
        line = line.replace(key, str(digits[key]))

    return line

print(sum(list(map(lambda numbers: int(numbers[0] + numbers[-1]), map(lambda line: re.findall('\\d', line), list(map(lambda line: replace_2_digits(line), open(
    "input/1.txt", "r").read().splitlines())))))))
