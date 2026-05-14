#librerias
import tkinter as tk
import ply.lex as lex
import ctypes
import ply.yacc as yacc
from tkinter import messagebox

#para generar obj y exe con cmd
import os
import subprocess


#variables
color_bg = "#181818" #color del fondo de la barra
ram = ""
nombre_asm = "programa"

#variables ARBOL 
NODO_RADIO = 22
X_SEP = 250     # separación horizontal entre "nodos hoja"
Y_SEP = 100     # separación vertical por nivel
MARGEN_X = 50
MARGEN_Y = 50

#Variables arbol semantico

#Ventana principal
root = tk.Tk()
root.title("Compiladores Proyecto Final III (Grupo No. 10)")
root.geometry("900x600")


nombre_archivo_var = tk.StringVar() #variable que siempre esta escuchando para el label de editor
nombre_archivo_var.set("Archivo actual: Ninguno")

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
    text="""
    Grupo No. 10

    Integrantes:
    Pablo Roldan 5090-23-13164
    Oliver Ruiz 5090-23-7889
    Henry Gonzalez 5090-23-19365
    Carlos Elías 5090-23-3510
    
    Instrucciones:
    Para comenzar abra el editor de texto y cargue o cree un programa válido.""",
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
    
    #MOSTRAR NOMBRE DEL ARCHIVO-----------------------------------

    nombrearch = tk.Label(
        content_frame,
        textvariable=nombre_archivo_var, #texto que siempre esta escuchando
        font=("Arial", 11),
        bg="#ecf0f1"
    )
    nombrearch.pack()

    #------------------------------------------------------

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
    
    #AUTOFOCUS
    texto_emergente.focus_set()

    btn_guardar = tk.Button(
        emergente,
        text = "Guardar",
        command=guardar_archivo,
        width= 20
    )
    btn_guardar.pack(pady=(25,10))

    #para guardar cuando se presione enter
    def presionar_enter(event):
        btn_guardar.invoke()

    texto_emergente.bind("<Return>", presionar_enter) #leer en esta ventana si se presiona enter


def guardar_archivo():
    codigo = obtener_codigo()
    nombre = texto_emergente.get("1.0", "end-1c")
    global nombre_archivo_var
    nombre_archivo_var.set("Archivo actual: "+ nombre +".txt")
    texto_emergente.delete("1.0", "end")
    direccion = "CODIGOS/" + nombre + ".txt"
    with open(direccion, "w" ) as file:
        file.write(codigo)
    emergente.destroy()
    Mbox('exito', 'Se ha guardado con exito', 0)
    #print("archivo guardado")

def Mbox(titulo, texto, estilo):
    return ctypes.windll.user32.MessageBoxW(0, texto, titulo, estilo)

def ventana_cargar(): #ventana emergente de cargar
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
    
     #AUTOFOCUS
    texto_emergente2.focus_set()

    btn_cargar = tk.Button(
        emergente2,
        text = "Cargar",
        command=cargar_archivo,
        width= 20
    )
    btn_cargar.pack(pady=(25,10))

    #Para cargar al presionar enter
    def presionar_enter(event):
        btn_cargar.invoke()
    
    texto_emergente2.bind("<Return>", presionar_enter) #leer en esta ventana si se presiona enter

def cargar_archivo():
    nombre = texto_emergente2.get("1.0", "end-1c") + ".txt"
    global nombre_archivo_var
    nombre_archivo_var.set("Archivo actual: "+ nombre)
    print(nombre_archivo_var)
    texto_emergente2.delete("1.0", "end") #limpia la ventana emergente
    direccion = "CODIGOS/" + nombre
    try:
        with open(direccion, 'r') as file:
            contenido = file.read()
        editor.delete("1.0", tk.END) #borra todo el texto del editor
        editor.insert("1.0",contenido) #inserta el contenido del archivo al editor
        Mbox("Éxito", "El codigo se cargó correctamente",0)
        emergente2.destroy()
    except FileNotFoundError: #en caso de que el nombre no sea correcto
        Mbox("Error", "No se encuentra el archivo",0)
    except Exception as e: #en caso de cualquier otro error
        Mbox("Error", "Error",0)



#------------------------------------------------------REGLAS LEXICAS (LEXER)-------------------------------------------------

# =====================================================
# PALABRAS RESERVADAS
# =====================================================

reservadas = {

    'int': 'INT',
    'float': 'FLOAT',

    'if': 'IF',
    'else': 'ELSE',
    'while': 'WHILE',

    'print': 'PRINT',
    'printf': 'PRINTF',

    'return': 'RETURN'
}

# =====================================================
# TOKENS
# =====================================================

tokens = [

    # Identificadores y literales
    'ID',
    'NUMERO',
    'CADENA',

    # Operadores aritméticos
    'SUMA',
    'RESTA',
    'MULTIPLICACION',
    'DIVISION',

    # Asignación
    'ASIGNACION',

    # Comparaciones
    'COMPARACION',

    # Símbolos
    'PUNTOCOMA',
    'COMA',

    # Paréntesis
    'PARENTESIS_IZQ',
    'PARENTESIS_DER',

    # Llaves
    'LLAVE_IZQ',
    'LLAVE_DER'

] + list(reservadas.values())

# =====================================================
# TOKENS SIMPLES
# =====================================================

t_SUMA = r'\+'
t_RESTA = r'-'
t_MULTIPLICACION = r'\*'
t_DIVISION = r'/'

# IMPORTANTE:
# COMPARACION debe ir antes que ASIGNACION
# para que == no se rompa en = =
def t_COMPARACION(t):
    r'<=|>=|==|!=|<|>'
    return t

def t_ASIGNACION(t):
    r'='
    return t

t_PUNTOCOMA = r';'
t_COMA = r','

t_PARENTESIS_IZQ = r'\('
t_PARENTESIS_DER = r'\)'

t_LLAVE_IZQ = r'\{'
t_LLAVE_DER = r'\}'

# Ignorar espacios y tabs
t_ignore = ' \t'

# =====================================================
# IDENTIFICADORES
# =====================================================

def t_ID(t):
    r'[a-zA-Z_][a-zA-Z_0-9]*'

    t.type = reservadas.get(t.value, 'ID')

    return t

# =====================================================
# NÚMEROS
# =====================================================

def t_NUMERO(t):
    r'\d+(\.\d+)?'

    if '.' in t.value:
        t.value = float(t.value)
    else:
        t.value = int(t.value)

    return t

# =====================================================
# CADENAS
# =====================================================

def t_CADENA(t):
    r'\"([^\\\n]|(\\.))*?\"'

    return t

# =====================================================
# NUEVAS LÍNEAS
# =====================================================

def t_newline(t):
    r'\n+'

    t.lexer.lineno += len(t.value)

# =====================================================
# ERRORES
# =====================================================

def t_error(t):

    print(
        f"Carácter ilegal '{t.value[0]}' "
        f"en línea {t.lineno}"
    )

    t.lexer.skip(1)

# =====================================================
# CONSTRUIR LEXER
# =====================================================

