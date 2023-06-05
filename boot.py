import gc
import network
import time
import usocket as socket
import ure
import ujson


gc.enable()
CONTENT = open('index.html', 'r').read()

# Define el contenido HTML del formulario
form_html = '''
<!DOCTYPE html>
<html>
<head>
  <title>Formulario ESP32</title>
</head>
<body>
  <h1>Formulario ESP32</h1>
  <form action="/submit" method="POST">
    <label for="nombre">Nombre:</label><br>
    <input type="text" id="nombre" name="nombre" required><br><br>
    <label for="email">Email:</label><br>
    <input type="email" id="email" name="email" required><br><br>
    <input type="submit" value="Enviar">
  </form>
</body>
</html>
'''

# Define el contenido HTML de la página de envío exitoso
submit_html = '''
<!DOCTYPE html>
<html>
<head>
  <title>Formulario Enviado</title>
</head>
<body>
  <h1>Formulario Enviado</h1>
  <p>Tu formulario ha sido enviado exitosamente.</p>
</body>
</html>
'''

def access_point():
    ap_if = network.WLAN(network.AP_IF)   # instancia el objeto -ap_if- para controlar la interfaz AP
    ap_if.config(essid="ESP-AccessPoint") # establece el identificador de red -ESSID- 
    ap_if.config(authmode=2, password="12345678")  # establece el modo de autentificación y la clave de red
    ap_if.config(max_clients=2)           # establece el número de clientes que se pueden conectar a la red
    ap_if.active(True)
    print("ESSID:", ap_if.config('essid'))
    print("Configuración de red (IP/netmask/gw/DNS):", ap_if.ifconfig())
    print("Modo de autentificación:",ap_if.config("authmode"))
    
def handle_request(client_sock):
    request = client_sock.recv(4096)
    if request:
        # Envía el encabezado de respuesta HTTP
        response = "HTTP/1.1 200 OK\nContent-Type: text/html\n\n"
        client_sock.send(response)
        
        # Envía el formulario HTML
        client_sock.send(form_html)

    client_sock.close()

access_point()
captive_server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
captive_server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
captive_server.bind(('', CAPTIVE_PORT))
captive_server.listen(1)


    

