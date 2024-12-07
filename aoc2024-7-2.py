class TreeRoot:
    def __init__(self, result, operands):
        self.result = result
        self.operands = operands
        self.childrens = []
        self.actual_value = operands[0]
        self.operation = str(self.actual_value) + ' '
        self.solution_found = False

    def build_tree(self):
        TreeNode.root = self
        child_operands = self.operands[1:]
        self.childrens.append(TreeNode('*', self, self.actual_value, child_operands))
        self.childrens.append(TreeNode('||', self, self.actual_value, child_operands))
        self.childrens.append(TreeNode('+', self, self.actual_value, child_operands))
        return self


class TreeNode:
    root: TreeRoot
    def __init__(self, operator, parent, parent_value, operands: list[int]):
        self.operator = operator
        self.parent = parent
        self.operands = operands
        self.actual_value = self.__get_actual_value(parent_value, operator)
        self.operand = operands[0]
        self.childrens = []
        self.solution_found = self.actual_value == result_of_eqation
        self.__build_children()

    def __get_actual_value(self, parent_value: int, operator: str) -> int:
        if self.operator == '||':
            return int(str(parent_value) + str(self.operands[0]))
        return int(eval(f"{parent_value} {operator} {self.operands[0]}"))

    def __build_children(self):
        if TreeNode.root.solution_found:
            return
        if self.actual_value == result_of_eqation and len(self.operands) == 1:
            TreeNode.root.solution_found = True
            #print(f"Solution found: {self.__get_equation_as_string()} == {result_of_eqation}")
        elif len(self.operands) > 1 and self.actual_value <= result_of_eqation:
            child_operands = self.operands[1:]
            self.childrens.append(TreeNode('||', self, self.actual_value, child_operands))
            self.childrens.append(TreeNode('*', self, self.actual_value, child_operands))
            self.childrens.append(TreeNode('+', self, self.actual_value, child_operands))

    def __get_equation_as_string(self) -> str:
        node = self
        nodes: list[TreeNode] = []
        while node != TreeNode.root:
            nodes.append(node)
            node = node.parent
        solution = str(TreeNode.root.actual_value)
        nodes.reverse()
        for node in nodes:
            solution += node.operator + str(node.operand)
        return solution


f = open("aoc2024-7-1-input.txt", "r")
content = f.read()
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
