#librerias
import tkinter as tk
import ply.lex as lex
import ctypes
import ply.yacc as yacc
from tkinter import messagebox

#variables
color_bg = "#181818" #color del fondo de la barra
ram = ""

#variables ARBOL 
NODO_RADIO = 22
X_SEP = 100     # separación horizontal entre "nodos hoja"
Y_SEP = 100     # separación vertical por nivel
MARGEN_X = 50
MARGEN_Y = 50


#Ventana principal
root = tk.Tk()
root.title("Compilador Grupo No. 10")
root.geometry("900x600")

#Los frames son los contenedores invisibles en donde se acomodan los botones, cajas de texto, y etc.
#Frame menu principal
menu_frame = tk.Frame(root, width=200, bg=color_bg)
menu_frame.pack(side="left", fill="y")
menu_frame.pack_propagate(False) #Para que el ancho no se agregue a los botones

#frame de contenido
content_frame = tk.Frame(root, bg="#7a7a7a")
content_frame.pack(side="right", fill="both", expand=True)

#Función para limpiar el contenido al cambiar de menu
def limpiar_contenido():
    for widget in content_frame.winfo_children():
        widget.destroy()

#Nombres
tk.Label(
    content_frame,
    text="""Pablo Roldan 5090-23-13164
    Oliver Ruiz 5090-23-7889
    Henry Gonzalez 5090-23-19365
    Carlos Elías 5090-23-3510
    
    Abra el editor de texto para comenzar.""",
    fg="white",
    bg="#7a7a7a",
    font=("Arial", 14, "bold"),
    justify="center"
).pack(pady=(200,10))


#---------------------------------------------------------------EDITOR DE TEXTO--------------------------------------------------------
def mostrar_editor():
    global editor
    limpiar_contenido()
    
    # Título
    titulo = tk.Label(
        content_frame,
        text="Editor de Código",
        font=("Arial", 16, "bold"),
        bg="#ecf0f1"
    )
    titulo.pack(pady=10)

    #Frame del editor
    editor_frame = tk.Frame(content_frame)
    editor_frame.pack(fill="both", expand=True, padx=10, pady=10)

    #Scrollbar vertical
    scrollbar = tk.Scrollbar(editor_frame)
    scrollbar.pack(side="right", fill="y")

    global editor #para que editor pueda usarse en todo el archivo
    # Área de texto (EDITOR)
    editor = tk.Text(
        editor_frame,
        wrap="none",
        undo=True,
        yscrollcommand=scrollbar.set,
        font=("Consolas", 12)
    )
    editor.pack(fill="both", expand=True)

    #CARGAR RAM
    global ram
    if(ram != ""):
        editor.delete("1.0", tk.END) #borra todo el texto del editor
        editor.insert("1.0",ram)
        ram = ""


    btn_guardar = tk.Button(
        content_frame,
        text="Guardar",
        command=ventana_guardar,
        width=20,
        pady=5 #espacio que sale del centro del boton hacia arriba y abajo
    )
    btn_guardar.pack(pady=(10,10), side = "right", padx=50) #pady con doble parentesis quiere decir (espacio desde arriba, espacio desde abajo)


    btn_cargar = tk.Button(
        content_frame,
        text="Cargar",
        command=ventana_cargar,
        width=20,
        pady=5 #espacio que sale del centro del boton hacia arriba y abajo
    )
    btn_cargar.pack(pady=(10,10), side="left", padx= 50) #pady con doble parentesis quiere decir (espacio desde arriba, espacio desde abajo)


    scrollbar.config(command=editor.yview)

    #Texto de ejemplo para debug
    #editor.insert("1.0", "int x = 10;\nfloat y = 5.5;\n")


#-----------------------------------MEMORIA--------------------------------------------------

def ocupar_ram():
    global ram
    if(ram == ""):
        ram = editor.get("1.0", "end-1c")

def obtener_codigo(): #FUNCION PARA OBTENER EL CODIGO
    codigo = editor.get("1.0", "end-1c") #esto quiere decir desde la primera linea hasta el final del texto (sin el salto de linea extra)
    return codigo    

