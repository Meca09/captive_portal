import network
from machine import Pin
import ujson
import usocket as socket

# Configura los detalles del portal cautivo
AP_SSID = 'ESP32-AP'
AP_PASSWORD = 'micropython'
CAPTIVE_PORT = 80

# Crea una instancia del punto de acceso
ap = network.WLAN(network.AP_IF)
ap.active(True)
ap.config(essid=AP_SSID, password=AP_PASSWORD)

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

# Configura el servidor de portal cautivo
captive_server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
captive_server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
captive_server.bind(('', CAPTIVE_PORT))
captive_server.listen(1)

print('Portal cautivo configurado')
print('SSID:', AP_SSID)
print('Contraseña:', AP_PASSWORD)
print('Dirección IP:', ap.ifconfig()[0])

# Función para manejar las solicitudes HTTP
def handle_request(client_sock):
    client_stream = client_sock.makefile('rwb')
    
    # Leer la solicitud HTTP
    first_line = client_stream.readline().decode('utf-8')
    method, path, version = first_line.split(' ')
    
    # Generar la respuesta HTTP
    if path == '/':
        response_status = '200 OK'
        response_headers = 'Content-Type: text/html\r\n'
        response_content = form_html.encode('utf-8')
    elif path == '/submit':
        content_length = 0
        while True:
            line = client_stream.readline()
            if not line or line == b'\r\n':
                break
            if line.startswith(b'Content-Length:'):
                content_length = int(line.split(b':')[1])
        
        client_stream.read(content_length)  # Descartar el cuerpo de la solicitud
        
        response_status = '200 OK'
        response_headers = 'Content-Type: text/html\r\n'
        response_content = submit_html.encode('utf-8')
    else:
        response_status = '404 Not Found'
        response_headers = 'Content-Type: text/html\r\n'
        response_content = b'404 Not Found'
    
    # Enviar la respuesta HTTP
    response_headers += 'Connection: close\r\n'
    response = 'HTTP/1.1 %s\r\n%s\r\n%s' % (response_status, response_headers, response_content)
    client_sock.sendall
