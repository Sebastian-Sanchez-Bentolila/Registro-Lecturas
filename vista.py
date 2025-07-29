#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Registro de Lecturas - vista.py

Autor: Sebastian Sanchez Bentolila
Email: sebastiansb3004@gmail.com
Versión: 1.0.0
Última modificación: 29/07/2025
Licencia: MIT
Copyright: © 2025 - Todos los derechos reservados

Descripción:
- Implementa la interfaz gráfica con Tkinter
- Maneja todos los componentes visuales
- Recibe interacciones del usuario


Dependencias:
- Python 3.13.3
- Módulos estándar: tkinter, typing, os, datetime
"""

import tkinter as tk
from tkinter import ttk, messagebox, filedialog, PhotoImage
from datetime import datetime
from typing import Optional, Dict, List, Callable
import os

class StyleConfig:
    """Configuración de estilos para la aplicación"""
    
    def __init__(self):
        # Paleta de colores pastel literarios
        self.colors = {
            'primary': '#F8B195',    # Rosa pastel
            'secondary': '#F67280',   # Rosa coral
            'accent': '#C06C84',     # Lila
            'background': '#F5E6CA',  # Beige claro
            'card': '#FFF5E1',       # Beige muy claro
            'text': '#4A4A4A',        # Gris oscuro
            'success': '#A8E6CF',     # Verde pastel
            'info': '#DCE2F1',        # Azul pastel
            'warning': '#FFD3B6',     # Naranja pastel
            'danger': '#FFAAA5'      # Rojo pastel
        }
        
        # Fuentes
        self.fonts = {
            'title': ('Helvetica', 16, 'bold'),
            'subtitle': ('Helvetica', 12, 'bold'),
            'body': ('Helvetica', 10),
            'small': ('Helvetica', 8)
        }
        
    def configure_styles(self):
        """Configura los estilos de los widgets"""
        style = ttk.Style()
        
        # Configurar el tema general
        style.theme_create('literario', parent='clam', settings={
            'TFrame': {
                'configure': {'background': self.colors['background']}
            },
            'TLabel': {
                'configure': {
                    'background': self.colors['background'],
                    'foreground': self.colors['text'],
                    'font': self.fonts['body']
                }
            },
            'TButton': {
                'configure': {
                    'background': self.colors['primary'],
                    'foreground': self.colors['text'],
                    'font': self.fonts['body'],
                    'borderwidth': 1,
                    'relief': 'raised',
                    'padding': 5
                },
                'map': {
                    'background': [
                        ('active', self.colors['secondary']),
                        ('pressed', self.colors['accent'])
                    ]
                }
            },
            'TEntry': {
                'configure': {
                    'fieldbackground': 'white',
                    'foreground': self.colors['text'],
                    'font': self.fonts['body'],
                    'padding': 5
                }
            },
            'TCombobox': {
                'configure': {
                    'fieldbackground': 'white',
                    'foreground': self.colors['text'],
                    'font': self.fonts['body'],
                    'padding': 5
                }
            },
            'Treeview': {
                'configure': {
                    'background': 'white',
                    'fieldbackground': 'white',
                    'foreground': self.colors['text'],
                    'font': self.fonts['small']
                },
                'map': {
                    'background': [('selected', self.colors['info'])],
                    'foreground': [('selected', self.colors['text'])]
                }
            },
            'Treeview.Heading': {
                'configure': {
                    'background': self.colors['accent'],
                    'foreground': 'white',
                    'font': self.fonts['small']
                }
            }
        })
        
        style.theme_use('literario')

class MainView(tk.Tk):
    """Vista principal de la aplicación"""
    
    def __init__(self, controller):
        super().__init__()
        self.controller = controller
        self.style = StyleConfig()
        self.style.configure_styles()
        
        self.title("Registro de Lecturas")
        self.geometry("1200x700")
        self.minsize(800, 600)
        
        # Configurar icono (asumiendo que tienes un archivo logo.ico)
        try:
            self.iconbitmap('src\\logo.ico')
        except:
            pass
        
        self._create_widgets()
        self._layout()
        
    def _create_widgets(self):
        """Crea todos los widgets de la interfaz"""
        # Frame principal
        self.main_frame = ttk.Frame(self)
        
        # Sección 1: Logo y título
        self.logo_frame = ttk.Frame(self.main_frame)
        self.logo_label = ttk.Label(self.logo_frame, text="📚", font=('Helvetica', 24))
        self.title_label = ttk.Label(
            self.logo_frame, 
            text="Mi Registro de Lecturas", 
            font=self.style.fonts['title']
        )
        
        # Sección 2: Nuevos libros (formulario)
        self.new_book_frame = ttk.LabelFrame(
            self.main_frame, 
            text="Agregar Nuevo Libro",
            padding=(10, 5)
        )
        
        self._create_book_form()
        
        # Sección 3: Tabla de libros con filtros
        self.books_frame = ttk.LabelFrame(
            self.main_frame, 
            text="Mis Libros Leídos",
            padding=(10, 5)
        )
        
        self._create_books_table()
        
        # Sección 4: Panel de usuario y acciones
        self.user_frame = ttk.Frame(self.main_frame, style='Card.TFrame')
        self._create_user_panel()
        
    def _create_book_form(self):
        """Crea el formulario para agregar nuevos libros"""
        # Campos del formulario
        fields = [
            ('titulo', 'Título:', 'entry'),
            ('autor', 'Autor:', 'entry'),
            ('genero', 'Género:', 'combobox'),
            ('subgenero', 'Subgénero:', 'entry'),
            ('anio_lectura', 'Año de lectura:', 'entry'),
            ('calificacion', 'Calificación (1-5):', 'spinbox'),
            ('paginas', 'Páginas:', 'entry'),
            ('editorial', 'Editorial:', 'entry'),
            ('comentario', 'Comentario:', 'text')
        ]
        
        self.form_vars = {}
        self.form_widgets = {}
        
        for i, (field, label, widget_type) in enumerate(fields):
            # Crear etiqueta
            lbl = ttk.Label(self.new_book_frame, text=label)
            lbl.grid(row=i, column=0, padx=5, pady=2, sticky='e')
            
            # Crear widget según el tipo
            if widget_type == 'entry':
                var = tk.StringVar()
                entry = ttk.Entry(self.new_book_frame, textvariable=var)
                entry.grid(row=i, column=1, padx=5, pady=2, sticky='we')
                self.form_widgets[field] = entry
                self.form_vars[field] = var
                
            elif widget_type == 'combobox':
                var = tk.StringVar()
                genres = [
                    # Ficción General
                    'Novela', 'Cuento', 'Microrrelato', 'Realismo Mágico', 'Fábula',
                    
                    # Ficción Específica
                    'Ciencia Ficción', 'Fantasía', 'Terror', 'Distopía', 'Ucronía',
                    'Romance', 'Romance Histórico', 'Romance Contemporáneo', 'Policial',
                    'Thriller', 'Suspenso', 'Misterio', 'Aventura', 'Western',
                    
                    # No Ficción
                    'Biografía', 'Autobiografía', 'Memorias', 'Diario', 'Ensayo',
                    'Periodismo', 'Crónica', 'Reportaje', 'Historia', 'Arte',
                    'Filosofía', 'Psicología', 'Sociología', 'Política',
                    
                    # Desarrollo Personal
                    'Autoayuda', 'Crecimiento Personal', 'Productividad', 'Motivación',
                    'Finanzas Personales', 'Liderazgo', 'Emprendimiento',
                    
                    # Educativos
                    'Educación', 'Pedagogía', 'Didáctica', 'Referencia', 'Diccionario',
                    'Enciclopedia', 'Manual', 'Guía',
                    
                    # Arte y Creatividad
                    'Poesía', 'Teatro', 'Guión', 'Cómic', 'Novela Gráfica', 'Manga',
                    'Arte', 'Fotografía', 'Diseño', 'Arquitectura',
                    
                    # Infantil/Juvenil
                    'Infantil', 'Juvenil', 'Young Adult', 'Middle Grade',
                    
                    # Especializados
                    'Ciencia', 'Tecnología', 'Medicina', 'Derecho', 'Economía',
                    'Negocios', 'Marketing', 'Cocina', 'Viajes', 'Deportes',
                    'Ecología', 'Espiritualidad', 'Religión', 'Esoterismo',
                    
                    # Otros
                    'Humor', 'Sátira', 'Erótico', 'Fanfiction', 'Experimental',
                    'Otro'
                ]
                combo = ttk.Combobox(
                    self.new_book_frame, 
                    textvariable=var, 
                    values=genres,
                    state='readonly'
                )
                combo.grid(row=i, column=1, padx=5, pady=2, sticky='we')
                self.form_widgets[field] = combo
                self.form_vars[field] = var
                
            elif widget_type == 'spinbox':
                var = tk.DoubleVar()
                spin = tk.Spinbox(
                    self.new_book_frame, 
                    from_=1, 
                    to=5, 
                    increment=0.5,
                    textvariable=var,
                    width=5
                )
                spin.grid(row=i, column=1, padx=5, pady=2, sticky='w')
                self.form_widgets[field] = spin
                self.form_vars[field] = var
                
            elif widget_type == 'text':
                var = tk.StringVar()
                text = tk.Text(self.new_book_frame, height=4, width=30)
                scroll = ttk.Scrollbar(self.new_book_frame, orient='vertical', command=text.yview)
                text.configure(yscrollcommand=scroll.set)
                text.grid(row=i, column=1, padx=5, pady=2, sticky='we')
                scroll.grid(row=i, column=2, sticky='ns')
                self.form_widgets[field] = text
                self.form_vars[field] = var
        
        # Botón de agregar
        self.add_btn = ttk.Button(
            self.new_book_frame, 
            text="Agregar Libro", 
            command=self.controller.add_book
        )
        self.add_btn.grid(row=len(fields), column=1, pady=10, sticky='e')
        
        # Configurar peso de columnas
        self.new_book_frame.columnconfigure(1, weight=1)
        
    def _create_books_table(self):
        """Crea la tabla de libros con filtros"""
        # Frame para filtros
        self.filters_frame = ttk.Frame(self.books_frame)
        self.filters_frame.pack(fill='x', pady=(0, 10))
        
        # Filtros
        ttk.Label(self.filters_frame, text="Filtrar por:").grid(row=0, column=0, padx=5)
        
        # Filtro por año
        self.year_var = tk.StringVar()
        ttk.Label(self.filters_frame, text="Año:").grid(row=0, column=1, padx=5)
        self.year_combo = ttk.Combobox(
            self.filters_frame, 
            textvariable=self.year_var,
            width=8,
            state='readonly'
        )
        self.year_combo.grid(row=0, column=2, padx=5)
        
        # Filtro por género
        self.genre_var = tk.StringVar()
        ttk.Label(self.filters_frame, text="Género:").grid(row=0, column=3, padx=5)
        self.genre_combo = ttk.Combobox(
            self.filters_frame, 
            textvariable=self.genre_var,
            width=15,
            state='readonly'
        )
        self.genre_combo.grid(row=0, column=4, padx=5)
        
        # Filtro por calificación
        self.rating_var = tk.StringVar()
        ttk.Label(self.filters_frame, text="Calificación mín:").grid(row=0, column=5, padx=5)
        self.rating_combo = ttk.Combobox(
            self.filters_frame, 
            textvariable=self.rating_var,
            values=['1', '2', '3', '4', '5'],
            width=3,
            state='readonly'
        )
        self.rating_combo.grid(row=0, column=6, padx=5)
        
        # Botón de filtrar
        self.filter_btn = ttk.Button(
            self.filters_frame, 
            text="Aplicar Filtros", 
            command=self.controller.filter_books,
            width=15
        )
        self.filter_btn.grid(row=0, column=7, padx=5)
        
        # Botón de limpiar filtros
        self.clear_filter_btn = ttk.Button(
            self.filters_frame, 
            text="Limpiar Filtros", 
            command=self.controller.clear_filters,
            width=15
        )
        self.clear_filter_btn.grid(row=0, column=8, padx=5)
        
        # Configurar peso de columnas
        self.filters_frame.columnconfigure(0, weight=1)
        
        # Tabla de libros
        columns = [
            'id', 'titulo', 'autor', 'genero', 'subgenero', 
            'anio_lectura', 'calificacion', 'paginas', 'editorial'
        ]
        
        self.books_table = ttk.Treeview(
            self.books_frame,
            columns=columns,
            show='headings',
            selectmode='browse',
            height=15
        )
        
        # Configurar columnas
        column_config = {
            'id': {'text': 'ID', 'width': 40, 'anchor': 'center'},
            'titulo': {'text': 'Título', 'width': 150},
            'autor': {'text': 'Autor', 'width': 120},
            'genero': {'text': 'Género', 'width': 100},
            'subgenero': {'text': 'Subgénero', 'width': 100},
            'anio_lectura': {'text': 'Año', 'width': 50, 'anchor': 'center'},
            'calificacion': {'text': 'Calif.', 'width': 60, 'anchor': 'center'},
            'paginas': {'text': 'Págs.', 'width': 50, 'anchor': 'center'},
            'editorial': {'text': 'Editorial', 'width': 100}
        }
        
        for col in columns:
            self.books_table.heading(col, text=column_config[col]['text'])
            self.books_table.column(col, width=column_config[col]['width'], 
                                 anchor=column_config[col].get('anchor', 'w'))
        
        # Scrollbar
        scrollbar = ttk.Scrollbar(
            self.books_frame, 
            orient='vertical', 
            command=self.books_table.yview
        )
        self.books_table.configure(yscrollcommand=scrollbar.set)
        
        # Empaquetar tabla y scrollbar
        self.books_table.pack(side='left', fill='both', expand=True)
        scrollbar.pack(side='right', fill='y')
        
        # Context menu para la tabla
        self.table_menu = tk.Menu(self, tearoff=0)
        self.table_menu.add_command(
            label="Ver Detalles", 
            command=self.controller.show_book_details
        )
        self.table_menu.add_command(
            label="Editar Libro", 
            command=self.controller.edit_book
        )
        self.table_menu.add_command(
            label="Eliminar Libro", 
            command=self.controller.delete_book
        )
        self.table_menu.add_separator()
        self.table_menu.add_command(
            label="Generar Informe", 
            command=self.controller.generate_report
        )
        
        # Bindear evento de clic derecho
        self.books_table.bind('<Button-3>', self._show_table_menu)
        
    def _create_user_panel(self):
        """Crea el panel de usuario con acciones"""
        # Frame para la foto y datos de usuario
        self.user_info_frame = ttk.Frame(self.user_frame)
        self.user_info_frame.pack(fill='x', pady=10)
        
        # Foto de usuario (placeholder)
        self.user_photo = tk.Label(
            self.user_info_frame, 
            text="👤", 
            font=('Helvetica', 24),
            background=self.style.colors['card']
        )
        self.user_photo.pack(side='left', padx=10)
        
        # Datos de usuario
        self.user_data_frame = ttk.Frame(self.user_info_frame)
        self.user_data_frame.pack(side='left', fill='x', expand=True)
        
        self.user_name = ttk.Label(
            self.user_data_frame, 
            text="Nombre Usuario",
            font=self.style.fonts['subtitle']
        )
        self.user_name.pack(anchor='w')
        
        self.user_email = ttk.Label(
            self.user_data_frame, 
            text="usuario@example.com",
            font=self.style.fonts['small']
        )
        self.user_email.pack(anchor='w')
        
        # Botón de editar usuario
        self.edit_user_btn = ttk.Button(
            self.user_info_frame, 
            text="✏️", 
            width=2,
            command=self.controller.edit_user
        )
        self.edit_user_btn.pack(side='right', padx=10)
        
        # Separador
        ttk.Separator(self.user_frame).pack(fill='x', pady=5)
        
        # Acciones rápidas
        actions_frame = ttk.Frame(self.user_frame)
        actions_frame.pack(fill='x', pady=10)
        
        action_buttons = [
            ("📊 Estadísticas", self.controller.show_stats),
            ("📝 Generar Informe", self.controller.generate_report),
            ("📤 Exportar CSV", self.controller.export_to_csv),
            ("❓ Ayuda", self.controller.show_help)
        ]
        
        for text, command in action_buttons:
            btn = ttk.Button(
                actions_frame, 
                text=text,
                command=command
            )
            btn.pack(side='left', padx=5, fill='x', expand=True)
        
    def _show_table_menu(self, event):
        """Muestra el menú contextual de la tabla"""
        item = self.books_table.identify_row(event.y)
        if item:
            self.books_table.selection_set(item)
            self.table_menu.post(event.x_root, event.y_root)
    
    def _layout(self):
        """Organiza los widgets en la ventana principal"""
        # Configurar grid principal
        self.main_frame.pack(fill='both', expand=True, padx=10, pady=10)
        
        # Sección 1: Logo y título (fila 0)
        self.logo_frame.grid(row=0, column=0, columnspan=2, pady=(0, 20))
        self.logo_label.pack(side='left', padx=10)
        self.title_label.pack(side='left')
        
        # Sección 2: Nuevos libros (fila 1, columna 0)
        self.new_book_frame.grid(row=1, column=0, sticky='nsew', padx=(0, 10))
        
        # Sección 3: Tabla de libros (fila 1, columna 1)
        self.books_frame.grid(row=1, column=1, sticky='nsew')
        
        # Sección 4: Panel de usuario (fila 2, columnas 0-1)
        self.user_frame.grid(row=2, column=0, columnspan=2, sticky='ew', pady=(20, 0))
        
        # Configurar pesos de filas y columnas
        self.main_frame.columnconfigure(0, weight=1)
        self.main_frame.columnconfigure(1, weight=3)
        self.main_frame.rowconfigure(1, weight=1)
        
    def get_form_data(self) -> Dict:
        """Obtiene los datos del formulario"""
        data = {}
        for field, var in self.form_vars.items():
            if field == 'comentario':
                # Manejar el widget Text de manera especial
                data[field] = self.form_widgets[field].get("1.0", tk.END).strip()
            else:
                data[field] = var.get()
        return data
    
    def clear_form(self):
        """Limpia el formulario"""
        for field, var in self.form_vars.items():
            if field == 'comentario':
                self.form_widgets[field].delete("1.0", tk.END)
            else:
                var.set('')
        
        # Establecer valores por defecto
        self.form_vars['anio_lectura'].set(datetime.now().year)
        self.form_vars['calificacion'].set(3.0)
    
    def populate_books_table(self, books: List[Dict]):
        """Llena la tabla con los libros"""
        # Limpiar tabla
        for item in self.books_table.get_children():
            self.books_table.delete(item)
        
        # Agregar libros
        for book in books:
            values = [book.get(col, '') for col in self.books_table['columns']]
            self.books_table.insert('', 'end', values=values)
    
    def populate_filters(self, years: List[int], genres: List[str]):
        """Llena los combobox de filtros"""
        self.year_combo['values'] = ['Todos'] + sorted(years, reverse=True)
        self.year_combo.current(0)
        
        self.genre_combo['values'] = ['Todos'] + sorted(genres)
        self.genre_combo.current(0)
        
        self.rating_combo['values'] = ['Todas'] + [str(i) for i in range(1, 6)]
        self.rating_combo.current(0)
    
    def get_selected_book_id(self) -> Optional[int]:
        """Obtiene el ID del libro seleccionado en la tabla"""
        selection = self.books_table.selection()
        if selection:
            item = self.books_table.item(selection[0])
            return int(item['values'][0])  # ID es la primera columna
        return None
    
    def get_filters(self) -> Dict:
        """Obtiene los filtros seleccionados"""
        filters = {}
        
        year = self.year_var.get()
        if year and year != 'Todos':
            filters['anio_lectura'] = int(year)
        
        genre = self.genre_var.get()
        if genre and genre != 'Todos':
            filters['genero'] = genre
        
        rating = self.rating_var.get()
        if rating and rating != 'Todas':
            filters['calificacion_min'] = int(rating)
        
        return filters
    
    def show_book_details(self, book: Dict):
        """Muestra los detalles de un libro en una ventana emergente"""
        detail_window = tk.Toplevel(self)
        detail_window.title(f"Detalles: {book.get('titulo', '')}")
        detail_window.geometry("500x400")
        
        # Frame principal
        frame = ttk.Frame(detail_window, padding=10)
        frame.pack(fill='both', expand=True)
        
        # Título
        ttk.Label(
            frame, 
            text=book.get('titulo', ''), 
            font=self.style.fonts['title']
        ).pack(pady=(0, 10))
        
        # Autor
        ttk.Label(
            frame, 
            text=f"Autor: {book.get('autor', '')}",
            font=self.style.fonts['subtitle']
        ).pack(anchor='w')
        
        # Géneros
        genres = f"{book.get('genero', '')}"
        if book.get('subgenero'):
            genres += f" / {book.get('subgenero', '')}"
        ttk.Label(frame, text=f"Género: {genres}").pack(anchor='w')
        
        # Detalles
        details_frame = ttk.Frame(frame)
        details_frame.pack(fill='x', pady=10)
        
        ttk.Label(details_frame, text=f"Año: {book.get('anio_lectura', '')}").grid(row=0, column=0, sticky='w')
        ttk.Label(details_frame, text=f"Páginas: {book.get('paginas', '')}").grid(row=0, column=1, sticky='w', padx=10)
        ttk.Label(details_frame, text=f"Editorial: {book.get('editorial', '')}").grid(row=0, column=2, sticky='w')
        
        ttk.Label(details_frame, text=f"Calificación: {book.get('calificacion', '')}/5").grid(row=1, column=0, sticky='w', pady=(5, 0))
        
        # Comentario
        ttk.Label(frame, text="Comentario:", font=self.style.fonts['subtitle']).pack(anchor='w', pady=(10, 0))
        
        comment_text = tk.Text(
            frame, 
            height=8, 
            wrap='word',
            bg='white',
            padx=5,
            pady=5
        )
        comment_text.insert('1.0', book.get('comentario', ''))
        comment_text.config(state='disabled')
        comment_text.pack(fill='both', expand=True)
        
        # Botón de cerrar
        ttk.Button(
            frame, 
            text="Cerrar", 
            command=detail_window.destroy
        ).pack(pady=(10, 0))
    
    def show_user_edit_dialog(self, user_data: Dict):
        """Muestra el diálogo para editar los datos del usuario"""
        dialog = tk.Toplevel(self)
        dialog.title("Editar Perfil")
        dialog.geometry("400x300")
        
        # Frame principal
        frame = ttk.Frame(dialog, padding=10)
        frame.pack(fill='both', expand=True)
        
        # Campos del formulario
        ttk.Label(frame, text="Nombre:").grid(row=0, column=0, sticky='e', pady=5)
        name_var = tk.StringVar(value=user_data.get('nombre', ''))
        name_entry = ttk.Entry(frame, textvariable=name_var)
        name_entry.grid(row=0, column=1, sticky='we', pady=5)
        
        ttk.Label(frame, text="Email:").grid(row=1, column=0, sticky='e', pady=5)
        email_var = tk.StringVar(value=user_data.get('email', ''))
        email_entry = ttk.Entry(frame, textvariable=email_var)
        email_entry.grid(row=1, column=1, sticky='we', pady=5)
        
        # Botones
        btn_frame = ttk.Frame(frame)
        btn_frame.grid(row=2, column=0, columnspan=2, pady=10)
        
        ttk.Button(
            btn_frame, 
            text="Guardar", 
            command=lambda: self.controller.update_user({
                'nombre': name_var.get(),
                'email': email_var.get()
            })
        ).pack(side='left', padx=5)
        
        ttk.Button(
            btn_frame, 
            text="Cancelar", 
            command=dialog.destroy
        ).pack(side='left', padx=5)
        
        # Configurar peso de columnas
        frame.columnconfigure(1, weight=1)
    
    def show_book_edit_dialog(self, book_data: Dict):
        """Muestra el diálogo para editar un libro"""
        dialog = tk.Toplevel(self)
        dialog.title(f"Editar: {book_data.get('titulo', '')}")
        dialog.geometry("500x600")
        
        # Frame principal
        frame = ttk.Frame(dialog, padding=10)
        frame.pack(fill='both', expand=True)
        
        # Campos del formulario
        fields = [
            ('titulo', 'Título:', book_data.get('titulo', '')),
            ('autor', 'Autor:', book_data.get('autor', '')),
            ('genero', 'Género:', book_data.get('genero', '')),
            ('subgenero', 'Subgénero:', book_data.get('subgenero', '')),
            ('anio_lectura', 'Año de lectura:', book_data.get('anio_lectura', datetime.now().year)),
            ('calificacion', 'Calificación (1-5):', book_data.get('calificacion', 3)),
            ('paginas', 'Páginas:', book_data.get('paginas', '')),
            ('editorial', 'Editorial:', book_data.get('editorial', '')),
            ('comentario', 'Comentario:', book_data.get('comentario', ''))
        ]
        
        self.edit_vars = {}
        
        for i, (field, label, value) in enumerate(fields):
            # Crear etiqueta
            ttk.Label(frame, text=label).grid(row=i, column=0, padx=5, pady=2, sticky='e')
            
            # Crear widget según el tipo
            if field == 'genero':
                var = tk.StringVar(value=value)
                genres = [
                    # Ficción General
                    'Novela', 'Cuento', 'Microrrelato', 'Realismo Mágico', 'Fábula',
                    
                    # Ficción Específica
                    'Ciencia Ficción', 'Fantasía', 'Terror', 'Distopía', 'Ucronía',
                    'Romance', 'Romance Histórico', 'Romance Contemporáneo', 'Policial',
                    'Thriller', 'Suspenso', 'Misterio', 'Aventura', 'Western',
                    
                    # No Ficción
                    'Biografía', 'Autobiografía', 'Memorias', 'Diario', 'Ensayo',
                    'Periodismo', 'Crónica', 'Reportaje', 'Historia', 'Arte',
                    'Filosofía', 'Psicología', 'Sociología', 'Política',
                    
                    # Desarrollo Personal
                    'Autoayuda', 'Crecimiento Personal', 'Productividad', 'Motivación',
                    'Finanzas Personales', 'Liderazgo', 'Emprendimiento',
                    
                    # Educativos
                    'Educación', 'Pedagogía', 'Didáctica', 'Referencia', 'Diccionario',
                    'Enciclopedia', 'Manual', 'Guía',
                    
                    # Arte y Creatividad
                    'Poesía', 'Teatro', 'Guión', 'Cómic', 'Novela Gráfica', 'Manga',
                    'Arte', 'Fotografía', 'Diseño', 'Arquitectura',
                    
                    # Infantil/Juvenil
                    'Infantil', 'Juvenil', 'Young Adult', 'Middle Grade',
                    
                    # Especializados
                    'Ciencia', 'Tecnología', 'Medicina', 'Derecho', 'Economía',
                    'Negocios', 'Marketing', 'Cocina', 'Viajes', 'Deportes',
                    'Ecología', 'Espiritualidad', 'Religión', 'Esoterismo',
                    
                    # Otros
                    'Humor', 'Sátira', 'Erótico', 'Fanfiction', 'Experimental',
                    'Otro'
                ]
                combo = ttk.Combobox(
                    frame, 
                    textvariable=var, 
                    values=genres,
                    state='readonly'
                )
                combo.grid(row=i, column=1, padx=5, pady=2, sticky='we')
                self.edit_vars[field] = var
                
            elif field == 'calificacion':
                var = tk.DoubleVar(value=value)
                spin = tk.Spinbox(
                    frame, 
                    from_=1, 
                    to=5, 
                    increment=0.5,
                    textvariable=var,
                    width=5
                )
                spin.grid(row=i, column=1, padx=5, pady=2, sticky='w')
                self.edit_vars[field] = var
                
            elif field == 'comentario':
                text = tk.Text(frame, height=8, width=30)
                text.insert('1.0', value)
                scroll = ttk.Scrollbar(frame, orient='vertical', command=text.yview)
                text.configure(yscrollcommand=scroll.set)
                text.grid(row=i, column=1, padx=5, pady=2, sticky='we')
                scroll.grid(row=i, column=2, sticky='ns')
                self.edit_vars[field] = text
                
            else:
                var = tk.StringVar(value=str(value) if value is not None else '')
                entry = ttk.Entry(frame, textvariable=var)
                entry.grid(row=i, column=1, padx=5, pady=2, sticky='we')
                self.edit_vars[field] = var
        
        # Botones
        btn_frame = ttk.Frame(frame)
        btn_frame.grid(row=len(fields), column=0, columnspan=2, pady=10)
        
        ttk.Button(
            btn_frame, 
            text="Guardar Cambios", 
            command=lambda: self._save_book_edit(book_data['id'], dialog)
        ).pack(side='left', padx=5)
        
        ttk.Button(
            btn_frame, 
            text="Cancelar", 
            command=dialog.destroy
        ).pack(side='left', padx=5)
        
        # Configurar peso de columnas
        frame.columnconfigure(1, weight=1)
    
    def _save_book_edit(self, book_id: int, dialog):
        """Recolecta los datos del diálogo de edición y los guarda"""
        data = {}
        for field, widget in self.edit_vars.items():
            if field == 'comentario':
                data[field] = widget.get("1.0", tk.END).strip()
            else:
                data[field] = widget.get()
        
        self.controller.update_book(book_id, data)
        dialog.destroy()
    
    def show_stats(self, stats: Dict):
        """Muestra las estadísticas en una ventana emergente"""
        stats_window = tk.Toplevel(self)
        stats_window.title("Estadísticas de Lectura")
        stats_window.geometry("500x400")
        
        # Frame principal
        frame = ttk.Frame(stats_window, padding=10)
        frame.pack(fill='both', expand=True)
        
        # Título
        ttk.Label(
            frame, 
            text="Estadísticas de Lectura", 
            font=self.style.fonts['title']
        ).pack(pady=(0, 10))
        
        # Total de libros
        ttk.Label(
            frame, 
            text=f"📚 Total de libros leídos: {stats.get('total_libros', 0)}",
            font=self.style.fonts['subtitle']
        ).pack(anchor='w', pady=5)
        
        # Libros por año
        ttk.Label(
            frame, 
            text="📅 Libros por año:",
            font=self.style.fonts['subtitle']
        ).pack(anchor='w', pady=(10, 0))
        
        books_per_year = stats.get('libros_por_anio', [])
        for year, count in books_per_year:
            ttk.Label(frame, text=f"  {year}: {count} libros").pack(anchor='w')
        
        # Promedio de calificación
        ttk.Label(
            frame, 
            text=f"⭐ Promedio de calificación: {stats.get('promedio_calificacion', 0):.1f}/5",
            font=self.style.fonts['subtitle']
        ).pack(anchor='w', pady=(10, 0))
        
        # Géneros más leídos
        ttk.Label(
            frame, 
            text="Géneros más leídos:",
            font=self.style.fonts['subtitle']
        ).pack(anchor='w', pady=(10, 0))
        
        popular_genres = stats.get('generos_populares', [])
        for genre, count in popular_genres:
            ttk.Label(frame, text=f"  {genre}: {count} libros").pack(anchor='w')
        
        # Botón de cerrar
        ttk.Button(
            frame, 
            text="Cerrar", 
            command=stats_window.destroy
        ).pack(pady=(20, 0))
    
    def show_message(self, title: str, message: str, type: str = 'info'):
        """Muestra un mensaje al usuario"""
        if type == 'info':
            messagebox.showinfo(title, message)
        elif type == 'warning':
            messagebox.showwarning(title, message)
        elif type == 'error':
            messagebox.showerror(title, message)
    
    def ask_confirmation(self, title: str, message: str) -> bool:
        """Pide confirmación al usuario"""
        return messagebox.askyesno(title, message)
    
    def get_save_path(self, default_name: str) -> Optional[str]:
        """Obtiene una ruta para guardar archivo"""
        return filedialog.asksaveasfilename(
            defaultextension='.csv',
            initialfile=default_name,
            filetypes=[('CSV Files', '*.csv')]
        )
    
    def update_user_info(self, user_data: Dict):
        """Actualiza la información del usuario en la interfaz"""
        self.user_name.config(text=user_data.get('nombre', ''))
        self.user_email.config(text=user_data.get('email', ''))
        
        # Actualizar foto si existe
        avatar = user_data.get('avatar', '')
        if avatar and os.path.exists(avatar):
            try:
                photo = PhotoImage(file=avatar)
                self.user_photo.config(image=photo)
                self.user_photo.image = photo  # Mantener referencia
            except:
                self.user_photo.config(text="👤")
        else:
            self.user_photo.config(text="👤")