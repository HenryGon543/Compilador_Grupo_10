#librerias
import tkinter as tk
import ply.lex as lex
import ctypes

#variables
color_bg = "#181818" #color del fondo de la barra

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
    'print': 'PRINT'
}

#Lista de tokens
tokens = [
    'ID',
    'NUMERO',
    'OPERACION',
    'ASIGNACION',
    'PUNTOCOMA',
    'PARENTESIS',
] + list(reserved.values())

#Definir reglas
#se debe usar regex para registrar simbolos como el + o * porque phyton los usa como palabras reservadas
t_OPERACION = r'\+ | - | \* | /'
t_ASIGNACION = r'='
t_PUNTOCOMA = r';'
t_PARENTESIS = r'\( | \)'
t_ignore = ' \t' #saltos de linea

def t_ID(t):
    r'[a-zA-Z_][a-zA-Z_0-9]*'
    t.type = reserved.get(t.value, 'ID')
    return t

def t_NUMERO(t):
    r'\d+(\.\d+)?'
    t.value = float(t.value) if '.' in t.value else int(t.value)
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
    
    #Obtener código del editor
    codigo = obtener_codigo()
    print(codigo)

    limpiar_contenido()
    
    global tokens_text

    titulo = tk.Label(
        content_frame,
        text="Análisis Léxico - Tokens",
        font=("Arial", 16, "bold"),
        bg="#e4faff"
    )
    titulo.pack(pady=10)

    tokens_frame = tk.Frame(content_frame)
    tokens_frame.pack(fill="both", expand=True, padx=10, pady=10)

    scrollbar = tk.Scrollbar(tokens_frame)
    scrollbar.pack(side="right", fill="y")



    tokens_text = tk.Text( #CUADRO DE TEXTO PARA LOS TOKENS
        tokens_frame,
        font=("Consolas", 11),
        yscrollcommand=scrollbar.set,
        state="normal",
        fg="#FFFFFF",
        bg="#000000"
    )
    tokens_text.pack(fill="both", expand=True)
    scrollbar.config(command=tokens_text.yview)


    lexer.lineno = 1
    lexer.input(codigo)

# Encabezado
    tokens_text.insert("end", f"{'TIPO':<10}{'LEXEMA':<10}{'LÍNEA'}\n\n\n")

    # Generar tokens
    for tok in lexer:
        tokens_text.insert(
            "end",
            f"{tok.type:<15}{str(tok.value):<15}{tok.lineno}\n"
        )

    tokens_text.config(state="disabled")




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
    width=20,
    pady=5
)
btn_sintactico.pack(pady=10)

btn_tabla = tk.Button(
    menu_frame,
    text="Tabla de símbolos",
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