lexer = lex.lex()
#------------------------------------------------------ANALIZADOR LEXICO-------------------------------------------------

def mostrar_lexico():
    ocupar_ram()
    #Obtener código del editor
    codigo = ram
    #print(codigo)

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
    
    
    # Colores
    tokens_text.tag_configure("reservadas", foreground="#cf4bff")
    tokens_text.tag_configure("operacion", foreground="#ff2c2c")
    tokens_text.tag_configure("parentesis", foreground="#2cb2ff")

    # Generar tokens
    for tok in lexer:

        total_tokens += 1

        if tok.type == "ID":
            total_id += 1

        if tok.type in (
            "INT",
            "FLOAT",
            "IF",
            "ELSE",
            "WHILE",
            "PRINT"
        ):
            total_reservadas += 1

        # Selección de color
        if tok.type in reservadas.values():

            mi_tag = "reservadas"

        elif tok.type in (
            'SUMA',
            'RESTA',
            'MULTIPLICACION',
            'DIVISION'
        ):

            mi_tag = "operacion"

        elif tok.type in (
            'PARENTESIS_IZQ',
            'PARENTESIS_DER'
        ):

            mi_tag = "parentesis"

        else:

            mi_tag = "normal"

        # Tipo
        tokens_text.insert(
            "end",
            f"{tok.type:<19}"
        )

        # Lexema
        tokens_text.insert(
            "end",
            f"{str(tok.value):<19}",
            mi_tag
        )

        # Línea
        tokens_text.insert(
            "end",
            f"{tok.lineno}\n"
        )

#------------------------------------------------------ARBOL SINTACTICO (PARSER)--------------------------------------------------

# Nodo AST
class Node:
    def __init__(self, label, children=None):
        self.label = label
        self.children = children or []

def make_leaf(label):
    return Node(label, [])

