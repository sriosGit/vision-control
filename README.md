# 🎮 Vision Control

<div align="center">

![Python](https://img.shields.io/badge/Python-3.7+-blue.svg)
![OpenCV](https://img.shields.io/badge/OpenCV-4.8.1-orange.svg)
![MediaPipe](https://img.shields.io/badge/MediaPipe-0.10.21-green.svg)
![macOS](https://img.shields.io/badge/macOS-Only-red.svg)

**Control de volumen y apagado del sistema mediante gestos de manos**

[Características](#-características) • [Instalación](#-instalación) • [Uso](#-uso) • [Gestos](#-gestos) • [Requisitos](#-requisitos)

</div>

---

## ✨ Características

- 🎵 **Control de volumen**: Ajusta el volumen del sistema con gestos simples
- 🔌 **Apagado remoto**: Apaga tu Mac con un gesto específico
- 📹 **Reconocimiento en tiempo real**: Detección instantánea de gestos usando MediaPipe
- ️ **Interfaz visual**: Vista en espejo con indicadores en pantalla
- ⚡ **Respuesta inmediata**: Control fluido y sin retrasos

## 🚀 Instalación

### Prerrequisitos

- macOS (sistema operativo requerido)
- Python 3.7 o superior
- Cámara web funcional

### Pasos de instalación

1. **Clona el repositorio**
   ```bash
   git clone https://github.com/tu-usuario/vision-control.git
   cd vision-control
   ```

2. **Instala las dependencias**
   ```bash
   pip install -r requirements.txt
   ```

3. **Ejecuta la aplicación**
   ```bash
   python volume_control.py
   ```

## 🎯 Uso

Una vez ejecutado el programa:

1. **Permite acceso a la cámara** cuando se solicite
2. **Posiciona tu mano** frente a la cámara
3. **Realiza los gestos** para controlar el sistema
4. **Presiona 'q'** para salir del programa

## 🤚 Gestos Soportados

| Gesto | Acción | Descripción |
|-------|--------|-------------|
| ✋ **Mano abierta** | Subir volumen | Todos los dedos extendidos |
| ✊ **Puño cerrado** | Bajar volumen | Todos los dedos doblados |
| 🖕 **Dedo medio** | Apagar sistema | Solo el dedo medio levantado (3 segundos) |

### Detalles de los gestos:

- **Mano abierta**: Aumenta el volumen en incrementos de 2%
- **Puño cerrado**: Disminuye el volumen en incrementos de 2%
- **Dedo medio**: Inicia una cuenta regresiva de 3 segundos para apagar el sistema

## 📋 Requisitos del Sistema

- **Sistema Operativo**: macOS (exclusivamente)
- **Python**: 3.7 o superior
- **Cámara**: Webcam funcional
- **Permisos**: Acceso a la cámara y control del sistema

### Dependencias

```
opencv-python==4.8.1.78
mediapipe==0.10.21
```

## 🔧 Configuración Avanzada

### Ajustar sensibilidad

Puedes modificar los parámetros de detección en el código:

```python
hands = mp_hands.Hands(
    static_image_mode=False,
    max_num_hands=1,
    min_detection_confidence=0.7,  # Sensibilidad de detección
    min_tracking_confidence=0.5    # Sensibilidad de seguimiento
)
```

### Cambiar incrementos de volumen

Modifica estos valores en el código:

```python
current_volume = max(0, current_volume - 2)  # Para bajar volumen
current_volume = min(100, current_volume + 2)  # Para subir volumen
```

## 🛠️ Solución de Problemas

### La cámara no se abre
- Verifica que tu cámara esté funcionando
- Asegúrate de haber dado permisos de cámara a Python

### Los gestos no se detectan
- Asegúrate de tener buena iluminación
- Mantén tu mano a una distancia adecuada de la cámara
- Verifica que no haya obstáculos entre tu mano y la cámara

### El volumen no cambia
- Verifica que tengas permisos de administrador
- Asegúrate de que el sistema de audio esté funcionando

## 🤝 Contribuir

¡Las contribuciones son bienvenidas! Para contribuir:

1. Fork el proyecto
2. Crea una rama para tu feature (`git checkout -b feature/AmazingFeature`)
3. Commit tus cambios (`git commit -m 'Add some AmazingFeature'`)
4. Push a la rama (`git push origin feature/AmazingFeature`)
5. Abre un Pull Request

## 📄 Licencia

Este proyecto está bajo la Licencia MIT. Ver el archivo `LICENSE` para más detalles.

## �� Agradecimientos

- [MediaPipe](https://mediapipe.dev/) por el framework de detección de manos
- [OpenCV](https://opencv.org/) por el procesamiento de imágenes
- [Apple](https://www.apple.com/) por las herramientas de control del sistema macOS

---

<div align="center">

**¡Disfruta controlando tu Mac con gestos! 🎉**

</div>