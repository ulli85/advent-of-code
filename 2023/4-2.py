import re

data = open("input/4").read().splitlines()
cards = dict(zip([i for i in range(1, len(data) + 1)], len(data) * [1]))
matches = map(lambda x: re.fullmatch('^Card\\s+\\d+:\\s+(?P<winning_nums>.*)\\|\\s+(?P<mine_nums>.*)$', x), data)
for game_id, match in enumerate(matches, 1):
    matchings = {*match.group('winning_nums').split()}.intersection({*match.group('mine_nums').split()})
    card_copies = cards[game_id]
    for i in range(game_id + 1 , game_id + len(matchings) + 1):
        if i not in cards: break
        cards[i] += card_copies

print(sum(cards.values()))
