from collections import deque
import numpy as np


class State:
    VISITED_STATES:set = None
    INDICATOR_FINAL: [bool] = None
    WIRING_SCHEMA: [int] = None
    JOLTAGE_REQUIREMENT: [int] = None

    @staticmethod
    def of(line):
        State.VISITED_STATES = set()
        indicator_final = line[1:line.index(']')]
        indicator_final = [True if indicator_final[i] == '#' else False for i in range(0, len(indicator_final))]
        State.INDICATOR_FINAL = tuple(indicator_final)

        wiring_schema = list(filter(lambda ws: len(ws) > 0, line[line.index(']') + 1: line.index('{') - 1].split(' ')))
        wiring_schema = [list(map(int, schema_item[1:-1].split(','))) for schema_item in wiring_schema]
        State.WIRING_SCHEMA = wiring_schema

        joltage_requirement = list(map(int, line[line.index('{') + 1: line.index('}')].split(',')))
        State.JOLTAGE_REQUIREMENT = joltage_requirement
        indicator_actual = tuple([False] * len(State.INDICATOR_FINAL))

        return State(indicator_actual)

    def __init__(self, indicator_actual, parent: 'State' = None):
        self.indicator_actual = indicator_actual
        self.parent_state = parent
        self.deep = 0 if parent is None else parent.deep + 1
        self.schema = -1

    def press(self, schema_idx: int):
        indicator_next = [i for i in self.indicator_actual]
        for indicator_id in State.WIRING_SCHEMA[schema_idx]:
            indicator_next[indicator_id] = not self.indicator_actual[indicator_id]
        s = State(tuple(indicator_next), self)
        s.schema = schema_idx
        if s in State.VISITED_STATES:
            return None
        State.VISITED_STATES.add(s)
        return s

    def is_on(self):
        return State.INDICATOR_FINAL == self.indicator_actual

    @staticmethod
    def __print_indicator__(indicator):
        return ''.join(['#' if i else '.' for i in indicator])

    def __str__(self):
        return f"'{State.__print_indicator__(self.indicator_actual)}', Pressed: {self.schema}, On: {self.is_on()}"

    def __repr__(self):
        return self.__str__()

    def __eq__(self, other):
        return self.indicator_actual == other.indicator_actual

    def __ne__(self, other):
        return not self.__eq__(other)

    def __hash__(self):
        return hash(self.indicator_actual)

lines = open('input/10.txt').read().splitlines()

all_clicks = 0
for line in lines:
    state: State = None
    q = deque([State.of(line)])
    while q:
        s = q.popleft()
        if s.is_on():
            break
        for schema_id, schema in enumerate(State.WIRING_SCHEMA):
            s_new = s.press(schema_id)
            if s_new is not None:
                q.append(s_new)
    all_clicks += s.deep
print(all_clicks)
