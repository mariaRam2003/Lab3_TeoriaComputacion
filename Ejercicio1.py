import networkx as nx
import matplotlib.pyplot as plt

# Función que obtiene la precedencia de un operador
def getPrecedence(c):
    precedences = {
        '(': 1,
        '|': 2,
        '.': 3,
        '?': 4,
        '*': 4,
        '+': 4,
        '^': 5
    }
    return precedences.get(c, 0)


# Función que formatea la expresión regular para agregar concatenación explícita donde sea necesario
def formatRegEx(regex):
    allOperators = ['|', '?', '+', '*', '^']
    binaryOperators = ['^', '|']

    res = ''
    for i in range(len(regex)):
        c1 = regex[i]

        # Verifica si hay otro carácter después de c1
        if i + 1 < len(regex):
            c2 = regex[i + 1]

            # Concatena c1 con el resultado, pero solo si c1 y c2 no son operadores válidos
            if c1 not in allOperators and c2 not in allOperators and c1 not in binaryOperators:
                res += c1

        # Concatena el último carácter de regex a res
        if c1 not in allOperators and c1 not in binaryOperators:
            res += c1

    return res



# Función que convierte una expresión regular de notación infix a notación postfix
def infixToPostfix(regex):
    postfix = ''  # Inicializa la notación postfix
    stack = []    # Inicializa la pila para los operadores
    formattedRegEx = formatRegEx(regex)  # Formatea la expresión regular

    # Recorre cada carácter en la expresión formateada
    for c in formattedRegEx:
        if c == '(':  # Si es paréntesis de apertura, lo agrega a la pila
            stack.append(c)
        elif c == ')':  # Si es paréntesis de cierre, saca operadores de la pila hasta encontrar el paréntesis de apertura correspondiente
            while stack and stack[-1] != '(':
                postfix += stack.pop()

            # Elimina el paréntesis de apertura de la pila
            if stack and stack[-1] == '(':
                stack.pop()
        else:  # Si es operador
            # Saca operadores de la pila y los agrega a postfix mientras la pila no esté vacía y el operador en la cima tenga mayor o igual precedencia
            while stack and getPrecedence(stack[-1]) >= getPrecedence(c):
                postfix += stack.pop()

            # Agrega el operador actual a la pila
            stack.append(c)

    # Saca los operadores restantes de la pila y los agrega a postfix
    while stack:
        postfix += stack.pop()

    return postfix

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

    # Procesa cada expresión regular en la lista expressions
    for i, expression in enumerate(expressions, start=1):
        expression = expression.strip()  # Elimina el salto de línea al final de la expresión
        postfix_expr = infixToPostfix(expression)  # Convierte la expresión a notación postfix
        print(f"Expresión {i}:")
        print("Infix:", expression)
        print("Postfix:", postfix_expr)

        #syntax_tree = buildSyntaxTree(postfix_expr)  # Construye el árbol sintáctico
        #graph = nx.DiGraph()  # Crea un nuevo grafo dirigido

        #pos = drawSyntaxTree(syntax_tree, graph)  # Dibuja el árbol sintáctico y obtiene la posición de los nodos

        # Muestra el árbol sintáctico en pantalla utilizando Matplotlib
        #plt.figure(figsize=(10, 6))
        #nx.draw(graph, pos, with_labels=True, node_size=1500, font_size=10, font_weight='bold', arrows=True)
        #plt.title(f"Árbol sintáctico - Expresión {i}")
        #plt.show()

        print("--------------------")


if __name__ == "__main__":
    main()