def ventana_guardar():
    global texto_emergente
    global emergente
    emergente = tk.Toplevel(root)
    emergente.title("Guardar")
    emergente.geometry("400x200")    

    titulo = tk.Label(emergente, text="Ingrese nombre para guardar", font=("consolas",12)).pack(pady=20)
    texto_emergente = tk.Text(
        emergente,
        font=("Consolas", 12),
        wrap="none",
        undo=True,
        width= 20,
        height=1
    )
    texto_emergente.pack(pady=(20,2))
    
    btn_guardar = tk.Button(
        emergente,
        text = "Guardar",
        command=guardar_archivo,
        width= 20
    )
    btn_guardar.pack(pady=(25,10))



def guardar_archivo():
    codigo = obtener_codigo()
    nombre = texto_emergente.get("1.0", "end-1c")
    with open(nombre + ".txt", "w" ) as file:
        file.write(codigo)
    emergente.destroy()
    Mbox('exito', 'Se ha guardado con exito', 0)
    print("archivo guardado")

def Mbox(title, text, style):
    return ctypes.windll.user32.MessageBoxW(0, text, title, style)


def ventana_cargar():
    global texto_emergente2
    global emergente2
    emergente2 = tk.Toplevel(root)
    emergente2.title("Cargar")
    emergente2.geometry("400x200")    

    titulo = tk.Label(emergente2, text="Ingrese nombre para cargar", font=("consolas",12)).pack(pady=20)
    texto_emergente2 = tk.Text(
        emergente2,
        font=("Consolas", 12),
        wrap="none",
        undo=True,
        width= 20,
        height=1
    )
    texto_emergente2.pack(pady=(20,2))
    
    btn_cargar = tk.Button(
        emergente2,
        text = "Cargar",
        command=cargar_archivo,
        width= 20
    )
    btn_cargar.pack(pady=(25,10))

def cargar_archivo():
    nombre = texto_emergente2.get("1.0", "end-1c") + ".txt"
    try:
        with open(nombre, 'r') as file:
            contenido = file.read()
        editor.delete("1.0", tk.END) #borra todo el texto del editor
        editor.insert("1.0",contenido) #inserta el contenido del archivo al editor
        Mbox("Éxito", "El codigo se cargó correctamente",0)
        emergente2.destroy()
    except FileNotFoundError: #en caso de que el nombre no sea correcto
        Mbox("Error", "No se encuentra el archivo",0)
    except Exception as e: #en caso de cualquier otro error
        Mbox("Error", "Error",0)






#------------------------------------------------------REGLAS LEXICAS-------------------------------------------------

#Palabras reservadas
reserved = {
    'int': 'INT',
    'float': 'FLOAT',
    'if': 'IF',
    'else': 'ELSE',
    'while': 'WHILE',
    'print': 'PRINT',
    'printf': 'PRINTF',
    'return': 'RETURN'
}

#Lista de tokens
tokens = [
    'ID',
    'NUMERO',
    'OPERACION',
    'ASIGNACION',
    'PUNTOCOMA',
    'PARENTESIS',
    'LLAVES',
    'COMA',
    'COMPARACION',
    'DESC'
] + list(reserved.values())

#Definir reglas
#se debe usar regex para registrar simbolos como el + o * porque phyton los usa como palabras reservadas
t_OPERACION = r'\+ | - | \* | /'
t_ASIGNACION = r'='
t_PUNTOCOMA = r';'
t_PARENTESIS = r'\( | \)'
t_LLAVES = r'\{ | \}'
t_COMA = r','
t_COMPARACION = r'< | > | =='
t_ignore = ' \t' #saltos de linea

def t_ID(t):
    r'[a-zA-Z_][a-zA-Z_0-9]*'
    t.type = reserved.get(t.value, 'ID')
    return t

def t_NUMERO(t):
    r'\d+(\.\d+)?'
    t.value = float(t.value) if '.' in t.value else int(t.value)
    return t
#Las palabras entre comillas "" son del tipo de token DESC
def t_DESC(t):
    r'\"([^\\\n]|(\\.))*?\"'
    return t

def t_newline(t):
    r'\n+'
    t.lexer.lineno += len(t.value)

def t_error(t):
    t.lexer.skip(1)

#Construir el lexer que será pasado para mostrar el codigo
lexer = lex.lex()
#------------------------------------------------------ANALIZADOR LEXICO-------------------------------------------------


