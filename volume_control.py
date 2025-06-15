import cv2
import mediapipe as mp
import numpy as np
import subprocess
import time
import os

# Inicializar MediaPipe
mp_hands = mp.solutions.hands
hands = mp_hands.Hands(
    static_image_mode=False,
    max_num_hands=1,
    min_detection_confidence=0.7,
    min_tracking_confidence=0.5
)
mp_draw = mp.solutions.drawing_utils

# Inicializar la cámara
cap = cv2.VideoCapture(0)

def set_volume(volume_level):
    """Establece el volumen del sistema en macOS"""
    # El volumen en macOS va de 0 a 100
    volume_level = max(0, min(100, volume_level))
    cmd = f"osascript -e 'set volume output volume {volume_level}'"
    subprocess.run(cmd, shell=True)

def get_volume():
    """Obtiene el volumen actual del sistema en macOS"""
    cmd = "osascript -e 'output volume of (get volume settings)'"
    result = subprocess.run(cmd, shell=True, capture_output=True, text=True)
    return int(result.stdout.strip())

def is_fist_closed(hand_landmarks):
    """Detecta si la mano está cerrada (puño)"""
    # Índices de los dedos en MediaPipe
    thumb_tip = 4
    index_tip = 8
    middle_tip = 12
    ring_tip = 16
    pinky_tip = 20
    
    # Obtener las coordenadas de las puntas de los dedos
    thumb = hand_landmarks.landmark[thumb_tip]
    index = hand_landmarks.landmark[index_tip]
    middle = hand_landmarks.landmark[middle_tip]
    ring = hand_landmarks.landmark[ring_tip]
    pinky = hand_landmarks.landmark[pinky_tip]
    
    # Obtener las coordenadas de las articulaciones base de los dedos
    thumb_base = hand_landmarks.landmark[2]
    index_base = hand_landmarks.landmark[5]
    middle_base = hand_landmarks.landmark[9]
    ring_base = hand_landmarks.landmark[13]
    pinky_base = hand_landmarks.landmark[17]
    
    # Verificar si cada dedo está doblado
    thumb_bent = thumb.y > thumb_base.y
    index_bent = index.y > index_base.y
    middle_bent = middle.y > middle_base.y
    ring_bent = ring.y > ring_base.y
    pinky_bent = pinky.y > pinky_base.y
    
    # La mano está cerrada si todos los dedos están doblados
    return all([thumb_bent, index_bent, middle_bent, ring_bent, pinky_bent])

def is_hand_open(hand_landmarks):
    """Detecta si la mano está abierta (todos los dedos extendidos)"""
    # Índices de los dedos en MediaPipe
    thumb_tip = 4
    index_tip = 8
    middle_tip = 12
    ring_tip = 16
    pinky_tip = 20
    
    # Obtener las coordenadas de las puntas de los dedos
    thumb = hand_landmarks.landmark[thumb_tip]
    index = hand_landmarks.landmark[index_tip]
    middle = hand_landmarks.landmark[middle_tip]
    ring = hand_landmarks.landmark[ring_tip]
    pinky = hand_landmarks.landmark[pinky_tip]
    
    # Obtener las coordenadas de las articulaciones base de los dedos
    thumb_base = hand_landmarks.landmark[2]
    index_base = hand_landmarks.landmark[5]
    middle_base = hand_landmarks.landmark[9]
    ring_base = hand_landmarks.landmark[13]
    pinky_base = hand_landmarks.landmark[17]
    
    # Verificar si cada dedo está extendido
    thumb_extended = thumb.y < thumb_base.y
    index_extended = index.y < index_base.y
    middle_extended = middle.y < middle_base.y
    ring_extended = ring.y < ring_base.y
    pinky_extended = pinky.y < pinky_base.y
    
    # La mano está abierta si todos los dedos están extendidos
    return all([thumb_extended, index_extended, middle_extended, ring_extended, pinky_extended])