# Precedencia de expresiones
precedence = (
    ('nonassoc', 'IFX'),
    ('nonassoc', 'ELSE'),

    ('left', 'SUMA', 'RESTA'),
    ('left', 'MULTIPLICACION', 'DIVISION'),
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

    p[0] = Node(
        "DECL",
        [p[1], make_leaf(f"ID:{p[2]}")]
    )

def p_stmt_decl_assign(p):
    "stmt : type ID ASIGNACION expr PUNTOCOMA"

    p[0] = Node(
        "DECL_ASIGN",
        [p[1], make_leaf(f"ID:{p[2]}"), p[4]]
    )

def p_stmt_assign(p):
    "stmt : ID ASIGNACION expr PUNTOCOMA"

    p[0] = Node(
        "ASIGN",
        [make_leaf(f"ID:{p[1]}"), p[3]]
    )

def p_stmt_print_multi(p):
    '''
    stmt : PRINT PARENTESIS_IZQ args_opt PARENTESIS_DER PUNTOCOMA
    '''

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
    '''
    stmt : IF PARENTESIS_IZQ condition PARENTESIS_DER block %prec IFX
    '''

    p[0] = Node("IF", [p[3], p[5]])

def p_stmt_if_with_else(p):
    '''
    stmt : IF PARENTESIS_IZQ condition PARENTESIS_DER block ELSE block
    '''

    p[0] = Node(
        "IF",
        [p[3], p[5], Node("ELSE", [p[7]])]
    )

def p_stmt_while(p):
    '''
    stmt : WHILE PARENTESIS_IZQ condition PARENTESIS_DER block
    '''

    p[0] = Node(
        "WHILE",
        [p[3], p[5]]
    )

# Tipos
def p_type_int(p):
    "type : INT"
    p[0] = Node("TIPO:int")

def p_type_float(p):
    "type : FLOAT"
    p[0] = Node("TIPO:float")

# Se usa parentesis como bloque para agrupar ( ... )
def p_block(p):
    '''
    block : PARENTESIS_IZQ stmts_opt PARENTESIS_DER
    '''

    p[0] = Node("BLOQUE", p[2])

# Condiciones
def p_condition(p):
    "condition : expr COMPARACION expr"

    nodo = Node("CONDICION", [p[1], p[3]])

    nodo.op_relacional = p[2]

    p[0] = nodo

# Expresiones con operadores
def p_expr_binop(p):
    '''
    expr : expr SUMA expr
         | expr RESTA expr
         | expr MULTIPLICACION expr
         | expr DIVISION expr
    '''

    p[0] = Node(
        p[2],
        [p[1], p[3]]
    )

def p_expr_group(p):
    '''
    expr : PARENTESIS_IZQ expr PARENTESIS_DER
    '''

    p[0] = p[2]

def p_expr_id(p):
    "expr : ID"
    p[0] = Node(f"ID:{p[1]}")

def p_expr_num(p):
    "expr : NUMERO"
    p[0] = Node(f"NUM:{p[1]}")

def p_expr_desc(p):
    '''
    expr : CADENA
    '''

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

parser = yacc.yacc(
    start="program",
    debug=True,
    write_tables=False
)

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
    #print(codigo)

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
        font=("Courier New", 11),
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


#----------------------------------------------ANALIZADOR SEMANTICO----------------------------------------------------

def mostrar_semantico():
    ocupar_ram()
    codigo = ram

    limpiar_contenido()

    titulo = tk.Label(
        content_frame,
        text="Árbol Semántico",
         font=("Segoe UI", 23, "bold"),
        fg="#2c3e50"
    )
    titulo.pack(pady=10)

    try:
        ast = parser.parse(codigo, lexer=lexer)

        analyzer = SemanticAnalyzer()
        semantic_tree = analyzer.analyze(ast)

        frame = tk.Frame(content_frame)
        frame.pack(fill="both", expand=True)

        canvas = tk.Canvas(frame, bg="white")
        canvas.pack(fill="both", expand=True)

        #mover con barra
        vbar = tk.Scrollbar(frame, orient='vertical', command=canvas.yview)
        hbar = tk.Scrollbar(frame, orient='horizontal', command=canvas.xview)
        canvas.configure(yscrollcommand=vbar.set, xscrollcommand=hbar.set)
        canvas.grid(row=0, column=0, sticky='nsew')
        vbar.grid(row=0, column=1, sticky='ns')
        hbar.grid(row=1, column=0, sticky='ew')
        frame.grid_rowconfigure(0, weight=1)
        frame.grid_columnconfigure(0, weight=1)

        tree_dict = semantic_to_dict(semantic_tree)
        dibujar_arbol(canvas, tree_dict)

        canvas.config(scrollregion=canvas.bbox("all"))

    except SemanticError as e:
        messagebox.showerror("Error Semántico", str(e))
    except Exception as e:
        messagebox.showerror("Error", str(e))

class SemanticError(Exception):
    pass


class SymbolTable:
    def __init__(self):
        self.scopes = [{}]

    def push_scope(self):
        self.scopes.append({})

    def pop_scope(self):
        self.scopes.pop()

    def declare(self, name, tipo):
        if name in self.scopes[-1]:
            raise SemanticError(f"Variable '{name}' ya declarada en este ámbito")
        self.scopes[-1][name] = tipo

    def assign(self, name, tipo):
        for scope in reversed(self.scopes):
            if name in scope:
                if scope[name] != tipo:
                    raise SemanticError(
                        f"Asignación incompatible en '{name}' (esperado {scope[name]}, recibido {tipo})"
                    )
                return
        raise SemanticError(f"Variable '{name}' usada sin ser declarada")

    def lookup(self, name):
        for scope in reversed(self.scopes):
            if name in scope:
                return scope[name]
        raise SemanticError(f"Variable '{name}' usada sin ser declarada")

class SemanticNode: #nodo
    def __init__(self, label, tipo=None, children=None):  #constructor para cada nodo
        self.label = label
        self.tipo = tipo
        self.children = children or []


class SemanticAnalyzer:
    def __init__(self): #constructor para el analizador, utiliza una tabla de simbolos
        self.table = SymbolTable()

    def analyze(self, node):
        return self.visit(node)

    def visit(self, node):
        label = node.label

        #IDs especiales
        if label.startswith("ID"):
            return self.visit_ID(node)
        if label.startswith("NUM"):
            return self.visit_NUM(node)
        if label.startswith("DESC"):
            return self.visit_DESC(node)

        #operadores
        if label in ["+", "-", "*", "/"]:
            return self.visit_(node)

        method_name = f"visit_{label}"
        method = getattr(self, method_name, self.generic_visit)
        return method(node)

    def generic_visit(self, node):
        children = [self.visit(c) for c in node.children]
        return SemanticNode(node.label, children=children)

    # ---------------- DECLARACIONES ----------------

    def visit_DECL(self, node):
        tipo = node.children[0].label.split(":")[1]
        var = node.children[1].label.split(":")[1]

        self.table.declare(var, tipo)

        return SemanticNode(f"DECL {var}", tipo)

    def visit_DECL_ASIGN(self, node):
        tipo = node.children[0].label.split(":")[1]
        var = node.children[1].label.split(":")[1]

        expr = self.visit(node.children[2])

        if tipo != expr.tipo:
            raise SemanticError(
                f"Asignación incompatible en '{var}' ({tipo} != {expr.tipo})"
            )

        self.table.declare(var, tipo)

        return SemanticNode(f"DECL_ASIGN {var}", tipo, [expr])

    # ---------------- ASIGNACION ----------------

    def visit_ASIGN(self, node):
        var = node.children[0].label.split(":")[1]
        expr = self.visit(node.children[1])

        self.table.assign(var, expr.tipo)

        return SemanticNode(f"ASIGN {var}", expr.tipo, [expr])

    # ---------------- EXPRESIONES ----------------

    def visit_ID(self, node):
        var = node.label.split(":")[1]
        tipo = self.table.lookup(var)
        return SemanticNode(node.label, tipo)

    def visit_NUM(self, node):
        val = node.label.split(":")[1]
        tipo = "float" if "." in val else "int"
        return SemanticNode(node.label, tipo)

    def visit_DESC(self, node):
        return SemanticNode(node.label, "string")

    def visit_(self, node):
        left = self.visit(node.children[0])
        right = self.visit(node.children[1])

        if left.tipo != right.tipo:
            raise SemanticError("Operación con tipos incompatibles")

        return SemanticNode(node.label, left.tipo, [left, right])

    # ---------------- CONTROL ----------------

    def visit_IF(self, node): #PARA LOS IF
        cond = self.visit(node.children[0])

        self.table.push_scope()
        then_block = self.visit(node.children[1])
        self.table.pop_scope()

        children = [cond, then_block]

        if len(node.children) == 3:
            self.table.push_scope()
            else_block = self.visit(node.children[2].children[0])
            self.table.pop_scope()
            children.append(else_block)

        return SemanticNode("IF", children=children)

    def visit_WHILE(self, node): #PARA LOS WHILE
        cond = self.visit(node.children[0])

        self.table.push_scope()
        block = self.visit(node.children[1])
        self.table.pop_scope()

        return SemanticNode("WHILE", children=[cond, block])

    def visit_BLOQUE(self, node): 
        children = [self.visit(c) for c in node.children]
        return SemanticNode("BLOQUE", children=children)

    def visit_PRINT(self, node): #PARA PRINT
        args = [self.visit(arg) for arg in node.children]
        return SemanticNode("PRINT", children=args)


# ---------------- CONVERSION A DICCIONARIO ----------------

def semantic_to_dict(node):
    return {
        "label": f"{node.label} ({node.tipo})" if node.tipo else node.label,
        "children": [semantic_to_dict(c) for c in node.children]
    }


#---------------------------------------------- GENERADOR DE CODIGO DE 3 DIRECCIONES -----------------------------------

class TACGenerator:
    def __init__(self):
        self.temp_count = 0
        self.label_count = 0
        self.code = []

    # ======================
    # UTILIDADES
    # ======================

    def new_temp(self):
        self.temp_count += 1
        return f"t{self.temp_count}"

    def new_label(self):
        self.label_count += 1
        return f"L{self.label_count}"

    def clean_leaf(self, label):
        """
        Convierte:
        ID:x        -> x
        NUM:5       -> 5
        STR:hola    -> "hola"
        DESC:hola   -> "hola"
        """

        if ":" in label:
            tipo, valor = label.split(":", 1)

            # cadenas
            if tipo in ["STR", "DESC"]:
                return valor

            return valor

        return label

    # ======================
    # GENERADOR PRINCIPAL
    # ======================

    def generate(self, node):

        if node is None:
            return None

        # ----------------------
        # PROGRAMA
        # ----------------------
        if node.label == "PROGRAMA":

            for stmt in node.children:
                self.generate(stmt)

        # ----------------------
        # DECLARACIÓN
        # ----------------------
        elif node.label == "DECL":
            pass

        # ----------------------
        # DECLARACIÓN CON ASIGNACIÓN
        # ----------------------
        elif node.label == "DECL_ASIGN":

            var = self.clean_leaf(node.children[1].label)
            val = self.generate(node.children[2])

            self.code.append(f"{var} = {val}")

        # ----------------------
        # ASIGNACIÓN
        # ----------------------
        elif node.label == "ASIGN":

            var = self.clean_leaf(node.children[0].label)
            val = self.generate(node.children[1])

            self.code.append(f"{var} = {val}")

        # ----------------------
        # PRINT
        # ----------------------
        elif node.label == "PRINT":

            for expr in node.children:

                val = self.generate(expr)

                if val is not None:
                    self.code.append(f"print {val}")

        # ----------------------
        # BLOQUE
        # ----------------------
        elif node.label == "BLOQUE":

            for stmt in node.children:
                self.generate(stmt)

        # ----------------------
        # IF
        # ----------------------
        elif node.label == "IF":

            cond = self.generate(node.children[0])

            label_true = self.new_label()
            label_end = self.new_label()

            self.code.append(f"if {cond} goto {label_true}")

            # ELSE
            if len(node.children) == 3:

                else_block = node.children[2].children[0]

                self.generate(else_block)

                self.code.append(f"goto {label_end}")

            self.code.append(f"{label_true}:")

            self.generate(node.children[1])

            self.code.append(f"{label_end}:")

        # ----------------------
        # WHILE
        # ----------------------
        elif node.label == "WHILE":
            start_label = self.new_label() # L1
            end_label = f"END_{start_label}" # END_L1

            self.code.append(f"{start_label}:")

            # Generamos la condición (ej: t6 = contador < 5)
            cond = self.generate(node.children[0])

            # Si la condición es FALSA (0), saltamos al final
            # (En TAC avanzado se suele usar 'ifFalse', pero con 'if' basta)
            self.code.append(f"if {cond} == 0 goto {end_label}")

            # Cuerpo del bucle
            self.generate(node.children[1])

            # Volver al inicio para re-evaluar
            self.code.append(f"goto {start_label}")
            self.code.append(f"{end_label}:")

        # ----------------------
        # CONDICIÓN
        # ----------------------
        elif node.label == "CONDICION":

            left = self.generate(node.children[0])
            right = self.generate(node.children[1])

            op = node.op_relacional

            temp = self.new_temp()

            self.code.append(f"{temp} = {left} {op} {right}")

            return temp
        # ----------------------
        # OPERACIONES
        # ----------------------
        elif node.label in ['+', '-', '*', '/']:

            left = self.generate(node.children[0])
            right = self.generate(node.children[1])

            temp = self.new_temp()

            self.code.append(f"{temp} = {left} {node.label} {right}")

            return temp

        # ----------------------
        # HOJAS
        # ----------------------
        elif (
            node.label.startswith("ID:") or
            node.label.startswith("NUM:") or
            node.label.startswith("STR:") or
            node.label.startswith("DESC:")
        ):

            return self.clean_leaf(node.label)

        # ----------------------
        # CASO GENERAL
        # ----------------------
        else:

            print("Nodo no reconocido:", node.label)

            for child in node.children:

                result = self.generate(child)

                if result is not None:
                    return result
    
def mostrar_tresdir():
    ocupar_ram()
    #Obtener código del editor
    codigo = ram
    #print(codigo)

    limpiar_contenido()

    titulo = tk.Label(
        content_frame,
        text="Código de Tres Direcciones",
        font=("Segoe UI", 23, "bold"),
        fg="#2c3e50"
    )
    titulo.pack(pady=10)

    # ============================
    # FRAME PRINCIPAL
    # ============================
    tresdir_frame = tk.Frame(content_frame)
    tresdir_frame.pack(fill="both", expand=True, padx=10, pady=10)

    # ============================
    # GENERAR TAC
    # ============================
    ast3 = parser.parse(codigo, lexer=lexer)

    gen = TACGenerator()
    gen.generate(ast3)

    # ============================
    # FRAME PARA NUMEROS + TEXTO
    # ============================
    editor_frame = tk.Frame(tresdir_frame)
    editor_frame.pack(fill="both", expand=True)

    # ----------------------------
    # NUMERACIÓN DE LÍNEAS
    # ----------------------------
    line_numbers = tk.Text(
        editor_frame,
        width=4,
        padx=5,
        takefocus=0,
        border=0,
        background="#2b2b2b",
        foreground="#aaaaaa",
        state="disabled",
        font=("Consolas", 11)
    )
    line_numbers.pack(side="left", fill="y")

    # ----------------------------
    # TEXT PRINCIPAL
    # ----------------------------
    text_tac = tk.Text(
        editor_frame,
        wrap="none",
        font=("Consolas", 11),
        bg="#1e1e1e",
        fg="#dcdcdc",
        insertbackground="white"
    )
    text_tac.pack(side="left", fill="both", expand=True)

    # ----------------------------
    # SCROLLBARS
    # ----------------------------
    scroll_y = tk.Scrollbar(editor_frame, orient="vertical")
    scroll_y.pack(side="right", fill="y")

    scroll_x = tk.Scrollbar(tresdir_frame, orient="horizontal")
    scroll_x.pack(side="bottom", fill="x")

    # Configurar scroll conjunto
    text_tac.config(yscrollcommand=scroll_y.set, xscrollcommand=scroll_x.set)
    scroll_y.config(command=lambda *args: sync_scroll(*args))
    scroll_x.config(command=text_tac.xview)

    # ============================
    # SINCRONIZAR SCROLL
    # ============================
    def sync_scroll(*args):
        text_tac.yview(*args)
        line_numbers.yview(*args)

    # ============================
    # INSERTAR TAC
    # ============================
    for i, line in enumerate(gen.code, start=1):
        text_tac.insert("end", line + "\n")
        line_numbers.config(state="normal")
        line_numbers.insert("end", f"{i}\n")
        line_numbers.config(state="disabled")

    # Bloquear edición
    text_tac.config(state="disabled")

    # ============================
    # BOTÓN COPIAR
    # ============================
    def copiar_tac():
        contenido = "\n".join(gen.code)
        content_frame.clipboard_clear()
        content_frame.clipboard_append(contenido)
        content_frame.update()  # necesario en algunos sistemas

    btn_copiar = tk.Button(
        content_frame,
        text="Copiar CTD",
        font=("Segoe UI", 11, "bold"),
        bg="#314F86",
        fg="white",
        padx=10,
        pady=5,
        command=copiar_tac
    )
    btn_copiar.pack(pady=5)





#---------------------------------------------- OPTIMIZAR CODIGO MEDIO------------------------------------------


class TACOptimizer:

    def __init__(self, code):
        self.code = code

    # ============================================
    # UTILIDADES
    # ============================================

    def is_number(self, value):
        try:
            int(value)
            return True
        except:
            return False

    # ============================================
    # CONSTANT FOLDING
    # t1 = 2 + 3  ->  t1 = 5
    # ============================================

    def constant_folding(self):

        optimized = []

        for line in self.code:

            if "=" not in line or line.startswith("if"):
                optimized.append(line)
                continue

            left, right = line.split("=", 1)

            left = left.strip()
            right = right.strip()

            parts = right.split()

            if len(parts) == 3:

                a, op, b = parts

                if self.is_number(a) and self.is_number(b):

                    a = int(a)
                    b = int(b)

                    result = None

                    if op == "+":
                        result = a + b

                    elif op == "-":
                        result = a - b

                    elif op == "*":
                        result = a * b

                    elif op == "/":
                        if b != 0:
                            result = a // b

                    elif op == ">":
                        result = int(a > b)

                    elif op == "<":
                        result = int(a < b)

                    elif op == "==":
                        result = int(a == b)

                    if result is not None:
                        optimized.append(f"{left} = {result}")
                        continue

            optimized.append(line)

        self.code = optimized

    # ============================================
    # CONSTANT PROPAGATION
    # a = 5
    # t1 = a + 2
    # -> t1 = 5 + 2
    # ============================================
    """
    def constant_propagation(self):

        constants = {}
        optimized = []

        for line in self.code:

            if "=" not in line or line.startswith("if"):
                optimized.append(line)
                continue

            left, right = line.split("=", 1)

            left = left.strip()
            right = right.strip()

            # reemplazar constantes
            parts = right.split()

            new_parts = []

            for p in parts:

                if p in constants:
                    new_parts.append(constants[p])
                else:
                    new_parts.append(p)

            right = " ".join(new_parts)

            # guardar constantes
            if self.is_number(right):
                constants[left] = right

            else:
                if left in constants:
                    del constants[left]

            optimized.append(f"{left} = {right}")

        self.code = optimized
    """
    # ============================================
    # ALGEBRAIC SIMPLIFICATION
    # x = a + 0 -> x = a
    # ============================================

    def algebraic_simplification(self):

        optimized = []

        for line in self.code:
            
            
            if (
                line.endswith(":")
                or line.startswith("goto")
                or line.startswith("if")
            ):
                optimized.append(line)
                continue

            if "=" not in line or line.startswith("if"):
                optimized.append(line)
                continue

            left, right = line.split("=", 1)

            left = left.strip()
            right = right.strip()

            parts = right.split()

            if len(parts) == 3:

                a, op, b = parts

                # a + 0
                if op == "+" and b == "0":
                    optimized.append(f"{left} = {a}")
                    continue

                if op == "+" and a == "0":
                    optimized.append(f"{left} = {b}")
                    continue

                # a - 0
                if op == "-" and b == "0":
                    optimized.append(f"{left} = {a}")
                    continue

                # a * 1
                if op == "*" and b == "1":
                    optimized.append(f"{left} = {a}")
                    continue

                if op == "*" and a == "1":
                    optimized.append(f"{left} = {b}")
                    continue

                # a * 0
                if op == "*" and (a == "0" or b == "0"):
                    optimized.append(f"{left} = 0")
                    continue

                # a / 1
                if op == "/" and b == "1":
                    optimized.append(f"{left} = {a}")
                    continue

            optimized.append(line)

        self.code = optimized

    # ============================================
    # COPY PROPAGATION
    # t1 = a
    # x = t1
    # -> x = a
    # ============================================

    def copy_propagation(self):

        copies = {}
        optimized = []

        for line in self.code:

            line = line.strip()

            # ====================================
            # RESET EN FLUJO DE CONTROL
            # ====================================

            if (
                line.endswith(":")
                or line.startswith("goto")
                or line.startswith("if")
            ):

                copies.clear()

                optimized.append(line)

                continue

            # ====================================
            # LÍNEAS SIN ASIGNACIÓN
            # ====================================

            if "=" not in line:

                optimized.append(line)

                continue

            # ====================================
            # ASIGNACIÓN
            # ====================================

            left, right = line.split("=", 1)

            left = left.strip()
            right = right.strip()

            # ====================================
            # REEMPLAZAR COPIAS DIRECTAS
            # ====================================

            if right in copies:
                right = copies[right]

            parts = right.split()

            new_parts = []

            for p in parts:

                if p in copies:
                    new_parts.append(copies[p])
                else:
                    new_parts.append(p)

            right = " ".join(new_parts)

            # ====================================
            # GUARDAR COPIA SIMPLE
            # x = y
            # ====================================

            if (
                len(parts) == 1
                and not self.is_number(right)
            ):
                copies[left] = right

            # ====================================
            # SI SE REDEFINE VARIABLE
            # INVALIDAR COPIA
            # ====================================

            elif left in copies:

                del copies[left]

            optimized.append(f"{left} = {right}")

        self.code = optimized

    # ============================================
    # DEAD CODE ELIMINATION
    # elimina temporales nunca usados
    # ============================================

    def dead_code_elimination(self):

        used = set()

        # ====================================
        # BUSCAR TEMPORALES USADOS
        # ====================================

        for line in self.code:

            if "=" in line and not line.startswith("if"):

                left, right = line.split("=", 1)

                parts = right.split()

                for p in parts:

                    if p.startswith("t"):
                        used.add(p)

            else:

                parts = (
                    line
                    .replace("==", " == ")
                    .replace("!=", " != ")
                    .split()
                )

                for p in parts:

                    if p.startswith("t"):
                        used.add(p)

        # ====================================
        # ELIMINAR TEMPORALES NO USADOS
        # ====================================

        optimized = []

        for line in self.code:

            if "=" in line and not line.startswith("if"):

                left = line.split("=")[0].strip()

                # eliminar temporal no usado
                if left.startswith("t") and left not in used:
                    continue

            optimized.append(line)

        self.code = optimized
    # ============================================
    # REMOVE REDUNDANT GOTOS
    # goto L1
    # L1:
    # ============================================

    def remove_redundant_gotos(self):

        optimized = []

        i = 0

        while i < len(self.code):

            line = self.code[i]

            if line.startswith("goto"):

                label = line.split()[1]

                if i + 1 < len(self.code):

                    next_line = self.code[i + 1]

                    if next_line == f"{label}:":
                        i += 1
                        continue

            optimized.append(line)

            i += 1

        self.code = optimized

    # ============================================
    # REMOVE DUPLICATE LABELS
    # ============================================

    def remove_duplicate_labels(self):

        optimized = []
        previous = None

        for line in self.code:

            if line.endswith(":") and previous == line:
                continue

            optimized.append(line)
            previous = line

        self.code = optimized

    # ============================================
    # OPTIMIZE ALL
    # ============================================

    def optimize(self):

        changed = True

        while changed:

            old_code = self.code.copy()

            #self.constant_propagation()

            self.constant_folding()

            self.algebraic_simplification()

            self.copy_propagation()

            self.dead_code_elimination()

            self.remove_redundant_gotos()

            self.remove_duplicate_labels()

            changed = old_code != self.code

        return self.code

def mostrar_tacoptimizer():

    ocupar_ram()

    # ============================================
    # OBTENER CÓDIGO
    # ============================================

    codigo = ram

    limpiar_contenido()

    titulo = tk.Label(
        content_frame,
        text="Código de Tres Direcciones Optimizado",
        font=("Segoe UI", 23, "bold"),
        fg="#2c3e50"
    )
    titulo.pack(pady=10)

    # ============================================
    # FRAME PRINCIPAL
    # ============================================

    tresdir_frame = tk.Frame(content_frame)
    tresdir_frame.pack(fill="both", expand=True, padx=10, pady=10)

    # ============================================
    # GENERAR TAC
    # ============================================

    ast3 = parser.parse(codigo, lexer=lexer)

    gen = TACGenerator()
    gen.generate(ast3)

    # ============================================
    # OPTIMIZAR TAC
    # ============================================

    optimizer = TACOptimizer(gen.code)

    optimized_code = optimizer.optimize()

    # ============================================
    # FRAME EDITOR
    # ============================================

    editor_frame = tk.Frame(tresdir_frame)
    editor_frame.pack(fill="both", expand=True)

    # ============================================
    # NUMERACIÓN
    # ============================================

    line_numbers = tk.Text(
        editor_frame,
        width=5,
        padx=5,
        takefocus=0,
        border=0,
        background="#2b2b2b",
        foreground="#aaaaaa",
        state="disabled",
        font=("Consolas", 11)
    )

    line_numbers.pack(side="left", fill="y")

    # ============================================
    # TEXTO TAC
    # ============================================

    text_tac = tk.Text(
        editor_frame,
        wrap="none",
        font=("Consolas", 11),
        bg="#1e1e1e",
        fg="#dcdcdc",
        insertbackground="white"
    )

    text_tac.pack(side="left", fill="both", expand=True)

    # ============================================
    # SCROLLBARS
    # ============================================

    scroll_y = tk.Scrollbar(editor_frame, orient="vertical")
    scroll_y.pack(side="right", fill="y")

    scroll_x = tk.Scrollbar(tresdir_frame, orient="horizontal")
    scroll_x.pack(side="bottom", fill="x")

    # ============================================
    # CONFIGURAR SCROLL
    # ============================================

    text_tac.config(
        yscrollcommand=scroll_y.set,
        xscrollcommand=scroll_x.set
    )

    scroll_y.config(command=lambda *args: sync_scroll(*args))
    scroll_x.config(command=text_tac.xview)

    # ============================================
    # SINCRONIZAR SCROLL
    # ============================================

    def sync_scroll(*args):
        text_tac.yview(*args)
        line_numbers.yview(*args)

    # ============================================
    # INSERTAR TAC OPTIMIZADO
    # ============================================

    line_numbers.config(state="normal")

    for i, line in enumerate(optimized_code, start=1):

        text_tac.insert("end", line + "\n")

        line_numbers.insert("end", f"{i}\n")

    line_numbers.config(state="disabled")

    # ============================================
    # BLOQUEAR EDICIÓN
    # ============================================

    text_tac.config(state="disabled")

    # ============================================
    # COPIAR TAC
    # ============================================

    def copiar_tac():

        contenido = "\n".join(optimized_code)

        content_frame.clipboard_clear()

        content_frame.clipboard_append(contenido)

        content_frame.update()

    # ============================================
    # BOTÓN COPIAR
    # ============================================

    btn_copiar = tk.Button(
        content_frame,
        text="Copiar TAC Optimizado",
        font=("Segoe UI", 11, "bold"),
        bg="#314F86",
        fg="white",
        padx=10,
        pady=5,
        command=copiar_tac
    )

    btn_copiar.pack(pady=5)

#----------------------------------------------TRADUCTOR TAC A NASM----------------------------------------------

class NASMGenerator:

    def __init__(self, tac_code):

        self.tac = tac_code
        self.asm = []

        self.variables = set()

        # NUEVO
        self.strings = {}
        self.string_count = 0

    # ============================================
    # DETECTAR VARIABLES
    # ============================================

    def collect_variables(self):
        for line in self.tac:
            parts = line.replace(",", " ").split()
            for p in parts:
                if p.startswith('"') and p.endswith('"'):
                    continue

                if (
                    p.isidentifier()
                    # Ignoramos etiquetas estándar (L1, L2...) 
                    and not p.startswith("L") 
                    # Ignoramos etiquetas de cierre de bucles (END_L1...)
                    and not p.startswith("END_")
                    # Ignoramos etiquetas de comparación (TRUE_t1, END_t1...)
                    and not p.startswith("TRUE_")
                    and p not in ["if", "goto", "print", "None"]
                ):
                    self.variables.add(p)
    # ============================================
    # VERIFICAR ENTERO
    # ============================================

    def is_number(self, value):

        try:
            int(value)
            return True
        except:
            return False

    # ============================================
    # VERIFICAR FLOAT
    # ============================================

    def is_float(self, value):

        try:
            float(value)
            return "." in value
        except:
            return False

    # ============================================
    # VERIFICAR STRING
    # ============================================

    def is_string(self, value):

        return (
            value.startswith('"')
            and value.endswith('"')
        )

    # ============================================
    # OBTENER LABEL STRING
    # ============================================

    def get_string_label(self, text):

        if text not in self.strings:

            label = f"str_{self.string_count}"

            self.strings[text] = label

            self.string_count += 1

        return self.strings[text]

    # ============================================
    # OBTENER OPERANDO
    # ============================================

    def operand(self, op):

        if self.is_number(op):
            return op

        if self.is_float(op):

            raise Exception(
                f"Float no soportado todavía: {op}"
            )

        return f"[{op}]"

    # ============================================
    # GENERAR ASM
    # ============================================

    def generate(self):

        self.collect_variables()

        # ====================================
        # DETECTAR STRINGS
        # ====================================

        for line in self.tac:

            if line.startswith("print"):

                value = line[len("print"):].strip()

                if self.is_string(value):

                    self.get_string_label(value)

        # ====================================
        # DATA
        # ====================================

        self.asm.append("section .data")

        for var in self.variables:
            self.asm.append(f"{var} dd 0")

        # FORMATOS
        self.asm.append('fmt_int db "%d",10,0')
        self.asm.append('fmt_str db "%s",10,0')

        # STRINGS
        for text, label in self.strings.items():

            clean = text[1:-1]

            self.asm.append(
                f'{label} db "{clean}",0'
            )

        # ====================================
        # TEXT
        # ====================================

        self.asm.append("section .text")
        self.asm.append("global _main")
        self.asm.append("extern _printf")
        self.asm.append("_main:")

        # ====================================
        # TRADUCIR TAC
        # ====================================

        for line in self.tac:
            self.translate(line)

        # ====================================
        # RETURN
        # ====================================

        self.asm.append("mov eax, 0")
        self.asm.append("ret")

        return self.asm

    # ============================================
    # TRADUCTOR
    # ============================================

    def translate(self, line):

        line = line.strip()

        if not line:
            return

        # ====================================
        # LABEL
        # ====================================

        if line.endswith(":"):

            self.asm.append(line)

            return

        # ====================================
        # GOTO
        # ====================================

        if line.startswith("goto"):

            label = line.split()[1]

            self.asm.append(f"jmp {label}")

            return

        # ====================================
        # IF (en el método translate)
        # ====================================
        if line.startswith("if"):
            parts = line.split()

            # if t1 goto L1
            if len(parts) == 4:

                condition = parts[1]
                label = parts[3]

                self.asm.append(f"mov eax, [{condition}]")
                self.asm.append("cmp eax, 1")
                self.asm.append(f"je {label}")

                return

            # if t1 == 0 goto L1
            elif len(parts) == 6:

                condition = parts[1]
                op = parts[2]
                value = parts[3]
                label = parts[5]

                self.asm.append(f"mov eax, [{condition}]")
                self.asm.append(f"cmp eax, {value}")

                if op == "==":
                    self.asm.append(f"je {label}")

                elif op == "!=":
                    self.asm.append(f"jne {label}")

                return

            else:
                raise Exception(f"IF TAC inválido: {line}")

        # ====================================
        # PRINT
        # ====================================

        if line.startswith("print"):

            value = line[len("print"):].strip()

            # STRING
            if self.is_string(value):

                label = self.get_string_label(value)

                self.asm.append(
                    f"push dword {label}"
                )

                self.asm.append(
                    "push fmt_str"
                )

                self.asm.append(
                    "call _printf"
                )

                self.asm.append(
                    "add esp, 8"
                )

                return

            # ENTERO
            if self.is_number(value):

                self.asm.append(
                    f"push dword {value}"
                )

            # VARIABLE
            else:

                self.asm.append(
                    f"push dword [{value}]"
                )

            self.asm.append("push fmt_int")
            self.asm.append("call _printf")
            self.asm.append("add esp, 8")

            return
        
        

        # ====================================
        # ASIGNACIONES
        # ====================================

        if "=" in line and not line.startswith("if"):

            left, right = line.split("=", 1)

            left = left.strip()
            right = right.strip()

            parts = right.split()

            # ================================
            # SIMPLE
            # ================================

            if len(parts) == 1:

                value = parts[0]

                if self.is_number(value):

                    self.asm.append(
                        f"mov dword [{left}], {value}"
                    )

                else:

                    self.asm.append(
                        f"mov eax, [{value}]"
                    )

                    self.asm.append(
                        f"mov [{left}], eax"
                    )

                return

            # ================================
            # OPERACIONES
            # ================================

            if len(parts) == 3:

                a, op, b = parts

                # COMPARACIONES
                if op in [">", "<", "=="]:

                    self.asm.append(
                        f"mov eax, {self.operand(a)}"
                    )

                    self.asm.append(
                        f"cmp eax, {self.operand(b)}"
                    )

                    true_label = f"TRUE_{left}"
                    end_label = f"END_{left}"

                    if op == ">":
                        self.asm.append(f"jg {true_label}")

                    elif op == "<":
                        self.asm.append(f"jl {true_label}")

                    elif op == "==":
                        self.asm.append(f"je {true_label}")

                    self.asm.append(
                        f"mov dword [{left}], 0"
                    )

                    self.asm.append(
                        f"jmp {end_label}"
                    )

                    self.asm.append(f"{true_label}:")

                    self.asm.append(
                        f"mov dword [{left}], 1"
                    )

                    self.asm.append(f"{end_label}:")

                    return

                # ARITMÉTICA

                self.asm.append(
                    f"mov eax, {self.operand(a)}"
                )

                if op == "+":
                    self.asm.append(
                        f"add eax, {self.operand(b)}"
                    )

                elif op == "-":
                    self.asm.append(
                        f"sub eax, {self.operand(b)}"
                    )

                elif op == "*":
                    self.asm.append(
                        f"imul eax, {self.operand(b)}"
                    )

                elif op == "/":

                    self.asm.append("cdq")

                    if self.is_number(b):

                        self.asm.append(
                            f"mov ebx, {b}"
                        )

                        self.asm.append(
                            "idiv ebx"
                        )

                    else:

                        self.asm.append(
                            f"idiv dword [{b}]"
                        )

                self.asm.append(
                    f"mov [{left}], eax"
                )

def mostrar_codigo_maquina():

    ocupar_ram()

    # ============================================
    # OBTENER CÓDIGO FUENTE
    # ============================================

    codigo = ram

    limpiar_contenido()

    titulo = tk.Label(
        content_frame,
        text="Código Máquina / NASM",
        font=("Segoe UI", 23, "bold"),
        fg="#2c3e50"
    )

    titulo.pack(pady=10)

    # ============================================
    # FRAME PRINCIPAL
    # ============================================

    maquina_frame = tk.Frame(content_frame)
    maquina_frame.pack(
        fill="both",
        expand=True,
        padx=10,
        pady=10
    )

    # ============================================
    # PARSER
    # ============================================

    ast = parser.parse(codigo, lexer=lexer)

    # ============================================
    # GENERAR TAC
    # ============================================

    tac = TACGenerator()

    tac.generate(ast)

    # ============================================
    # OPTIMIZAR TAC
    # ============================================

    optimizer = TACOptimizer(tac.code)

    optimized_code = optimizer.optimize()

    # ============================================
    # GENERAR NASM
    # ============================================

    nasm = NASMGenerator(optimized_code)

    asm_code = nasm.generate()

    # CONVERTIR LISTA -> STRING
    asm_code = "\n".join(asm_code)

    # ============================================
    # FRAME EDITOR
    # ============================================

    editor_frame = tk.Frame(maquina_frame)

    editor_frame.pack(
        fill="both",
        expand=True
    )

    # ============================================
    # NUMERACIÓN
    # ============================================

    line_numbers = tk.Text(
        editor_frame,
        width=5,
        padx=5,
        takefocus=0,
        border=0,
        background="#2b2b2b",
        foreground="#aaaaaa",
        state="disabled",
        font=("Consolas", 11)
    )

    line_numbers.pack(side="left", fill="y")

    # ============================================
    # TEXTO ASM
    # ============================================

    text_asm = tk.Text(
        editor_frame,
        wrap="none",
        font=("Consolas", 11),
        bg="#1e1e1e",
        fg="#dcdcdc",
        insertbackground="white"
    )

    text_asm.pack(
        side="left",
        fill="both",
        expand=True
    )

    # ============================================
    # SCROLLBARS
    # ============================================

    scroll_y = tk.Scrollbar(
        editor_frame,
        orient="vertical"
    )

    scroll_y.pack(side="right", fill="y")

    scroll_x = tk.Scrollbar(
        maquina_frame,
        orient="horizontal"
    )

    scroll_x.pack(side="bottom", fill="x")

    # ============================================
    # CONFIGURAR SCROLL
    # ============================================

    text_asm.config(
        yscrollcommand=scroll_y.set,
        xscrollcommand=scroll_x.set
    )

    scroll_y.config(
        command=lambda *args: sync_scroll(*args)
    )

    scroll_x.config(command=text_asm.xview)

    # ============================================
    # SINCRONIZAR SCROLL
    # ============================================

    def sync_scroll(*args):

        text_asm.yview(*args)

        line_numbers.yview(*args)

    # ============================================
    # INSERTAR ASM
    # ============================================

    line_numbers.config(state="normal")

    for i, line in enumerate(asm_code.splitlines(), start=1):

        text_asm.insert("end", line + "\n")

        line_numbers.insert("end", f"{i}\n")

    line_numbers.config(state="disabled")

    # ============================================
    # BLOQUEAR EDICIÓN
    # ============================================

    text_asm.config(state="disabled")

    # ============================================
    # COPIAR ASM
    # ============================================

    def copiar_asm():

        contenido = "\n".join(asm_code)

        content_frame.clipboard_clear()

        content_frame.clipboard_append(contenido)

        content_frame.update()


    #GUARDAR ASM ANTES DE BOTON

    def ventana_asm():
        global texto_emergente3
        global emergente3
        emergente3 = tk.Toplevel(root)
        emergente3.title("Guardar")
        emergente3.geometry("400x200")    

        titulo = tk.Label(emergente3, text="Ingrese nombre para guardar", font=("consolas",12)).pack(pady=20)
        texto_emergente3 = tk.Text(
            emergente3,
            font=("Consolas", 12),
            wrap="none",
            undo=True,
            width= 20,
            height=1
        )
        texto_emergente3.pack(pady=(20,2))
        
        btn_guardar = tk.Button(
            emergente3,
            text = "Guardar",
            command=guardar_asm,
            width= 20
        )
        btn_guardar.pack(pady=(25,10))

        #para guardar cuando se presione enter
        def presionar_enter(event):
            btn_guardar.invoke()

        texto_emergente3.bind("<Return>", presionar_enter) #leer en esta ventana si se presiona enter


    def guardar_asm():
        nombre_asm = texto_emergente3.get("1.0", "end-1c").strip()
        texto_emergente3.delete("1.0", "end")
        ruta = "ARCHIVOS_ASM/" + nombre_asm + ".asm"
        with open(ruta, "w", encoding="utf-8") as f:
            f.write(asm_code)
        emergente3.destroy()

        Mbox('exito', 'Se ha guardado el archivo .asm con exito', 0)
    # ============================================
    # BOTÓN COPIAR
    # ============================================

    btn_copiar = tk.Button(
        content_frame,
        text="Copiar ASM",
        font=("Segoe UI", 11, "bold"),
        bg="#314F86",
        fg="white",
        padx=10,
        pady=5,
        command=copiar_asm
    )

    btn_copiar.pack(pady=5)

    # ============================================
    # BOTÓN GUARDAR
    # ============================================

    btn_guardar = tk.Button(
        content_frame,
        text="Guardar ASM",
        font=("Segoe UI", 11, "bold"),
        bg="#1E8449",
        fg="white",
        padx=10,
        pady=5,
        command=ventana_asm
    )

    btn_guardar.pack(pady=5)

#----------------------------------------------GENERAR OBJ Y EXE----------------------------------------
def crear_exe():

    nombre = nombreexe.get("1.0", "end-1c").strip()

    nombre_asm = "ARCHIVOS_ASM/" + nombre + ".asm"
    nombre_obj = "ARCHIVOS_OBJ/" + nombre + ".obj"
    nombre_exe = "RESULTADO_EXE/" + nombre + ".exe"

    # ============================================
    # ASM -> OBJ
    # ============================================

    subprocess.run([
        "nasm",
        "-f",
        "win32",
        nombre_asm,
        "-o",
        nombre_obj
    ])

    # ============================================
    # OBJ -> EXE
    # ============================================

    subprocess.run([
        "gcc",
        nombre_obj,
        "-o",
        nombre_exe
       
    ])


def mostrar_obj_exe():
    ocupar_ram()

    limpiar_contenido()
    
    # Título
    titulo = tk.Label(
        content_frame,
        text="Generar OBJ y EXE",
        font=("Arial", 18, "bold"),
        bg="#ecf0f1"
    )
    titulo.pack(pady=10)
    
 

    nombrearch = tk.Label(
        content_frame,
        text="Ingrese nombre del archivo .asm",
        font=("Arial", 11),
        bg="#ecf0f1"
    )
    nombrearch.pack()

    #------------------------------------------------------

    global nombreexe
    nombreexe = tk.Text(
        content_frame,
        font=("Consolas", 12),
        wrap="none",
        undo=True,
        width= 20,
        height=1
    )
    nombreexe.pack()


    btn_crear = tk.Button(
        content_frame,
        text="Crear",
        command=crear_exe,
        width=20,
        pady=5 #espacio que sale del centro del boton hacia arriba y abajo
    )
    btn_crear.pack(pady=5) #pady con doble parentesis quiere decir (espacio desde arriba, espacio desde abajo)



#----------------------------------------------BOTONES Y TITULO EN BARRA-----------------------------------------------



label = tk.Label( #TITULO EN LA BARRA
    menu_frame, 
    text = "Compiladores\nProyecto Parte III",
    fg="white",
    bg=color_bg,
    font=("Arial", 14, "bold"),
    justify="center"
)
label.pack(pady=10)

#BOTONES DEL MENU
btn_editor = tk.Button(
    menu_frame,
    text="1. Editor de texto",
    command=mostrar_editor,
    width=20,
    pady=5 #espacio que sale del centro del boton hacia arriba y abajo
)
btn_editor.pack(pady=(20,10)) #pady con doble parentesis quiere decir (espacio desde arriba, espacio desde abajo)

btn_lexico = tk.Button(
    menu_frame,
    text="2. Análisis léxico",
    #no se ejecuta instantaneamente con () porque lambda solo se ejecuta al dar click
    command=lambda: mostrar_lexico() if nombre_archivo_var.get() != "Archivo actual: Ninguno" else no_hay_code(),
    width=20,
    pady=5
)
btn_lexico.pack(pady=10)

btn_sintactico = tk.Button(
    menu_frame,
    text="3. Árbol sintáctico",
    command=lambda: mostrar_arbol() if nombre_archivo_var.get() != "Archivo actual: Ninguno" else no_hay_code(),
    width=20,
    pady=5
)
btn_sintactico.pack(pady=10)

btn_tabla = tk.Button(
    menu_frame,
    text="4. Tabla de símbolos",
    command=lambda: mostrar_tabla() if nombre_archivo_var.get() != "Archivo actual: Ninguno" else no_hay_code(),
    width=20,
    pady=5
)
btn_tabla.pack(pady=10)

btn_semantico = tk.Button(
    menu_frame,
    text="5. Analizador semantico",
    command=lambda: mostrar_semantico() if nombre_archivo_var.get() != "Archivo actual: Ninguno" else no_hay_code(),
    width=20,
    pady=5
)
btn_semantico.pack(pady=10)

btn_tresdir = tk.Button(
    menu_frame,
    text="6. Código intermedio",
    command=lambda: mostrar_tresdir() if nombre_archivo_var.get() != "Archivo actual: Ninguno" else no_hay_code(),
    width=20,
    pady=5
)
btn_tresdir.pack(pady=10)

btn_optimizado = tk.Button(
    menu_frame,
    text="7. Código optimizado",
    command=lambda: mostrar_tacoptimizer() if nombre_archivo_var.get() != "Archivo actual: Ninguno" else no_hay_code(),
    width=20,
    pady=5
)
btn_optimizado.pack(pady=10)

btn_maquina = tk.Button(
    menu_frame,
    text="8. Código Máquina",
    command=lambda: mostrar_codigo_maquina() if nombre_archivo_var.get() != "Archivo actual: Ninguno" else no_hay_code(),
    width=20,
    pady=5
)
btn_maquina.pack(pady=10)

btn_exe = tk.Button(
    menu_frame,
    text="9. Generar EXE",
    command=lambda: mostrar_obj_exe()  if nombre_archivo_var.get() != "Archivo actual: Ninguno" else no_hay_code(),
    width=20,
    pady=5
)
btn_exe.pack(pady=10)

btn_salir = tk.Button(
    menu_frame,
    text="10. Salir",
    fg="red", #color texto
    command=root.destroy, #comando para cerrar
    width=20,
    pady=5
)
btn_salir.pack(pady=30)


#--------------------------------Advertencia si no hay codigo en memoria--------------------------------------

def no_hay_code(): #en caso de que la memoria este vacía, se comprueba antes  
    Mbox("Error", "No hay ningún código cargado en memoria.",0)
    
root.mainloop() #LOOP PARA VENTANA SIEMPRE DEBE IR DE ULTIMO