def mostrar_lexico():
    ocupar_ram()
    #Obtener código del editor
    codigo = ram
    print(codigo)

    limpiar_contenido()
    
    global tokens_text

    titulo = tk.Label(
        content_frame,
        text="Análisis Léxico",
        font=("Segoe UI", 23, "bold"),
        fg="#2c3e50"

    )
    titulo.pack(pady=10)
    
    linea = tk.Frame(content_frame, height=2, bg="#ffffff") #Linea de decoración debajo del título
    linea.pack(fill="x", padx=40, pady=(0,10))

    tokens_frame = tk.Frame(content_frame)
    tokens_frame.pack(fill="both", expand=True, padx=10, pady=10)

    scrollbar = tk.Scrollbar(tokens_frame)
    scrollbar.pack(side="right", fill="y")



    tokens_text = tk.Text( #CUADRO DE TEXTO PARA LOS TOKENS
        tokens_frame,
        font=("Courier New", 14, "bold"),
        yscrollcommand=scrollbar.set,
        state="normal",
        fg="#FFFFFF",
        bg="#1b1b1b",
        padx=15,
        pady=10
    )
    tokens_text.pack(fill="both", expand=True)
    scrollbar.config(command=tokens_text.yview)


    lexer.lineno = 1
    lexer.input(codigo)

# Encabezado
    tokens_text.insert("end", f"{'TIPO':<18}{'LEXEMA':<18}{'LÍNEA'}\n\n\n")
    
    #Iniciar los contadores en 0
    total_tokens = 0
    total_id = 0
    total_reservadas = 0
    
    
    tokens_text.tag_configure("reservadas", foreground="#cf4bff")  # naranja
    tokens_text.tag_configure("operacion", foreground="#ff2c2c")
    tokens_text.tag_configure("parentesis", foreground="#2cb2ff")
    
    # Generar tokens
    for tok in lexer:
        #Contador de tokens, palabras reservadas y variables
        total_tokens += 1
            
        if tok.type == "ID":
            total_id += 1

        if tok.type in ("INT", "FLOAT", "IF", "ELSE", "WHILE", "PRINT"):
            total_reservadas += 1
       
        #Se define el valor de mi_tag que hace referencia al color de las palabras reservadas,
        #operaciones y parentesis, e indica que color va según su tipo
        if tok.type in reserved.values():
            mi_tag = "reservadas"
        elif tok.type == 'OPERACION':
            mi_tag = "operacion"
        elif tok.type == 'PARENTESIS':
            mi_tag = "parentesis"
        else:
            mi_tag = "normal"

        #Se inserta el tipo
        tokens_text.insert("end", f"{tok.type:<19}")
            
        #Se inserta el lexema y se aplica el tag definido anteriormente
        tokens_text.insert("end", f"{str(tok.value):<19}", mi_tag)
            
        #Se inserta el número de línea y se realiza un salto de línea
        tokens_text.insert("end", f"{tok.lineno}\n")

        
    tokens_text.insert("end", "\n")
    tokens_text.insert("end", "----------------------------------------\n")
    tokens_text.insert("end", f"Total de tokens: {total_tokens}\n")
    tokens_text.insert("end", f"Total de variables: {total_id}\n")
    tokens_text.insert("end", f"Total de palabras reservadas: {total_reservadas}\n")

    tokens_text.config(state="disabled")

#------------------------------------------------------ARBOL SINTACTICO--------------------------------------------------

# Nodo AST
class Node:
    def __init__(self, label, children=None):
        self.label = label
        self.children = children or []

def make_leaf(label):
    return Node(label, [])

# Precedencia de expresiones
precedence = (
    ('nonassoc', 'IFX'),   # precedencia ficticia para IF sin ELSE
    ('nonassoc', 'ELSE'),  # ELSE tiene mayor prioridad que IFX
    ("left", "OPERACION"), # precedencia aritmetica
)

# Programa: lista de sentencias
def p_program(p):
    "program : stmts"
    p[0] = Node("PROGRAMA", p[1])

def p_stmts_opt(p):
    """stmts_opt : stmts
                | empty"""
    p[0] = p[1] if p[1] is not None else []

