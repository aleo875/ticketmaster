import tkinter as tk
from tkinter import messagebox
import re

def registrar_usuario():
    # Obtener los datos de las cajas de texto
    nombre = entry_nombre.get().strip()
    correo = entry_correo.get().strip()
    password = entry_password.get()
    confirmacion = entry_confirmacion.get()

    # ==========================================
    # PRUEBAS DE CAJA BLANCA (Validaciones lógicas)
    # ==========================================

    # 1. Validar campos vacíos
    if not nombre or not correo or not password or not confirmacion:
        messagebox.showerror("Error de Validación", "Todos los campos son obligatorios.")
        return

    # 2. Validar Nombre: Solo letras y espacios (incluyendo acentos y la ñ)
    if not re.match(r"^[A-Za-zÁÉÍÓÚáéíóúÑñ\s]+$", nombre):
        messagebox.showerror("Error de Validación", "El nombre solo debe contener letras y espacios.")
        return

    # 3. Validar Correo: Formato estándar de email (ej. algo@dominio.com)
    if not re.match(r"^[\w\.-]+@[\w\.-]+\.\w+$", correo):
        messagebox.showerror("Error de Validación", "El formato del correo electrónico no es válido.")
        return

    # 4. Validar Contraseña: Al menos 8 caracteres, una mayúscula y un número
    if len(password) < 8 or not any(c.isupper() for c in password) or not any(c.isdigit() for c in password):
        messagebox.showerror("Error de Validación", "La contraseña debe tener al menos 8 caracteres, incluir una mayúscula y un número.")
        return

    # 5. Validar Confirmación: Deben ser exactamente iguales
    if password != confirmacion:
        messagebox.showerror("Error de Validación", "Las contraseñas no coinciden.")
        return

    # ==========================================
    # PRUEBA DE CAJA NEGRA (Resultado Esperado)
    # ==========================================
    messagebox.showinfo("Éxito", "Registro exitoso")


# ==========================================
# INTERFAZ GRÁFICA (GUI)
# ==========================================
root = tk.Tk()
root.title("Sistema de Registro")
root.geometry("350x300")
root.configure(padx=20, pady=20)

# Etiquetas y campos de entrada
tk.Label(root, text="Nombre completo:").pack(anchor="w")
entry_nombre = tk.Entry(root, width=40)
entry_nombre.pack(pady=5)

tk.Label(root, text="Correo electrónico:").pack(anchor="w")
entry_correo = tk.Entry(root, width=40)
entry_correo.pack(pady=5)

tk.Label(root, text="Contraseña:").pack(anchor="w")
entry_password = tk.Entry(root, width=40, show="*")
entry_password.pack(pady=5)

tk.Label(root, text="Confirmar contraseña:").pack(anchor="w")
entry_confirmacion = tk.Entry(root, width=40, show="*")
entry_confirmacion.pack(pady=5)

# Botón de registro
btn_registrar = tk.Button(root, text="Registrar", command=registrar_usuario, bg="#4CAF50", fg="white", font=("Arial", 10, "bold"))
btn_registrar.pack(pady=20)

# Iniciar la aplicación
root.mainloop()