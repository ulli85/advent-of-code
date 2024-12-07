class TreeRoot:
    def __init__(self, result, operands):
        self.result = result
        self.operands = operands
        self.children_left = None
        self.children_right = None
        self.actual_value = operands[0]
        self.operation = str(self.actual_value) + ' '
        self.solution_found = False

    def build_tree(self):
        child_operands = self.operands[1:]
        self.children_left = TreeNode('+', self, self.actual_value, child_operands)
        self.children_right = TreeNode('*', self, self.actual_value, child_operands)
        return self


class TreeNode:
    def __init__(self, operator, parent, parent_value, operands: list[int]):
        self.operator = operator
        self.parent = parent
        self.actual_value = int(eval(f"{parent_value} {operator} {operands[0]}"))
        self.operands = operands
        self.operand = operands[0]
        self.children_left = None
        self.children_right = None
        self.solution_found = self.actual_value == result_of_eqation
        self.__build_children()

    def __build_children(self):
        if self.__get_tree_root().solution_found:
            print("Solution already found. Skipping build tree")
            return
        if self.actual_value == result_of_eqation and len(self.operands) == 1:
            self.__propagate_solution_found_to_root()
            print(f"Solution found: {self.__get_equation_as_string()} == {result_of_eqation}")
        elif len(self.operands) > 1:
            if self.actual_value <= result_of_eqation:
                child_operands = self.operands[1:]
                self.children_left = TreeNode('+', self, self.actual_value, child_operands)
                self.children_right = TreeNode('*', self, self.actual_value, child_operands)
            else:
                print(f"Result: {result_of_eqation}, Actual value: {self.actual_value}")
        elif len(self.operands) == 1:
            print(f"Solution not found: {self.__get_equation_as_string()} != {result_of_eqation}")
        else:
            print(f"No operands left. Result: {result_of_eqation}, Actual value: {self.actual_value}")

    def __get_tree_root(self) -> TreeRoot:
        node = self
        while type(node) is TreeNode:
            node = node.parent
        return node

    def __propagate_solution_found_to_root(self):
        root = self.__get_tree_root()
        root.solution_found = True

    def __get_equation_as_string(self) -> str:
        node = self
        nodes: list[TreeNode] = []
        while type(node) is TreeNode:
            nodes.append(node)
            node = node.parent
        solution = ''
        if type(node) is TreeRoot:
            solution += str(node.actual_value)
        nodes.reverse()
        for node in nodes:
            solution += node.operator + str(node.operand)
        return solution


f = open("aoc2024-7-1-input.txt", "r")
content = f.read()
print(content)
lines = content.splitlines()
solution = 0
for line in lines:
    data = line.split(':')
    result_of_eqation = int(data[0])
    operands = [int(x) for x in data[1].strip().split(' ')]
    tree = TreeRoot(result_of_eqation, operands).build_tree()
    if tree.solution_found:
        solution += result_of_eqation
print(solution)