def p_stmts_multi(p):
    "stmts : stmts stmt"
    p[0] = p[1] + [p[2]]

def p_stmts_one(p):
    "stmts : stmt"
    p[0] = [p[1]]

def p_stmt_decl(p):
    "stmt : type ID PUNTOCOMA"
    # int y;
    p[0] = Node("DECL", [p[1], make_leaf(f"ID:{p[2]}")])

def p_stmt_decl_assign(p):
    "stmt : type ID ASIGNACION expr PUNTOCOMA"
    # int x = 10;
    p[0] = Node("DECL_ASIGN", [p[1], make_leaf(f"ID:{p[2]}"), p[4]])

def p_stmt_assign(p):
    "stmt : ID ASIGNACION expr PUNTOCOMA"
    # x = x - 1;
    p[0] = Node("ASIGN", [make_leaf(f"ID:{p[1]}"), p[3]])

def p_stmt_print_multi(p):
    "stmt : PRINT PARENTESIS args_opt PARENTESIS PUNTOCOMA"
    # p[3] será una lista de nodos (args)
    p[0] = Node("PRINT", p[3])

def p_args_opt(p):
    """args_opt : args_list
                | empty"""
    # Permite print();
    p[0] = p[1] if p[1] is not None else []

def p_args_list_single(p):
    "args_list : expr"
    p[0] = [p[1]]

def p_args_list_many(p):
    "args_list : args_list COMA expr"
    # Forma iterativa: acumula
    p[0] = p[1] + [p[3]]

def p_stmt_if_no_else(p):
    "stmt : IF PARENTESIS condition PARENTESIS block %prec IFX"
    # IF con 2 hijos: condición y bloque THEN
    p[0] = Node("IF", [p[3], p[5]])

def p_stmt_if_with_else(p):
    "stmt : IF PARENTESIS condition PARENTESIS block ELSE block"
    # IF con 3 hijos: condición, bloque THEN, y un nodo ELSE que contiene su bloque
    p[0] = Node("IF", [p[3], p[5], Node("ELSE", [p[7]])])

def p_stmt_while(p):
    "stmt : WHILE PARENTESIS condition PARENTESIS block"
    p[0] = Node("WHILE", [p[3], p[5]])

# Tipos
def p_type_int(p):
    "type : INT"
    p[0] = Node("TIPO:int")

def p_type_float(p):
    "type : FLOAT"
    p[0] = Node("TIPO:float")

# Se usa parentesis como bloque para agrupar ( ... )
def p_block(p):
    "block : PARENTESIS stmts_opt PARENTESIS"
    p[0] = Node("BLOQUE", p[2])

# Condiciones
def p_condition_gt(p):
    "condition : expr COMPARACION expr"
    p[0] = Node("CONDICION", [p[1], p[3]])

# Expresiones con operadores
def p_expr_binop(p):
    "expr : expr OPERACION expr"
    op = p[2].strip()
    p[0] = Node(op, [p[1], p[3]])

def p_expr_group(p):
    "expr : PARENTESIS expr PARENTESIS"
    p[0] = p[2]

def p_expr_id(p):
    "expr : ID"
    p[0] = Node(f"ID:{p[1]}")

def p_expr_num(p):
    "expr : NUMERO"
    p[0] = Node(f"NUM:{p[1]}")

def p_expr_desc(p):
    "expr : DESC"
    p[0] = Node(f"DESC:{p[1]}")

def p_empty(p):
    "empty :"
    p[0] = None

def p_error(p):
    if p:
        messagebox.showinfo("Error", f"Error de sintaxis en token {p.type} ({p.value}) linea {p.lineno}")
        raise SyntaxError(f"Error de sintaxis en token {p.type} ({p.value}) linea {p.lineno}")
    messagebox.showinfo("Error", "Error de sintaxis al final del archivo")
    raise SyntaxError("Error de sintaxis al final del archivo")

parser = yacc.yacc(start="program")

def node_to_dict(n):
    return {
        "label": n.label,
        "children": [node_to_dict(c) for c in n.children]
    }

def count_leaves(node):
    """Cantidad de hojas en el subarbol (para asignar ancho)"""
    children = node.get("children", [])
    if not children:
        return 1
    return sum(count_leaves(ch) for ch in children)

