# 📚 Registro de Lecturas

**Registro de Lecturas** es una aplicación de escritorio desarrollada en Python con arquitectura **Modelo-Vista-Controlador (MVC)** que te permite llevar un seguimiento detallado de todos los libros que leíste. Podrás registrar cada lectura, filtrar por año, género o calificación, generar informes y estadísticas personalizadas, y exportar tus datos a CSV.

> _“La lectura es a la mente lo que el ejercicio es al cuerpo.” – Joseph Addison_

---

## 🚀 Características principales

- Interfaz gráfica intuitiva y moderna creada con **Tkinter**
- Registro de libros con campos detallados (título, autor, género, año, calificación, etc.)
- Filtros por año, género y calificación
- Edición y eliminación de libros
- Exportación a archivo CSV
- Generación de informes de lectura
- Panel de usuario editable
- Estadísticas visuales de tus hábitos de lectura
- Paleta de colores suave estilo literario

---

## 🛠️ Tecnologías utilizadas

- Python 3.13.3
- Tkinter
- SQLite
- Estructura MVC
- PyInstaller (para generar el ejecutable `.exe`)

---

## 🧩 Estructura del proyecto

```

.
├── main.py                 # Punto de entrada
├── controlador.py          # Lógica de control
├── modelo.py               # Interacción con base de datos
├── vista.py                # Interfaz gráfica
├── db/
│   └── lecturas.db         # Base de datos SQLite
├── src/
│   └── logo.ico            # Ícono de la app
├── Registro-Lecturas.exe   # Ejecutable generado
├── INTALACION.txt          # Guía detallada de instalación para principiantes
├── build/                  # Carpeta generada por PyInstaller
├── dist/                   # Carpeta generada por PyInstaller
├── RegistroLecturas.spec   # Carpeta generada por PyInstaller
├── README.md               # Documentación de la aplicación

```

---

## ✅ Instalación

1. Asegúrate de tener Python instalado. Si no lo tienes, sigue la guía incluida en `INTALACION.txt`.
2. Cloná este repositorio o descargá los archivos.
3. Ejecutá la aplicación con:

```bash
python main.py
````

O directamente abrí `Registro-Lecturas.exe` en la carpeta raíz (requiere Windows 64 bits).

---

## 💡 ¿Por qué usar esta app?

* Porque leer es crecer.
* Porque cada libro cuenta una historia, y ahora vos podés contar qué libros forman parte de tu viaje lector.
* Porque no solo registrás libros, sino también tu evolución como lector o lectora.

> *“Un hogar sin libros es como un cuerpo sin alma.” – Cicerón*

---

## ✍️ Autor

**Sebastián Sánchez Bentolila**
📧 [sebastiansb3004@gmail.com](mailto:sebastiansb3004@gmail.com)
🔗 [LinkedIn](https://www.linkedin.com/in/sebastian-sanchez-bentolila/)
🐱 [GitHub](https://github.com/Sebastian-Sanchez-Bentolila)
📷 [Instagram](https://instagram.com/pedaleando_el_alma)

---

## 🧪 Licencia

Este proyecto está bajo la licencia MIT.

---

¡Gracias por usar Registro de Lecturas! Que tus libros te sigan llevando lejos 🚴📖