def is_middle_finger_up(hand_landmarks):
    """Detecta si solo el dedo medio está levantado"""
    # Índices de los dedos en MediaPipe
    index_tip = 8
    middle_tip = 12
    ring_tip = 16
    
    # Obtener las coordenadas de las puntas de los dedos
    index = hand_landmarks.landmark[index_tip]
    middle = hand_landmarks.landmark[middle_tip]
    ring = hand_landmarks.landmark[ring_tip]
    
    # Obtener las coordenadas de las articulaciones base de los dedos
    index_base = hand_landmarks.landmark[7]
    middle_base = hand_landmarks.landmark[9]
    ring_base = hand_landmarks.landmark[15]
    
    # Verificar si cada dedo está doblado o extendido
    # Un dedo está doblado si su punta está más abajo que su base (Y mayor)
    index_bent = index.y > index_base.y
    middle_extended = middle.y < middle_base.y  # Dedo medio extendido si su punta está más arriba
    ring_bent = ring.y > ring_base.y
    
    # Solo el dedo medio está levantado si:
    # 1. Está extendido (punta más arriba que la base)
    # 2. Los otros dedos están doblados (puntas más abajo que sus bases)
    return (middle_extended and 
            all([index_bent, ring_bent]))

# Obtener el volumen inicial
current_volume = get_volume()
shutdown_countdown = 0
shutdown_started = False

while True:
    success, img = cap.read()
    if not success:
        break
        
    # Voltear la imagen horizontalmente para una vista espejo
    img = cv2.flip(img, 1)
    
    # Convertir la imagen a RGB para MediaPipe
    imgRGB = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
    
    # Procesar la imagen con MediaPipe
    results = hands.process(imgRGB)
    
    # Si se detectan manos
    if results.multi_hand_landmarks:
        for hand_landmarks in results.multi_hand_landmarks:
            # Dibujar los puntos de referencia
            mp_draw.draw_landmarks(img, hand_landmarks, mp_hands.HAND_CONNECTIONS)
            
            # Obtener el estado de los dedos para debug
            thumb = hand_landmarks.landmark[4]
            index = hand_landmarks.landmark[8]
            middle = hand_landmarks.landmark[12]
            ring = hand_landmarks.landmark[16]
            pinky = hand_landmarks.landmark[20]
            
            # Mostrar las coordenadas Y de cada dedo (para debug)
            y_positions = f"Thumb: {thumb.y:.2f}, Index: {index.y:.2f}, Middle: {middle.y:.2f}, Ring: {ring.y:.2f}, Pinky: {pinky.y:.2f}"
            cv2.putText(img, y_positions, (10, 100), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255), 1)
            
             # Verificar si solo el dedo medio está levantado
            if is_middle_finger_up(hand_landmarks):
                if not shutdown_started:
                    shutdown_started = True
                    shutdown_countdown = 3  # 3 segundos de cuenta regresiva
                    start_time = time.time()
                
                # Calcular el tiempo restante
                elapsed_time = time.time() - start_time
                remaining_time = max(0, shutdown_countdown - int(elapsed_time))
                
                if remaining_time > 0:
                    # Mostrar cuenta regresiva
                    cv2.putText(img, f"Apagando en {remaining_time} segundos...", (10, 50), 
                               cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 2)
                else:
                    # Ejecutar comando de apagado usando osascript
                    print("Apagando...")
                    # Liberar recursos antes de apagar
                    cap.release()
                    cv2.destroyAllWindows()
                    # Iniciar el apagado
                    os.system("osascript -e 'tell app \"System Events\" to shut down'")
                    break
            # Verificar si la mano está cerrada
            elif is_fist_closed(hand_landmarks):
                # Bajar el volumen
                current_volume = max(0, current_volume - 2)  # Reducir el volumen
                set_volume(current_volume)
                
                # Mostrar mensaje y volumen actual en la pantalla
                cv2.putText(img, f"Bajando volumen: {current_volume}%", (10, 50), 
                           cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 2)
                shutdown_countdown = 0
                shutdown_started = False
            
            # Verificar si la mano está abierta
            elif is_hand_open(hand_landmarks):
                # Subir el volumen
                current_volume = min(100, current_volume + 2)  # Aumentar el volumen
                set_volume(current_volume)
                
                # Mostrar mensaje y volumen actual en la pantalla
                cv2.putText(img, f"Subiendo volumen: {current_volume}%", (10, 50), 
                           cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)
                shutdown_countdown = 0
                shutdown_started = False
            else:
                shutdown_countdown = 0
                shutdown_started = False
    
    # Mostrar la imagen
    cv2.imshow("Control de Volumen", img)
    
    # Salir si se presiona 'q'
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# Liberar recursos
cap.release()
cv2.destroyAllWindows() 