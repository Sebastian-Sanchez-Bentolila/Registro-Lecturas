#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Registro de Lecturas - modelo.py

Autor: Sebastian Sanchez Bentolila
Email: sebastiansb3004@gmail.com
Versión: 1.0.0
Última modificación: 29/07/2025
Licencia: MIT
Copyright: © 2025 - Todos los derechos reservados

Descripción:
- Gestiona toda la interacción con la base de datos
- Define las estructuras de datos principales
- Maneja la lógica de persistencia


Dependencias:
- Python 3.13.3
- Módulos estándar: sqlite3, json, typing, os, datetime
"""

import sqlite3
import json
import os
from datetime import datetime
from typing import List, Dict, Optional, Tuple

class DatabaseManager:
    """Clase para manejar la conexión y operaciones con la base de datos SQLite"""
    
    def __init__(self, db_name: str = 'db\\lecturas.db'):
        self.db_name = db_name
        self._initialize_database()
        
    def _initialize_database(self):
        """Inicializa la base de datos con las tablas necesarias"""
        with self._get_connection() as conn:
            cursor = conn.cursor()
            
            # Tabla de libros
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS libros (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    titulo TEXT NOT NULL,
                    autor TEXT NOT NULL,
                    genero TEXT NOT NULL,
                    subgenero TEXT,
                    anio_lectura INTEGER,
                    fecha_lectura DATE,
                    calificacion REAL,
                    paginas INTEGER,
                    editorial TEXT,
                    comentario TEXT,
                    fecha_creacion TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    fecha_actualizacion TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                )
            ''')
            
            # Tabla de usuario
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS usuario (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    nombre TEXT NOT NULL,
                    email TEXT,
                    avatar TEXT,
                    preferencias TEXT,
                    fecha_creacion TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    fecha_actualizacion TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                )
            ''')
            
            # Insertar usuario por defecto si no existe
            cursor.execute('SELECT COUNT(*) FROM usuario')
            if cursor.fetchone()[0] == 0:
                cursor.execute('''
                    INSERT INTO usuario (nombre, email, avatar, preferencias)
                    VALUES (?, ?, ?, ?)
                ''', ('Lector', 'lector@example.com', 'default_avatar.png', '{}'))
            
            conn.commit()
    
    def _get_connection(self):
        """Retorna una conexión a la base de datos"""
        return sqlite3.connect(self.db_name)
    
    def execute_query(self, query: str, params: Tuple = (), fetch: bool = False):
        """Ejecuta una consulta SQL y opcionalmente retorna resultados"""
        with self._get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute(query, params)
            if fetch:
                return cursor.fetchall()
            conn.commit()

class LibroModel:
    """Modelo para manejar los libros en la base de datos"""
    
    def __init__(self, db_manager: DatabaseManager):
        self.db = db_manager
    
    def crear_libro(self, libro_data: Dict) -> int:
        """Crea un nuevo libro y retorna su ID"""
        query = '''
            INSERT INTO libros (
                titulo, autor, genero, subgenero, anio_lectura, 
                fecha_lectura, calificacion, paginas, editorial, comentario
            )
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        '''
        params = (
            libro_data['titulo'],
            libro_data['autor'],
            libro_data['genero'],
            libro_data.get('subgenero', ''),
            libro_data.get('anio_lectura', datetime.now().year),
            libro_data.get('fecha_lectura', datetime.now().date().isoformat()),
            libro_data.get('calificacion', 0),
            libro_data.get('paginas', 0),
            libro_data.get('editorial', ''),
            libro_data.get('comentario', '')
        )
        
        with self.db._get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute(query, params)
            libro_id = cursor.lastrowid
            conn.commit()
        
        return libro_id
    
    def obtener_libros(self, filtros: Optional[Dict] = None) -> List[Dict]:
        """Obtiene todos los libros con filtros opcionales"""
        base_query = 'SELECT * FROM libros'
        params = []
        
        if filtros:
            conditions = []
            for key, value in filtros.items():
                if key == 'anio_lectura':
                    conditions.append(f'anio_lectura = ?')
                    params.append(value)
                elif key == 'genero':
                    conditions.append(f'genero = ?')
                    params.append(value)
                elif key == 'calificacion_min':
                    conditions.append(f'calificacion >= ?')
                    params.append(value)
                elif key == 'calificacion_max':
                    conditions.append(f'calificacion <= ?')
                    params.append(value)
                elif key == 'search':
                    conditions.append(f'(titulo LIKE ? OR autor LIKE ?)')
                    params.append(f'%{value}%')
                    params.append(f'%{value}%')
            
            if conditions:
                base_query += ' WHERE ' + ' AND '.join(conditions)
        
        base_query += ' ORDER BY fecha_lectura DESC'
        
        libros = self.db.execute_query(base_query, tuple(params), fetch=True)
        
        # Convertir a lista de diccionarios
        column_names = [
            'id', 'titulo', 'autor', 'genero', 'subgenero', 'anio_lectura',
            'fecha_lectura', 'calificacion', 'paginas', 'editorial',
            'comentario', 'fecha_creacion', 'fecha_actualizacion'
        ]
        
        return [dict(zip(column_names, libro)) for libro in libros]
    
    def actualizar_libro(self, libro_id: int, libro_data: Dict) -> bool:
        """Actualiza un libro existente"""
        query = '''
            UPDATE libros SET
                titulo = ?,
                autor = ?,
                genero = ?,
                subgenero = ?,
                anio_lectura = ?,
                fecha_lectura = ?,
                calificacion = ?,
                paginas = ?,
                editorial = ?,
                comentario = ?,
                fecha_actualizacion = CURRENT_TIMESTAMP
            WHERE id = ?
        '''
        params = (
            libro_data['titulo'],
            libro_data['autor'],
            libro_data['genero'],
            libro_data.get('subgenero', ''),
            libro_data.get('anio_lectura', datetime.now().year),
            libro_data.get('fecha_lectura', datetime.now().date().isoformat()),
            libro_data.get('calificacion', 0),
            libro_data.get('paginas', 0),
            libro_data.get('editorial', ''),
            libro_data.get('comentario', ''),
            libro_id
        )
        
        self.db.execute_query(query, params)
        return True
    
    def eliminar_libro(self, libro_id: int) -> bool:
        """Elimina un libro por su ID"""
        query = 'DELETE FROM libros WHERE id = ?'
        self.db.execute_query(query, (libro_id,))
        return True
    
    def obtener_estadisticas(self) -> Dict:
        """Retorna estadísticas sobre los libros leídos"""
        stats = {}
        
        # Total de libros
        query = 'SELECT COUNT(*) FROM libros'
        stats['total_libros'] = self.db.execute_query(query, fetch=True)[0][0]
        
        # Libros por año
        query = '''
            SELECT anio_lectura, COUNT(*) as count 
            FROM libros 
            GROUP BY anio_lectura 
            ORDER BY anio_lectura DESC
        '''
        stats['libros_por_anio'] = self.db.execute_query(query, fetch=True)
        
        # Promedio de calificación
        query = 'SELECT AVG(calificacion) FROM libros'
        stats['promedio_calificacion'] = self.db.execute_query(query, fetch=True)[0][0] or 0
        
        # Géneros más leídos
        query = '''
            SELECT genero, COUNT(*) as count 
            FROM libros 
            GROUP BY genero 
            ORDER BY count DESC 
            LIMIT 5
        '''
        stats['generos_populares'] = self.db.execute_query(query, fetch=True)
        
        return stats
    
    def exportar_a_csv(self, file_path: str, filtros: Optional[Dict] = None) -> bool:
        """Exporta los libros a un archivo CSV"""
        libros = self.obtener_libros(filtros)
        if not libros:
            return False
        
        import csv
        
        with open(file_path, 'w', newline='', encoding='utf-8') as csvfile:
            fieldnames = libros[0].keys()
            writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
            
            writer.writeheader()
            writer.writerows(libros)
        
        return True

class UsuarioModel:
    """Modelo para manejar los datos del usuario"""
    
    def __init__(self, db_manager: DatabaseManager):
        self.db = db_manager
    
    def obtener_usuario(self) -> Dict:
        """Obtiene los datos del usuario"""
        query = 'SELECT * FROM usuario LIMIT 1'
        usuario = self.db.execute_query(query, fetch=True)[0]
        
        column_names = [
            'id', 'nombre', 'email', 'avatar', 'preferencias',
            'fecha_creacion', 'fecha_actualizacion'
        ]
        
        usuario_dict = dict(zip(column_names, usuario))
        usuario_dict['preferencias'] = json.loads(usuario_dict['preferencias'])
        
        return usuario_dict
    
    def actualizar_usuario(self, usuario_data: Dict) -> bool:
        """Actualiza los datos del usuario"""
        query = '''
            UPDATE usuario SET
                nombre = ?,
                email = ?,
                avatar = ?,
                preferencias = ?,
                fecha_actualizacion = CURRENT_TIMESTAMP
            WHERE id = ?
        '''
        params = (
            usuario_data['nombre'],
            usuario_data['email'],
            usuario_data.get('avatar', 'default_avatar.png'),
            json.dumps(usuario_data.get('preferencias', {})),
            usuario_data['id']
        )
        
        self.db.execute_query(query, params)
        return True

class InformeModel:
    """Modelo para generar informes de lectura"""
    
    def __init__(self, db_manager: DatabaseManager):
        self.db = db_manager
        self.libro_model = LibroModel(db_manager)
    
    def generar_informe_lectura(self, libro_id: int) -> Dict:
        """Genera un informe detallado para un libro específico"""
        query = 'SELECT * FROM libros WHERE id = ?'
        libro = self.db.execute_query(query, (libro_id,), fetch=True)
        
        if not libro:
            return {}
        
        column_names = [
            'id', 'titulo', 'autor', 'genero', 'subgenero', 'anio_lectura',
            'fecha_lectura', 'calificacion', 'paginas', 'editorial',
            'comentario', 'fecha_creacion', 'fecha_actualizacion'
        ]
        
        libro_dict = dict(zip(column_names, libro[0]))
        
        # Agregar estadísticas adicionales
        stats = self.libro_model.obtener_estadisticas()
        libro_dict['total_libros_leidos'] = stats['total_libros']
        libro_dict['promedio_calificacion_global'] = stats['promedio_calificacion']
        
        return libro_dict

# Inicialización del modelo
db_manager = DatabaseManager()
libro_model = LibroModel(db_manager)
usuario_model = UsuarioModel(db_manager)
informe_model = InformeModel(db_manager)