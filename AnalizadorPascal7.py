import re
import tkinter as tk
from tkinter import messagebox

# Clase PascalLexer para tokenizar el código Pascal
class PascalLexer:
    # Definición de los tipos de tokens con expresiones regulares
    tokens = [
        ('KEYWORD', r'\b(program|begin|end|var|integer|real|boolean|procedure|function|if|then|else|while|do|for|to|downto|repeat|until|case|of|write|writeln|read|readln)\b'),
        ('NUMBER', r'\b\d+(\.\d+)?\b'),
        ('IDENTIFIER', r'\b[A-Za-z_][A-Za-z0-9_]*\b'),
        ('OPERATOR', r'[\+\-\*/:=<>]'),
        ('DELIMITER', r'[;,\(\)\[\]\.]'),
        ('WHITESPACE', r'\s+'),
        ('UNKNOWN', r'.')
    ]

    def __init__(self, code):
        self.code = code
        self.pos = 0

    # Método para obtener el siguiente token
    def get_token(self):
        if self.pos >= len(self.code):
            return None, None
        for token_type, pattern in self.tokens:
            regex = re.compile(pattern)
            match = regex.match(self.code, self.pos)
            if match:
                token = match.group(0)
                self.pos = match.end(0)
                if token_type != 'WHITESPACE':  # Ignorar espacios en blanco
                    return token_type, token
        unknown_char = self.code[self.pos]
        self.pos += 1
        return 'UNKNOWN', unknown_char

    # Método para tokenizar todo el código
    def tokenize(self):
        tokens = []
        while self.pos < len(self.code):
            token_type, token = self.get_token()
            if token_type and token:
                tokens.append((token_type, token))
        return tokens

# Clase PascalParser para analizar sintácticamente los tokens
class PascalParser:
    def __init__(self, tokens):
        self.tokens = tokens
        self.pos = 0

    # Método para verificar y avanzar al siguiente token si coincide
    def match(self, expected_type, expected_value=None):
        if self.pos < len(self.tokens) and self.tokens[self.pos][0] == expected_type:
            if expected_value is None or self.tokens[self.pos][1] == expected_value:
                print(f"Matched {expected_type} with value {self.tokens[self.pos][1]}")  # Depuración
                self.pos += 1
                return True
        return False

    # Método para analizar la estructura principal del programa
    def parse_program(self):
        print("Parsing program")  # Depuración
        if not self.match('KEYWORD', 'program'):
            return self.error("Expected 'program'")
        if not self.match('IDENTIFIER'):
            return self.error("Expected program name")
        if not self.match('DELIMITER', ';'):
            return self.error("Expected ';' after program name")
        if not self.parse_block():
            return self.error("Invalid block")
        if not self.match('DELIMITER', '.'):
            return self.error("Expected '.' at the end")
        return True

    # Método para analizar un bloque (declaraciones y sentencias)
    def parse_block(self):
        print("Parsing block")  # Depuración
        return self.parse_variable_declaration_part() and self.parse_statement_part()

    # Método para analizar la parte de declaración de variables
    def parse_variable_declaration_part(self):
        print("Parsing variable declaration part")  # Depuración
        if self.match('KEYWORD', 'var'):
            while True:
                if not self.parse_variable_declaration():
                    return self.error("Invalid variable declaration")
                if not self.match('DELIMITER', ';'):
                    return self.error("Expected ';' after variable declaration")
                if not self.peek('IDENTIFIER'):
                    break
            return True
        return True  # Permitir parte de declaración de variables vacía

    # Método para analizar una declaración de variable
    def parse_variable_declaration(self):
        print("Parsing variable declaration")  # Depuración
        if not self.match('IDENTIFIER'):
            return self.error("Expected variable name")
        while self.match('DELIMITER', ','):
            if not self.match('IDENTIFIER'):
                return self.error("Expected variable name after ','")
        if not self.match('DELIMITER', ':'):
            return self.error("Expected ':' after variable name(s)")
        if not self.parse_type():
            return self.error("Expected type after ':'")
        return True

    # Método para analizar el tipo de variable
    def parse_type(self):
        print("Parsing type")  # Depuración
        return self.match('KEYWORD', 'integer') or self.match('KEYWORD', 'real') or self.match('KEYWORD', 'boolean')

    # Método para analizar la parte de sentencias
    def parse_statement_part(self):
        print("Parsing statement part")  # Depuración
        return self.parse_compound_statement()

    # Método para analizar una sentencia compuesta
    def parse_compound_statement(self):
        print("Parsing compound statement")  # Depuración
        if not self.match('KEYWORD', 'begin'):
            return self.error("Expected 'begin'")
        while True:
            if not self.parse_statement():
                return self.error("Invalid statement")
            if not self.match('DELIMITER', ';'):
                break
        if not self.match('KEYWORD', 'end'):
            return self.error("Expected 'end'")
        return True

    # Método para analizar una sentencia
    def parse_statement(self):
        print("Parsing statement")  # Depuración
        if self.match('IDENTIFIER'):
            return self.match('OPERATOR', ':=') and self.parse_expression()
        return self.parse_compound_statement()

    # Método para analizar una expresión
    def parse_expression(self):
        print("Parsing expression")  # Depuración
        return self.match('NUMBER') or self.match('IDENTIFIER')

    # Método para mirar el siguiente token sin consumirlo
    def peek(self, expected_type):
        return self.pos < len(self.tokens) and self.tokens[self.pos][0] == expected_type

    # Método para reportar errores de análisis
    def error(self, message):
        if self.pos < len(self.tokens):
            token_type, token = self.tokens[self.pos]
            print(f"Error: {message} at token {token_type} with value {token}")
        else:
            print(f"Error: {message} at end of input")
        return False

# Función para verificar el código ingresado en el área de texto
def check_code():
    code = text.get("1.0", "end-1c")  # Obtener el código del área de texto
    lexer = PascalLexer(code)
    tokens = lexer.tokenize()
    
    # Imprimir tokens para depuración
    for token_type, token in tokens:
        print(f"Token: {token_type}, Value: {token}")
        if token_type == 'UNKNOWN':
            messagebox.showerror("Error", f"Error de sintaxis: {token}")
            return

    parser = PascalParser(tokens)
    if parser.parse_program():
        messagebox.showinfo("Éxito", "El código es válido.")
    else:
        messagebox.showerror("Error", "El código es inválido.")

# Creasion de la interfaz gráfica usando tkinter
root = tk.Tk()
root.title("Analizador Léxico y Sintáctico para Pascal")

# ventana de texto para ingresar el código Pascal
text = tk.Text(root, height=20, width=60)
text.pack(pady=10)

# Botón para verificar el código
check_button = tk.Button(root, text="Verificar Código", command=check_code)
check_button.pack(pady=10)

# Iniciar el bucle principal de la interfaz gráfica
root.mainloop()
