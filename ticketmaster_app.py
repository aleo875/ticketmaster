import tkinter as tk
from tkinter import messagebox
from tkinter import ttk
import mysql.connector
import bcrypt
import uuid # Para generar el código único del boleto
from datetime import datetime
from twilio.rest import Client # API de WhatsApp

class TicketMasterApp:
    def __init__(self, root):
        self.root = root
        self.root.title("TicketMaster - Base de Datos y WhatsApp")
        self.root.geometry("400x500")
        self.usuario_actual = None # Almacenará el ID del usuario logueado
        self.intentos_fallidos = 0
        self.mostrar_login()

    def conectar_db(self):
        """Establece la conexión con MySQL"""
        try:
            conexion = mysql.connector.connect(
                host="localhost",
                user="root",       # <--- CAMBIA SI TU USUARIO ES OTRO
                password="greta",       # <--- PON TU CONTRASEÑA DE MYSQL
                database="ticketmaster"
            )
            return conexion
        except mysql.connector.Error as err:
            messagebox.showerror("Error de BD", f"No se pudo conectar: {err}")
            return None

    def limpiar(self):
        for widget in self.root.winfo_children():
            widget.destroy()

    # ================= REGISTRO DE USUARIO =================
    def mostrar_registro(self):
        self.limpiar()
        tk.Label(self.root, text="REGISTRO DE USUARIO", font=("Arial", 14, "bold")).pack(pady=20)

        tk.Label(self.root, text="Nombre completo:").pack()
        self.reg_nombre = tk.Entry(self.root, width=30)
        self.reg_nombre.pack()

        tk.Label(self.root, text="Correo electrónico:").pack()
        self.reg_correo = tk.Entry(self.root, width=30)
        self.reg_correo.pack()
        
        tk.Label(self.root, text="Teléfono (con código de país, ej. +52...):").pack()
        self.reg_telefono = tk.Entry(self.root, width=30)
        self.reg_telefono.pack()

        tk.Label(self.root, text="Contraseña:").pack()
        self.reg_password = tk.Entry(self.root, show="*", width=30)
        self.reg_password.pack()

        tk.Button(self.root, text="Registrarse", command=self.registrar_usuario, bg="lightblue").pack(pady=15)
        tk.Button(self.root, text="Volver al Login", command=self.mostrar_login).pack()

    def registrar_usuario(self):
        nombre = self.reg_nombre.get()
        correo = self.reg_correo.get()
        telefono = self.reg_telefono.get()
        password = self.reg_password.get()

        if not nombre or not correo or not telefono or not password:
            messagebox.showwarning("Advertencia", "Todos los campos son obligatorios")
            return

        # Hashing seguro de la contraseña
        salt = bcrypt.gensalt()
        password_hash = bcrypt.hashpw(password.encode('utf-8'), salt)

        conexion = self.conectar_db()
        if conexion:
            try:
                cursor = conexion.cursor()
                sql = "INSERT INTO Usuarios (nombre, correo, telefono, password_hash) VALUES (%s, %s, %s, %s)"
                valores = (nombre, correo, telefono, password_hash.decode('utf-8')) # Se decodifica para guardarlo como string
                cursor.execute(sql, valores)
                conexion.commit()
                messagebox.showinfo("Éxito", "Usuario registrado correctamente.")
                self.mostrar_login()
            except mysql.connector.IntegrityError:
                messagebox.showerror("Error", "Este correo ya está registrado.")
            finally:
                cursor.close()
                conexion.close()

    # ================= INICIO DE SESIÓN =================
    def mostrar_login(self):
        self.limpiar()
        tk.Label(self.root, text="INICIO DE SESIÓN", font=("Arial", 14, "bold")).pack(pady=20)

        tk.Label(self.root, text="Correo electrónico:").pack()
        self.log_correo = tk.Entry(self.root, width=30)
        self.log_correo.pack()

        tk.Label(self.root, text="Contraseña:").pack()
        self.log_password = tk.Entry(self.root, show="*", width=30)
        self.log_password.pack()

        tk.Button(self.root, text="Ingresar", command=self.iniciar_sesion, bg="lightgreen").pack(pady=15)
        tk.Button(self.root, text="¿No tienes cuenta? Regístrate", command=self.mostrar_registro).pack()

    def iniciar_sesion(self):
        if self.intentos_fallidos >= 3:
            messagebox.showerror("Bloqueo", "Has superado el número de intentos fallidos. Aplicación bloqueada por seguridad.")
            return

        correo = self.log_correo.get()
        password = self.log_password.get()

        conexion = self.conectar_db()
        if conexion:
            cursor = conexion.cursor(dictionary=True)
            cursor.execute("SELECT * FROM Usuarios WHERE correo = %s", (correo,))
            usuario = cursor.fetchone()
            cursor.close()
            conexion.close()

            if usuario:
                if bcrypt.checkpw(password.encode('utf-8'), usuario['password_hash'].encode('utf-8')):
                    self.usuario_actual = usuario['id_usuario']
                    self.intentos_fallidos = 0 # Reiniciar intentos al entrar
                    messagebox.showinfo("Bienvenido", f"Hola, {usuario['nombre']}")
                    self.mostrar_menu()
                else:
                    self.intentos_fallidos += 1
                    messagebox.showerror("Error", f"Contraseña incorrecta. Intentos restantes: {3 - self.intentos_fallidos}")
            else:
                messagebox.showerror("Error", "Usuario no encontrado.")
    # ================= MENÚ PRINCIPAL =================
    def mostrar_menu(self):
       self.limpiar()
       tk.Label(self.root, text="MENÚ PRINCIPAL", font=("Arial", 16, "bold")).pack(pady=20)
       tk.Label(self.root, text="Seleccione el tipo de evento:").pack(pady=10)

        # Ahora los botones llamarán a una función dinámica
       tk.Button(self.root, text=" Teatro", width=20, command=lambda: self.mostrar_eventos('Teatro')).pack(pady=5)
       tk.Button(self.root, text=" Cine", width=20, command=lambda: self.mostrar_eventos('Cine')).pack(pady=5)
       tk.Button(self.root, text=" Museo", width=20, command=lambda: self.mostrar_eventos('Museo')).pack(pady=5)
        
       tk.Button(self.root, text="Cerrar sesión", command=self.mostrar_login, fg="red").pack(pady=30)

