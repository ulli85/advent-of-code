input = open("input/19-1.txt").read().splitlines()
PATTERNS = input[0].split(', ')
DESIGNS = input[2::]
LEN2PT = {}  # key is pattern_len, value list of unique patterns with length pattern_len

def init_len2patttern_dictionary():
    # find boundaries
    min_len = 99999  # lowest len of all patterns found
    max_len = 0  # highest len of all patterns found

    for pattern in PATTERNS:
        length = len(pattern)
        if min_len > length: min_len = length
        if max_len < length: max_len = length

    LEN2PT[min_len] = []
    for pattern in PATTERNS:
        if len(pattern) == min_len:
            LEN2PT[min_len].append(pattern)  # shortest patterns (should be a set)

    # add unique patterns only to len2pt dictionary
    for i in range(min_len + 1, max_len + 1):
        for pattern in PATTERNS:
            if len(pattern) == i:
                if is_composable(pattern): continue
                if i not in LEN2PT:
                    LEN2PT[i] = [pattern]
                else:
                    LEN2PT[i].append(pattern)


def create_unique_patterns_set() -> set:
    unique_patterns_set = set()
    for uniq_patterns_lst in LEN2PT.values():
        for uniq_pattern in uniq_patterns_lst:
            unique_patterns_set.add(uniq_pattern)
    return unique_patterns_set


def is_composable(pattern: str) -> bool:
    tmp = pattern
#    print(pattern)
    pattern_lens = sorted(list(LEN2PT.keys()), reverse=True)  # longest apply first
    max_len_2_apply = pattern_lens[0]
    match = True
    uniq_patterns = create_unique_patterns_set()
    applied_lens = []
    applied_patterns = []
    while len(tmp) > 0 and match:
        match = False
        # check longest patterns first
        for ptlen in pattern_lens:  # for all length of patterns
            if ptlen > max_len_2_apply: continue
            if ptlen <= len(tmp):
                prefix = tmp[0:ptlen]
                if prefix in uniq_patterns:
                    applied_patterns.append(prefix)
                    tmp = tmp[ptlen:]
                    #print(tmp + '  ' + '|'.join(applied_patterns))
                    match = True
                    applied_lens.append(ptlen)
                    max_len_2_apply = len(tmp)
                    break
        # back_track rules
        if not match and len(applied_lens) > 0:
#            print(tmp + '  ' + '|'.join(applied_patterns))
            last_applied_len = applied_lens[-1]
            if last_applied_len == 1:
                applied_lens.pop()
                last_pattern = applied_patterns.pop()
                if len(applied_lens) == 0: break  # cannot apply anything else
                tmp = last_pattern + tmp # rollback 1 char change
 #               print('rooll1 ' + tmp)
              #  print(applied_lens)
            last_pattern = applied_patterns.pop()
            last_applied_len = applied_lens.pop()
            tmp = last_pattern + tmp   # rollback change
#            print('rooll2 ' + tmp)
         #   print(applied_lens)
            max_len_2_apply = last_applied_len - 1
            match = True
    return len(tmp) == 0

def test_unique_patterns():
    for pattern in PATTERNS:
        if is_composable(pattern): continue
        raise Exception(f"Pattern {pattern} is not composable")


init_len2patttern_dictionary()
test_unique_patterns()
print(LEN2PT)
#print(PATTERNS)
DESIGNS.sort()
#print(DESIGNS)
composable_designs = 0
for design in DESIGNS:
    if is_composable(design): composable_designs += 1

print(composable_designs)
