import cv2
import threading
from tkinter import Tk, Frame, Label, StringVar
import requests
import time
import netifaces
from PIL import Image, ImageTk

flash_on = False
speed = 0
state_on_move = False
last_letter = ' '

def control_motor(c):
    global state_on_move
    global last_letter
    last_letter = c
    if c == ' ':
        state_on_move = False
        return '0', '0', '0', '0', '0'
    elif c == 'w':
        state_on_move = True
        return str(speed), str(speed), '0', '0', '0'
    elif c == 'd':
        state_on_move = True
        return str(speed), '0', '0', '0', '0'
    elif c == 'a':
        state_on_move = True
        return '0', str(speed), '0', '0', '0'
    elif c == 's':
        state_on_move = True
        return str(speed), str(speed), '1', '0', '0'



def key_pressed(e):
    global flash_on
    global speed
    c = e.char.lower()
    if c in 'wasd ':
        stringvar.set(frases.get(c, 'Control Inválido'))
        motor_params = dict(zip(['motorA', 'motorB', 'estadoAB', 'estadoC', 'estadoH'], control_motor(c)))
        print(motor_params)
        params.update(motor_params)
        enviar()
        # Actualizar el Label de velocidad
        velocidad_label.config(text=f"Velocidad: {speed}")
    elif c == 'f':
        flash_on = not flash_on
        flash_value = 1 if flash_on else 0
        flash_url = f"http://192.168.4.2/control?var=flash&val={flash_value}"
        try:
            response = requests.get(flash_url)
        except Exception as e:
            pass
        print("Flash activado" if flash_on else "Flash desactivado")
    elif c == '+':
        speed += 128
        if speed > 1023:
            speed = 1023
        if state_on_move:
            #stringvar.set(frases.get(c, 'Control Inválido'))
            motor_params = dict(zip(['motorA', 'motorB', 'estadoAB', 'estadoC', 'estadoH'], control_motor(last_letter)))
            print(motor_params)
            params.update(motor_params)
            enviar()
        velocidad_label.config(text=f"Velocidad: {speed}")
    elif c == '-':
        speed -= 128
        if speed < 0:
            speed = 0
        if state_on_move:
            #stringvar.set(frases.get(c, 'Control Inválido'))
            motor_params = dict(zip(['motorA', 'motorB', 'estadoAB', 'estadoC', 'estadoH'], control_motor(last_letter)))
            print(motor_params)
            params.update(motor_params)
            enviar()
        velocidad_label.config(text=f"Velocidad: {speed}")

def enviar():
    try:
        response = requests.post(f'http://{IP}', params=params)
        #print(params)
        #print(response.status_code)
    except Exception as e:
        pass
        #print("Error al enviar", e)

def mostrar_video():
    cap = cv2.VideoCapture("http://192.168.4.2:81/stream")
    video_label = Label(root)  # Crea un Label en la ventana principal

    while True:
        ret, frame = cap.read()
        if ret:
            img = Image.fromarray(cv2.cvtColor(frame, cv2.COLOR_BGR2RGB))
            img = ImageTk.PhotoImage(img)

            video_label.config(image=img)
            video_label.img = img
            
            # Utiliza pack en lugar de grid para el Label
            video_label.pack()
            
        key = cv2.waitKey(1)
        if key == 27:  # Presionar Esc para salir
            break
    
    cap.release()
    cv2.destroyAllWindows()


if __name__=="__main__":
    gateways = netifaces.gateways()
    defaults = gateways.get("default")
    gw_info = defaults.get(netifaces.AF_INET)
    IP = gw_info[0]

    frases = {'w': 'Adelante', 's': 'Atras',
            'a': 'Izquierda', 'd': 'Derecha', ' ': 'Alto'}
    params = {'motora': '0', 'motorb': '0', 'state': '0', 'a':'0'}

    root = Tk()             
    root.geometry("400x400")
    root.title("Controlador ESP32")     
    stringvar = StringVar()
    stringvar.set("Controlador ROBOT ESP32")

    frame = Frame(root)     
    lbl_titulo = Label(frame, textvariable=stringvar)   
    lbl_titulo.grid(row=0, column=0, pady=20, padx=20)  

    # Agregar un Label para mostrar la velocidad
    velocidad_label = Label(root, text="Velocidad: 0")
    velocidad_label.pack()

    frame.bind_all("<KeyPress>", key_pressed)
    frame.pack()
    frame.focus_set()

    video_thread = threading.Thread(target=mostrar_video)
    video_thread.start()

    root.mainloop()