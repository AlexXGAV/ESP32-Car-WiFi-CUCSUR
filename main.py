import socket
import machine
import network
import uasyncio as asyncio

# Configuración de pines
motorA1_pwm = machine.PWM(machine.Pin(15), freq=1000, duty=0)  # Pin para el motor A
motorA2_pwm = machine.PWM(machine.Pin(21), freq=1000, duty=0)  # Pin para el motor A
motorB1_pwm = machine.PWM(machine.Pin(22), freq=1000, duty=0)  # Pin para el motor B
motorB2_pwm = machine.PWM(machine.Pin(23), freq=1000, duty=0)  # Pin para el motor B

LED = machine.Pin(2, machine.Pin.OUT)  # Pin para pruebas

# Configuración de red como Access Point
ap = network.WLAN(network.AP_IF)
ap.active(True)
ap.config(essid='Carro', password='carroAAA', authmode=network.AUTH_WPA_WPA2_PSK)


# Función para controlar el carro
def controlar_carro(data):
    #print(data)
    try:
        #data = data.decode('utf-8')
         # Obtener la cadena de parámetros del cuerpo de la solicitud
        body_start = data.find(b'\r\n\r\n') + 4  # Encuentra el inicio del cuerpo
        params_data = data[body_start:].decode('utf-8')
        params = {}
        for item in params_data.split('&'):
            key, value = item.split('=')
            params[key] = int(value)
            #print(key, value)
        
        motorA = params.get('motorA', 0)
        motorB = params.get('motorB', 0)
        estadoAB = params.get('estadoAB', 0)
        estadoC = params.get('estadoC', 0)
        estadoH = params.get('estadoH', 0)
        
        # Control de motores
        if (estadoAB==0):
            motorA1_pwm.duty(motorA)
            motorA2_pwm.duty(0)
            motorB1_pwm.duty(motorB)
            motorB2_pwm.duty(0)
        else:
            motorA1_pwm.duty(0)
            motorA2_pwm.duty(motorA)
            motorB1_pwm.duty(0)
            motorB2_pwm.duty(motorB)
        
        
    except Exception as e:
        #print("Error al procesar los datos:", e)
        pass

# Función principal
async def main():
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.bind(('0.0.0.0', 80))
    server_socket.listen(5)
    
    while True:
        client_socket, client_addr = server_socket.accept()
        #print('Conexión entrante desde:', client_addr)
        
        try:
            data = client_socket.recv(2048)
            if data:
                controlar_carro(data)
                LED.value(True)
            #client_socket.send('HTTP/1.1 200 OK\n\n'.encode('utf-8'))
        except Exception as e:
            #print("Error de conexión:", e)
            pass
        finally:
            client_socket.close()
            LED.value(False)

if __name__ == '__main__':
    #print("Dirección IP del ESP32:", network.WLAN(network.AP_IF).ifconfig()[0])
    asyncio.run(main())


