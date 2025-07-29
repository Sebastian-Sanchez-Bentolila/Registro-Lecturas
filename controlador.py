#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Registro de Lecturas - controlador.py

Autor: Sebastian Sanchez Bentolila
Email: sebastiansb3004@gmail.com
Versión: 1.0.0
Última modificación: 29/07/2025
Licencia: MIT
Copyright: © 2025 - Todos los derechos reservados

Descripción:
- Coordina la comunicación entre Modelo y Vista
- Implementa la lógica de la aplicación
- Maneja los eventos principales


Dependencias:
- Python 3.13.3
- Módulos estándar: typing, os, datetime
"""

from modelo import libro_model, usuario_model, informe_model
from vista import MainView
from typing import Dict, List, Optional
import os
from datetime import datetime

class MainController:
    """Controlador principal de la aplicación"""
    
    def __init__(self):
        # Inicializar modelos
        self.libro_model = libro_model
        self.usuario_model = usuario_model
        self.informe_model = informe_model
        
        # Inicializar vista
        self.view = MainView(self)
        
        # Cargar datos iniciales
        self._load_initial_data()
        
        # Iniciar la aplicación
        self.view.mainloop()
    
    def _load_initial_data(self):
        """Carga los datos iniciales en la aplicación"""
        # Cargar datos del usuario
        user_data = self.usuario_model.obtener_usuario()
        self.view.update_user_info(user_data)
        
        # Cargar libros y configurar filtros
        self._refresh_books_table()
        
        # Establecer valores por defecto en el formulario
        self.view.clear_form()
    
    def _refresh_books_table(self, filters: Optional[Dict] = None):
        """Actualiza la tabla de libros con los filtros dados"""
        # Obtener libros con filtros
        books = self.libro_model.obtener_libros(filters)
        self.view.populate_books_table(books)
        
        # Actualizar filtros disponibles
        all_books = self.libro_model.obtener_libros()
        years = {book['anio_lectura'] for book in all_books if book.get('anio_lectura')}
        genres = {book['genero'] for book in all_books if book.get('genero')}
        
        self.view.populate_filters(sorted(years, reverse=True), sorted(genres))
    
    def add_book(self):
        """Agrega un nuevo libro desde el formulario"""
        try:
            # Obtener datos del formulario
            book_data = self.view.get_form_data()
            
            # Validar campos obligatorios
            if not book_data.get('titulo') or not book_data.get('autor'):
                self.view.show_message(
                    "Error", 
                    "Título y autor son campos obligatorios", 
                    'error'
                )
                return
            
            # Convertir tipos de datos
            if book_data.get('anio_lectura'):
                try:
                    book_data['anio_lectura'] = int(book_data['anio_lectura'])
                except ValueError:
                    book_data['anio_lectura'] = datetime.now().year
            
            if book_data.get('paginas'):
                try:
                    book_data['paginas'] = int(book_data['paginas'])
                except ValueError:
                    book_data['paginas'] = 0
            
            # Crear el libro
            self.libro_model.crear_libro(book_data)
            
            # Actualizar la vista
            self.view.clear_form()
            self._refresh_books_table()
            
            self.view.show_message(
                "Éxito", 
                "Libro agregado correctamente", 
                'info'
            )
        except Exception as e:
            self.view.show_message(
                "Error", 
                f"No se pudo agregar el libro: {str(e)}", 
                'error'
            )
    
    def filter_books(self):
        """Filtra los libros según los criterios seleccionados"""
        filters = self.view.get_filters()
        self._refresh_books_table(filters)
    
    def clear_filters(self):
        """Limpia todos los filtros aplicados"""
        self._refresh_books_table()
    
    def show_book_details(self):
        """Muestra los detalles del libro seleccionado"""
        book_id = self.view.get_selected_book_id()
        if book_id:
            book = self.informe_model.generar_informe_lectura(book_id)
            self.view.show_book_details(book)
        else:
            self.view.show_message(
                "Advertencia", 
                "Por favor selecciona un libro primero", 
                'warning'
            )
    
    def edit_book(self):
        """Abre el diálogo para editar un libro"""
        book_id = self.view.get_selected_book_id()
        if book_id:
            book = self.libro_model.obtener_libros({'id': book_id})[0]
            self.view.show_book_edit_dialog(book)
        else:
            self.view.show_message(
                "Advertencia", 
                "Por favor selecciona un libro primero", 
                'warning'
            )
    
    def update_book(self, book_id: int, book_data: Dict):
        """Actualiza un libro existente"""
        try:
            # Validar campos obligatorios
            if not book_data.get('titulo') or not book_data.get('autor'):
                self.view.show_message(
                    "Error", 
                    "Título y autor son campos obligatorios", 
                    'error'
                )
                return
            
            # Convertir tipos de datos
            if book_data.get('anio_lectura'):
                try:
                    book_data['anio_lectura'] = int(book_data['anio_lectura'])
                except ValueError:
                    book_data['anio_lectura'] = datetime.now().year
            
            if book_data.get('paginas'):
                try:
                    book_data['paginas'] = int(book_data['paginas'])
                except ValueError:
                    book_data['paginas'] = 0
            
            # Actualizar el libro
            self.libro_model.actualizar_libro(book_id, book_data)
            
            # Actualizar la vista
            self._refresh_books_table()
            
            self.view.show_message(
                "Éxito", 
                "Libro actualizado correctamente", 
                'info'
            )
        except Exception as e:
            self.view.show_message(
                "Error", 
                f"No se pudo actualizar el libro: {str(e)}", 
                'error'
            )
    
    def delete_book(self):
        """Elimina el libro seleccionado"""
        book_id = self.view.get_selected_book_id()
        if book_id:
            confirm = self.view.ask_confirmation(
                "Confirmar eliminación", 
                "¿Estás seguro de que quieres eliminar este libro?"
            )
            
            if confirm:
                try:
                    self.libro_model.eliminar_libro(book_id)
                    self._refresh_books_table()
                    self.view.show_message(
                        "Éxito", 
                        "Libro eliminado correctamente", 
                        'info'
                    )
                except Exception as e:
                    self.view.show_message(
                        "Error", 
                        f"No se pudo eliminar el libro: {str(e)}", 
                        'error'
                    )
        else:
            self.view.show_message(
                "Advertencia", 
                "Por favor selecciona un libro primero", 
                'warning'
            )
    
    def generate_report(self):
        """Genera un informe para el libro seleccionado"""
        book_id = self.view.get_selected_book_id()
        if book_id:
            book = self.informe_model.generar_informe_lectura(book_id)
            self.view.show_book_details(book)
        else:
            self.view.show_message(
                "Advertencia", 
                "Por favor selecciona un libro primero", 
                'warning'
            )
    
    def export_to_csv(self):
        """Exporta los libros a un archivo CSV"""
        try:
            # Obtener filtros actuales
            filters = self.view.get_filters()
            
            # Pedir ubicación para guardar
            default_name = f"lecturas_{datetime.now().strftime('%Y%m%d')}.csv"
            file_path = self.view.get_save_path(default_name)
            
            if file_path:
                success = self.libro_model.exportar_a_csv(file_path, filters)
                if success:
                    self.view.show_message(
                        "Éxito", 
                        f"Libros exportados correctamente a {file_path}", 
                        'info'
                    )
                else:
                    self.view.show_message(
                        "Advertencia", 
                        "No hay libros para exportar con los filtros actuales", 
                        'warning'
                    )
        except Exception as e:
            self.view.show_message(
                "Error", 
                f"No se pudo exportar los libros: {str(e)}", 
                'error'
            )
    
    def show_stats(self):
        """Muestra las estadísticas de lectura"""
        stats = self.libro_model.obtener_estadisticas()
        self.view.show_stats(stats)
    
    def edit_user(self):
        """Abre el diálogo para editar los datos del usuario"""
        user_data = self.usuario_model.obtener_usuario()
        self.view.show_user_edit_dialog(user_data)
    
    def update_user(self, user_data: Dict):
        """Actualiza los datos del usuario"""
        try:
            # Validar campos obligatorios
            if not user_data.get('nombre'):
                self.view.show_message(
                    "Error", 
                    "El nombre es obligatorio", 
                    'error'
                )
                return
            
            # Actualizar usuario
            current_data = self.usuario_model.obtener_usuario()
            updated_data = {**current_data, **user_data}
            self.usuario_model.actualizar_usuario(updated_data)
            
            # Actualizar la vista
            self.view.update_user_info(updated_data)
            
            self.view.show_message(
                "Éxito", 
                "Perfil actualizado correctamente", 
                'info'
            )
        except Exception as e:
            self.view.show_message(
                "Error", 
                f"No se pudo actualizar el perfil: {str(e)}", 
                'error'
            )
    
    def show_help(self):
        """Muestra la ayuda de la aplicación"""
        help_text = """
        Registro de Lecturas - Ayuda
        
        1. Agregar Libros:
           - Completa el formulario en la sección "Agregar Nuevo Libro".
           - Los campos Título y Autor son obligatorios.
        
        2. Filtrar Libros:
           - Usa los filtros arriba de la tabla para buscar libros específicos.
           - Puedes filtrar por año, género y calificación.
        
        3. Acciones sobre Libros:
           - Haz clic derecho en un libro para ver opciones:
             * Ver Detalles: Muestra información completa del libro.
             * Editar Libro: Modifica los datos del libro.
             * Eliminar Libro: Borra el libro del registro.
             * Generar Informe: Crea un informe detallado.
        
        4. Exportar Datos:
           - Usa el botón "Exportar CSV" para guardar tus libros en un archivo.
        
        5. Estadísticas:
           - El botón "Estadísticas" muestra un resumen de tus lecturas.
        """
        
        self.view.show_message("Ayuda", help_text.strip(), 'info')

def run_app():
    """Función para iniciar la aplicación"""
    controller = MainController()

if __name__ == "__main__":
    run_app()