def layout_tree(node, depth=0, x0=0, positions=None):
    """
    Asigna a cada nodo:
      - _x: centro del subarbol en unidades de hoja
      - _y: profundidad (nivel)
    x0 es el inicio (en unidades hoja) del bloque que ocupa este subarbol
    """
    if positions is None:
        positions = []

    children = node.get("children", [])
    y = depth

    if not children:
        # hoja: su centro está en x0 + 0.5 (medio de su "unidad")
        x_center = x0 + 0.5
        node["_x"] = x_center
        node["_y"] = y
        positions.append(node)
        return x0 + 1  # consume 1 unidad hoja

    # nodo interno: asignar layout a hijos en secuencia
    cur = x0
    child_centers = []
    for ch in children:
        cur_next = layout_tree(ch, depth + 1, cur, positions)
        child_centers.append(ch["_x"])
        cur = cur_next

    # centro del padre = promedio de centros de hijos
    x_center = sum(child_centers) / len(child_centers)
    node["_x"] = x_center
    node["_y"] = y
    positions.append(node)
    return cur  # devuelve hasta dónde llegó (en unidades hoja)

def to_canvas_coords(node):
    """Convierte coordenadas del layout (unidades) a píxeles del Canvas."""
    x = MARGEN_X + node["_x"] * X_SEP
    y = MARGEN_Y + node["_y"] * Y_SEP
    return x, y

def draw_node(canvas, x, y, text):
    canvas.create_oval(x - NODO_RADIO, y - NODO_RADIO, x + NODO_RADIO, y + NODO_RADIO,
                       outline="black", width=2, fill="white")
    canvas.create_text(x, y, text=text, font=("Arial", 14, "bold"))

def draw_edge(canvas, x1, y1, x2, y2):
    canvas.create_line(x1, y1 + NODO_RADIO, x2, y2 - NODO_RADIO, width=2)

def dibujar_arbol(canvas, root):
    # 1) calcular layout
    positions = []
    layout_tree(root, depth=0, x0=0, positions=positions)

    # 2) dibujar lineas
    def draw_edges_rec(node):
        x1, y1 = to_canvas_coords(node)
        for ch in node.get("children", []):
            x2, y2 = to_canvas_coords(ch)
            draw_edge(canvas, x1, y1, x2, y2)
            draw_edges_rec(ch)

    draw_edges_rec(root)

    # 3) dibujar nodos
    def draw_nodes_rec(node):
        x, y = to_canvas_coords(node)
        draw_node(canvas, x, y, node["label"])
        for ch in node.get("children", []):
            draw_nodes_rec(ch)

    draw_nodes_rec(root)

def mostrar_arbol():
    ocupar_ram()
    #Obtener código del editor
    codigo = ram
    print(codigo)

    limpiar_contenido()

    titulo = tk.Label(
        content_frame,
        text="Arbol Sintactico",
        font=("Segoe UI", 23, "bold"),
        fg="#2c3e50"
    )
    titulo.pack(pady=10)

    arbol_frame = tk.Frame(content_frame)
    arbol_frame.pack(fill="both", expand=True, padx=10, pady=10)
    ast = parser.parse(codigo, lexer=lexer)

    canvas = tk.Canvas(arbol_frame, bg="white")
    canvas.pack(fill='both', expand=True)
    vbar = tk.Scrollbar(arbol_frame, orient='vertical', command=canvas.yview)
    hbar = tk.Scrollbar(arbol_frame, orient='horizontal', command=canvas.xview)
    canvas.configure(yscrollcommand=vbar.set, xscrollcommand=hbar.set)
    canvas.grid(row=0, column=0, sticky='nsew')
    vbar.grid(row=0, column=1, sticky='ns')
    hbar.grid(row=1, column=0, sticky='ew')
    arbol_frame.grid_rowconfigure(0, weight=1)
    arbol_frame.grid_columnconfigure(0, weight=1)
    tree_dict = node_to_dict(ast)
    dibujar_arbol(canvas, tree_dict)
    canvas.config(scrollregion=canvas.bbox("all"))

#------------------------------------------------------TABLA DE SIMBOLOS-------------------------------------------------

