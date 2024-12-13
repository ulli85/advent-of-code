class TreeRoot:
    def __init__(self, result_of_equation, operands):
        self.result_of_equation = result_of_equation
        self.operands = operands
        self.children = []
        self.actual_value = operands[0]
        self.solution_found = False
        self.leaf_with_solution: TreeNode = None

    def build_tree(self):
        TreeNode.root = self
        add_children(self, self.operands)
        return self


class TreeNode:
    root: TreeRoot

    def __init__(self, operator, parent, parent_value, operands: list[int]):
        self.operator = operator
        self.parent = parent
        self.operand = operands[0]
        self.actual_value = self.apply_operator(parent_value)
        self.childrens = []
        self.solution_found = self.actual_value == TreeNode.root.result_of_equation
        self.__build_children(operands)

    def apply_operator(self, parent_value) -> int:
        if self.operator == '||':
            return int(str(parent_value) + str(self.operand))
        return int(eval(f"{parent_value} {self.operator} {self.operand}"))

    def __build_children(self, operands: list[int]):
        if TreeNode.root.solution_found:
            return
        if self.actual_value == TreeNode.root.result_of_equation and len(operands) == 1:
            TreeNode.root.solution_found = True
            TreeNode.root.leaf_with_solution = self
        elif len(operands) > 1 and self.actual_value <= TreeNode.root.result_of_equation:
            add_children(self, operands)

def add_children(node: TreeRoot | TreeNode, operands: list[int]):
    child_operands = operands[1:]
    node.children.append(TreeNode('*', node, node.actual_value, child_operands))
    node.children.append(TreeNode('||', node, node.actual_value, child_operands))
    node.children.append(TreeNode('+', node, node.actual_value, child_operands))

f = open("7-1-input.txt", "r")
content = f.read()
lines = content.splitlines()
solution = 0
for line in lines:
    data = line.split(':')
    result_of_equation = int(data[0])
    operands = [int(x) for x in data[1].strip().split(' ')]
    tree = TreeRoot(result_of_equation, operands).build_tree()
    solution += result_of_equation if tree.solution_found else 0
print(solution)