# ================= SELECCIÓN DE EVENTOS Y COMPRA =================
    def mostrar_eventos(self, tipo_evento):
        self.limpiar()
        tk.Label(self.root, text=f"EVENTOS DE {tipo_evento.upper()}", font=("Arial", 14, "bold")).pack(pady=10)

        conexion = self.conectar_db()
        if not conexion: return

        cursor = conexion.cursor(dictionary=True)
        cursor.execute("SELECT * FROM Eventos WHERE tipo_evento = %s", (tipo_evento,))
        eventos = cursor.fetchall()
        cursor.close()
        conexion.close()

        if not eventos:
            tk.Label(self.root, text="No hay eventos disponibles de este tipo.").pack()
            tk.Button(self.root, text="Volver", command=self.mostrar_menu).pack(pady=10)
            return

        # Variables para la compra
        self.evento_seleccionado = tk.StringVar(value=eventos[0]['id_evento'])
        
        tk.Label(self.root, text="Selecciona un evento:").pack()
        # Crear un menú desplegable con los eventos
        opciones_eventos = {f"{e['nombre_evento']} - ${e['precio']}": e['id_evento'] for e in eventos}
        
        combo_eventos = ttk.Combobox(self.root, values=list(opciones_eventos.keys()), width=40, state="readonly")
        combo_eventos.current(0)
        combo_eventos.pack(pady=5)

        tk.Label(self.root, text="Cantidad de boletos:").pack()
        self.cantidad_boletos = tk.Spinbox(self.root, from_=1, to=10, width=5)
        self.cantidad_boletos.pack(pady=5)

        tk.Label(self.root, text="Método de pago:").pack()
        self.metodo_pago = ttk.Combobox(self.root, values=["Tarjeta de Crédito", "Tarjeta de Débito", "PayPal"], state="readonly")
        self.metodo_pago.current(0)
        self.metodo_pago.pack(pady=5)

        tk.Button(self.root, text="Proceder al Pago", bg="lightgreen", 
                  command=lambda: self.procesar_compra(opciones_eventos[combo_eventos.get()])).pack(pady=20)
        tk.Button(self.root, text="Volver", command=self.mostrar_menu).pack()

    def procesar_compra(self, id_evento):
        cantidad = int(self.cantidad_boletos.get())
        metodo = self.metodo_pago.get()
        codigo_boleto = str(uuid.uuid4())[:8].upper()

        # Validación: Sistema fuera de horario (Ejemplo: no operar entre 2 AM y 5 AM)
        hora_actual = datetime.now().hour
        if hora_actual >= 2 and hora_actual < 5:
            messagebox.showerror("Fuera de servicio", "El sistema de compras no opera entre las 2:00 AM y 5:00 AM.")
            return

        conexion = self.conectar_db()
        if not conexion: return

        cursor = conexion.cursor(dictionary=True)
        
        # 1. Obtener detalles del evento para el total y comprobación de capacidad
        cursor.execute("SELECT * FROM Eventos WHERE id_evento = %s", (id_evento,))
        evento = cursor.fetchone()
        
        # Validación: Revisar si hay suficientes boletos
        if cantidad > evento['capacidad']:
            messagebox.showerror("Agotado", f"Lo sentimos, solo quedan {evento['capacidad']} boletos disponibles.")
            cursor.close()
            conexion.close()
            return
            
        total_pagado = float(evento['precio']) * cantidad

        try:
            # 2. Registrar la transacción en la Base de Datos
            sql_transaccion = """INSERT INTO Transacciones 
                                 (id_usuario, id_evento, cantidad_boletos, metodo_pago, total_pagado, codigo_boleto) 
                                 VALUES (%s, %s, %s, %s, %s, %s)"""
            cursor.execute(sql_transaccion, (self.usuario_actual, id_evento, cantidad, metodo, total_pagado, codigo_boleto))
            
            # 3. ACTUALIZAR LA CAPACIDAD EN LA BASE DE DATOS (Resta los boletos comprados)
            sql_update = "UPDATE Eventos SET capacidad = capacidad - %s WHERE id_evento = %s"
            cursor.execute(sql_update, (cantidad, id_evento))

            # 4. Obtener el teléfono del usuario para WhatsApp
            cursor.execute("SELECT nombre, telefono FROM Usuarios WHERE id_usuario = %s", (self.usuario_actual,))
            usuario = cursor.fetchone()
            
            conexion.commit() # Confirmar cambios (transacción y actualización)
            
            messagebox.showinfo("Éxito", f"Compra realizada con éxito.\nTotal pagado: ${total_pagado}\nEnviando boleto por WhatsApp...")
            
            self.enviar_whatsapp(usuario['nombre'], usuario['telefono'], evento, cantidad, metodo, total_pagado, codigo_boleto)
            self.mostrar_menu()

        except mysql.connector.Error as err:
            conexion.rollback() # Revierte los cambios si algo falla
            messagebox.showerror("Error", f"Fallo al procesar la compra: {err}")
        finally:
            cursor.close()
            conexion.close()

    # ================= INTEGRACIÓN API WHATSAPP =================
    def enviar_whatsapp(self, nombre, telefono, evento, cantidad, metodo, total, codigo):
        # AQUI PON TUS CREDENCIALES DE TWILIO
        TWILIO_ACCOUNT_SID = 'AC574436387636c1883facc26d152062e8'
        TWILIO_AUTH_TOKEN = 'ab35e11e2fa4e22594e6e1ee809bc8e3'
        TWILIO_PHONE_NUMBER = 'whatsapp:+14155238886' # Revisa si el tuyo es diferente en Twilio

        try:
            client = Client(TWILIO_ACCOUNT_SID, TWILIO_AUTH_TOKEN)

            mensaje_cuerpo = f"""
🎫 *TICKETMASTER CONFIRMACIÓN* 🎫
Hola {nombre}, ¡gracias por tu compra!

*Evento:* {evento['nombre_evento']} ({evento['tipo_evento']})
*Ubicación:* {evento['ubicacion']}
*Fecha:* {evento['horario']}
*Boletos:* {cantidad}
*Método de Pago:* {metodo}
*Total Pagado:* ${total}

🔑 *CÓDIGO DE ACCESO:* {codigo}

¡Disfruta tu evento!
"""
            # Asegúrate de que el teléfono destino tenga el formato correcto (ej. whatsapp:+521234567890)
            numero_destino = f"whatsapp:{telefono}"

            message = client.messages.create(
                body=mensaje_cuerpo,
                from_=TWILIO_PHONE_NUMBER,
                to=numero_destino
            )
            print(f"Mensaje de WhatsApp enviado: {message.sid}")
            
        except Exception as e:
            messagebox.showerror("Error WhatsApp", f"La compra se guardó, pero hubo un error enviando el WhatsApp:\n{str(e)}")

if __name__ == "__main__":
    root = tk.Tk()
    app = TicketMasterApp(root)
    root.mainloop()