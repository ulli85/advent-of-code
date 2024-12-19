input = open("input/19-1.txt").read().splitlines()
patterns = input[0].split(', ')
designs = input[2::]
patterns.sort()
designs.sort()
print(f'{patterns}\n{designs}')

def get_unique_patterns() -> {}:
    len2pt = {} # key is pattern_len, value list of patterns with pattern_len
    min_len = 99999 # lowest len of all patterns found
    max_len = 0 # highest len of all patterns found
    for pattern in patterns:
        length = len(pattern)
        if min_len > length: min_len = length
        if max_len < length:max_len = length
        if length in len2pt:
            len2pt[length].append(pattern)
        else:
            pt = [pattern]
            len2pt[length] = pt
    for i in (2, max_len): # for all longer patterns with len 2+
        filtered = []
        if i in len2pt: # if such a longer pattern exists
            unfiltered_patterns_with_len_i = len2pt[i]
            for pattern_len_i in unfiltered_patterns_with_len_i: # for all patterns with fixed len
                full_pattern_with_len_i = pattern_len_i
                for j in (i-1, 0, -1): # (i-1, 1, -1)? for all subpatterns of size i-1 to 1
                    if j in len2pt: # if subpattern exist
                        sub_patterns = len2pt[j] # get all subpatterns
                        match = True
                        while match and len(pattern_len_i) > 0: # while longer pattern startswith subpattern we do its substring
                            match = False
                            for sub_pattern in sub_patterns:
                                if pattern_len_i.startswith(sub_pattern): # if longer pattern contains subpattern, cut it off
                                    match = True
                                    pattern_len_i = pattern_len_i[len(sub_pattern)::]
                if len(pattern_len_i) > 0: # longer pattern cannot be fully composed by subpatterns - we add it to list
                    filtered.append(full_pattern_with_len_i)

            if len(filtered) == 0: len2pt.pop(i) # all longer patterns that could be composed by its subpatterns we dispose
            else: len2pt[i] = filtered  # unique longer patterns left
    return len2pt


ptlen_2_unique_patterns_lst = get_unique_patterns()
print(ptlen_2_unique_patterns_lst)
# now we create set of unique patterns
unique_patterns_set = set()
for uniq_patterns_lst in ptlen_2_unique_patterns_lst.values():
    for uniq_pattern in uniq_patterns_lst:
        unique_patterns_set.add(uniq_pattern)
print(unique_patterns_set)

possible_cnt = 0
# we try to compose design with unique patterns we have
pattern_lens = list(ptlen_2_unique_patterns_lst.keys())
pattern_lens.sort()
pattern_lens.reverse() # longer keys first
print(pattern_lens)
for design in designs:
    tmp_design = design
    match = True
    while len(tmp_design) > 0 and match:
        match = False
        # check longest patterns first
        for ptlen in pattern_lens: # for all length of patterns
            if ptlen <= len(tmp_design):
                if tmp_design[0:ptlen] in unique_patterns_set:
                    tmp_design = tmp_design[ptlen::]
                    match = True

    if len(tmp_design) == 0: possible_cnt += 1
    else: print(design)
print(possible_cnt)
