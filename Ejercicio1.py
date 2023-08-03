import networkx as nx
import matplotlib.pyplot as plt

# Función que convierte una expresión regular de notación infix a notación postfix usando Shunting Yard
def infixToPostfix(expression):
    operators = {
        '+': 1,
        '-': 1,
        '*': 2,
        '/': 2,
        '^': 3
    }
    stack_operators = []
    output = []

    for token in expression:
        if token.isdigit():
            output.append(token)
        elif token == '(':
            stack_operators.append(token)
        elif token == ')':
            while stack_operators and stack_operators[-1] != '(':
                output.append(stack_operators.pop())
            stack_operators.pop()  # Discard the opening parenthesis
        else:
            while stack_operators and operators.get(token, 0) <= operators.get(stack_operators[-1], 0):
                output.append(stack_operators.pop())
            stack_operators.append(token)

    while stack_operators:
        output.append(stack_operators.pop())

    return output

# Definición de la clase Nodo para el árbol sintáctico
class Node:
    def __init__(self, value):
        self.value = value
        self.left = None
        self.right = None


# Función para construir el árbol sintáctico a partir de la expresión postfix
def buildSyntaxTree(postfix_expr):
    stack = []
    operators = {'|', '.', '?', '*', '+'}

    for c in postfix_expr:
        if c not in operators:
            node = Node(c)
            stack.append(node)
        else:
            right_operand = stack.pop()
            left_operand = stack.pop()
            node = Node(c)
            node.left = left_operand
            node.right = right_operand
            stack.append(node)

    return stack.pop()

# Función para dibujar el árbol sintáctico utilizando NetworkX y Matplotlib
def drawSyntaxTree(node, graph, parent_node=None, pos=None):
    graph.add_node(node.value)

    if parent_node is not None:
        graph.add_edge(parent_node.value, node.value)

    if pos is None:
        pos = {node.value: (0, 0)}

    if node.left is not None:
        pos[node.left.value] = (pos[node.value][0] - 1, pos[node.value][1] - 1)
        drawSyntaxTree(node.left, graph, node, pos)

    if node.right is not None:
        pos[node.right.value] = (pos[node.value][0] + 1, pos[node.value][1] - 1)
        drawSyntaxTree(node.right, graph, node, pos)

    return pos


# Función principal que procesa las expresiones regulares
def main():
    with open("expresiones.txt", "r", encoding='utf-8') as file:
        expressions = file.readlines()

    # Process each infix expression in the list expressions
    for i, expression in enumerate(expressions, start=1):
        # Split the infix expression into tokens (space-separated) before passing it to the function
        infix_tokens = expression.split()
        postfix_expression = infixToPostfix(infix_tokens)
        print(f"Expression {i}: {' '.join(postfix_expression)}")

        #syntax_tree = buildSyntaxTree(postfix_expr)  # Construye el árbol sintáctico
        #graph = nx.DiGraph()  # Crea un nuevo grafo dirigido

        #pos = drawSyntaxTree(syntax_tree, graph)  # Dibuja el árbol sintáctico y obtiene la posición de los nodos

        # Muestra el árbol sintáctico en pantalla utilizando Matplotlib
        #plt.figure(figsize=(10, 6))
        #nx.draw(graph, pos, with_labels=True, node_size=1500, font_size=10, font_weight='bold', arrows=True)
        #plt.title(f"Árbol sintáctico - Expresión {i}")
        #plt.show()

        print("--------------------------")


if __name__ == "__main__":
    main()