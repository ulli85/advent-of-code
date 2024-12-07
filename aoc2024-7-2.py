class TreeRoot:
    def __init__(self, result, operands):
        self.result = result
        self.operands = operands
        self.childrens = []
        self.actual_value = operands[0]
        self.solution_found = False
        self.leaf_with_solution: TreeNode = None

    def build_tree(self):
        TreeNode.root = self
        add_children(self)
        return self

    def get_solution_of_equation(self) -> str:
        if self.leaf_with_solution is not None:
            node = self.leaf_with_solution
            nodes: list[TreeNode] = []
            while node != self:
                nodes.append(node)
                node = node.parent
            solution = str(self.actual_value)
            nodes.reverse()
            for node in nodes:
                solution += node.operator + str(node.operand)
            return f"{self.result} = {solution}"
        return 'Solution not found yet'


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
            TreeNode.root.leaf_with_solution = self
        elif len(self.operands) > 1 and self.actual_value <= result_of_eqation:
            add_children(self)


def add_children(node: TreeRoot | TreeNode):
    child_operands = node.operands[1:]
    node.childrens.append(TreeNode('*', node, node.actual_value, child_operands))
    node.childrens.append(TreeNode('||', node, node.actual_value, child_operands))
    node.childrens.append(TreeNode('+', node, node.actual_value, child_operands))


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
        print(tree.get_solution_of_equation())
        solution += result_of_eqation
print(solution)
