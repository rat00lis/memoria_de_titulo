import imaplib
import email
from email.header import decode_header

# Configuración
IMAP_SERVER = "imap.zoho.com"  # Cambia según tu proveedor
EMAIL_ACCOUNT = "prueba.documentos@zohomail.com"  # Tu dirección de correo
PASSWORD = '''aaaaa'''  # Tu contraseña (o contraseña de aplicación para Gmail)

def listar_correos():
    try:
        # Conexión al servidor IMAP
        mail = imaplib.IMAP4_SSL(IMAP_SERVER)
        mail.login(EMAIL_ACCOUNT, PASSWORD)

        # Seleccionar la bandeja de entrada
        mail.select("inbox")

        # Buscar todos los correos en la bandeja de entrada
        status, mensajes = mail.search(None, "ALL")
        if status != "OK":
            print("No se encontraron correos.")
            return

        # Obtener una lista de IDs de correos
        ids_correos = mensajes[0].split()

        print(f"Se encontraron {len(ids_correos)} correos.")
        for i in ids_correos[-5:]:  # Listar los últimos 5 correos
            status, data = mail.fetch(i, "(RFC822)")  # Obtener el contenido del correo
            if status != "OK":
                print(f"Error obteniendo el correo {i}")
                continue

            # Parsear el correo
            for respuesta in data:
                if isinstance(respuesta, tuple):
                    mensaje = email.message_from_bytes(respuesta[1])

                    # Decodificar el asunto
                    asunto, encoding = decode_header(mensaje["Subject"])[0]
                    if isinstance(asunto, bytes):
                        asunto = asunto.decode(encoding or "utf-8")
                    
                    # Mostrar información básica
                    remitente = mensaje.get("From")
                    print(f"Asunto: {asunto}")
                    print(f"Remitente: {remitente}")
                    print("-" * 50)

        # Cerrar la conexión
        mail.logout()
    except Exception as e:
        print(f"Error: {e}")

# Ejecutar la función
listar_correos()