def mostrar_tabla():
    ocupar_ram()
    codigo = ram
    limpiar_contenido()

    nuevo_lexer = lex.lex()
    nuevo_lexer.lineno = 1
    nuevo_lexer.input(codigo)

    tokens_lista = list(nuevo_lexer)

    titulo = tk.Label(
        content_frame,
        text="Tabla de símbolos",
        font=("Segoe UI", 23, "bold"),
        fg="#2c3e50"
    )
    titulo.pack(pady=10)

    frame = tk.Frame(content_frame)
    frame.pack(fill="both", expand=True, padx=10, pady=10)

    scrollbar = tk.Scrollbar(frame)
    scrollbar.pack(side="right", fill="y")

    tabla_text = tk.Text(
        frame,
        font=("Courier New", 13),
        yscrollcommand=scrollbar.set,
        fg="#FFFFFF",
        bg="#1b1b1b",
        padx=15,
        pady=10
    )
    tabla_text.pack(fill="both", expand=True)
    scrollbar.config(command=tabla_text.yview)

    # Encabezado
    tabla_text.insert("end", 
        f"{'Nombre':<15}"
        f"{'Tipo':<12}"
        f"{'Categoría':<15}"
        f"{'Valor':<10}"
        f"{'Línea'}\n"
    )
    tabla_text.insert("end", "-"*65 + "\n")

    simbolos = {}
    tipo_actual = None
    ultimo_id = None

    for i, tok in enumerate(tokens_lista):

        # Detectar tipo declarado
        if tok.type in ("INT", "FLOAT"):
            tipo_actual = tok.value

        # Detectar identificador
        elif tok.type == "ID":
            ultimo_id = tok.value

            if tok.value not in simbolos:
                simbolos[tok.value] = {
                    "tipo": tipo_actual if tipo_actual else "-",
                    "categoria": "variable",
                    "valor": "-",
                    "linea": tok.lineno
                }

        # Detectar asignación
        elif tok.type == "ASIGNACION" and ultimo_id:
            # Buscar el siguiente token (valor)
            if i+1 < len(tokens_lista):
                siguiente = tokens_lista[i+1]
                if siguiente.type in ("NUMERO", "DESC"):
                    simbolos[ultimo_id]["valor"] = str(siguiente.value)

    # Imprimir tabla
    for nombre, datos in simbolos.items():
        tabla_text.insert(
            "end",
            f"{nombre:<15}"
            f"{datos['tipo']:<12}"
            f"{datos['categoria']:<15}"
            f"{datos['valor']:<10}"
            f"{datos['linea']}\n"
        )

    tabla_text.config(state="disabled")


#----------------------------------------------BOTONES Y TITULO EN BARRA-----------------------------------------------

label = tk.Label( #TITULO EN LA BARRA
    menu_frame, 
    text = "Compiladores\nProyecto No. 1\nGrupo No. 10",
    fg="white",
    bg=color_bg,
    font=("Arial", 14, "bold"),
    justify="center"
)
label.pack(pady=20)

#BOTONES DEL MENU
btn_editor = tk.Button(
    menu_frame,
    text="Editor de texto",
    command=mostrar_editor,
    width=20,
    pady=5 #espacio que sale del centro del boton hacia arriba y abajo
)
btn_editor.pack(pady=(40,10)) #pady con doble parentesis quiere decir (espacio desde arriba, espacio desde abajo)

btn_lexico = tk.Button(
    menu_frame,
    text="Análisis léxico",
    command=mostrar_lexico,
    width=20,
    pady=5
)
btn_lexico.pack(pady=10)

btn_sintactico = tk.Button(
    menu_frame,
    text="Árbol sintáctico",
    command=mostrar_arbol,
    width=20,
    pady=5
)
btn_sintactico.pack(pady=10)

btn_tabla = tk.Button(
    menu_frame,
    text="Tabla de símbolos",
    command=mostrar_tabla,
    width=20,
    pady=5
)
btn_tabla.pack(pady=10)

btn_salir = tk.Button(
    menu_frame,
    text="Salir",
    command=root.destroy, #comando para cerrar
    width=20,
    pady=5
)
btn_salir.pack(pady=30)


root.mainloop() #LOOP PARA VENTANA SIEMPRE DEBE IR DE ULTIMO
