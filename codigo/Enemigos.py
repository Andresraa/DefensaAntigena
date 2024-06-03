import pygame as pg
from pygame.math import Vector2
import math
import constants as c
from enemy_data import ENEMY_DATA

class Enemigo(pg.sprite.Sprite):
    def __init__(self, tipo_enemigo, puntos_de_ruta, imagenes):
        """
        Inicializa un nuevo enemigo.

        Args:
            tipo_enemigo (str): El tipo de enemigo.
            puntos_de_ruta (list): Lista de puntos de ruta que el enemigo seguirá.
            imagenes (dict): Diccionario de imágenes para diferentes tipos de enemigos.
        """
        pg.sprite.Sprite.__init__(self)
        self.puntos_de_ruta = puntos_de_ruta
        self.posicion = Vector2(self.puntos_de_ruta[0])
        self.punto_destino = 1
        self.salud = ENEMY_DATA.get(tipo_enemigo)["salud"]
        self.velocidad = ENEMY_DATA.get(tipo_enemigo)["velocidad"]
        self.angulo = 0
        self.imagen_original = imagenes.get(tipo_enemigo)
        self.imagen = pg.transform.rotate(self.imagen_original, self.angulo)
        self.rectangulo = self.imagen.get_rect()
        self.rectangulo.center = self.posicion

    def actualizar(self, mundo):
        """
        Actualiza la posición y estado del enemigo en el mundo.

        Args:
            mundo (objeto): El objeto del mundo que contiene información del juego.
        """
        self.mover(mundo)
        self.rotar()
        self.verificar_vivo(mundo)

    def mover(self, mundo):
        """
        Mueve al enemigo hacia el siguiente punto de ruta.

        Args:
            mundo (objeto): El objeto del mundo que contiene información del juego.
        """
        # Define el siguiente punto de ruta
        if self.punto_destino < len(self.puntos_de_ruta):
            self.objetivo = Vector2(self.puntos_de_ruta[self.punto_destino])
            self.movimiento = self.objetivo - self.posicion
        else:
            # El enemigo ha llegado al final del camino
            self.kill()
            mundo.salud -= 1
            mundo.enemigos_perdidos += 1

        # Calcula la distancia al punto de destino
        distancia = self.movimiento.length()

        # Verifica si la distancia restante es mayor que la velocidad del enemigo
        if distancia >= (self.velocidad * mundo.velocidad_juego):
            self.posicion += self.movimiento.normalize() * (self.velocidad * mundo.velocidad_juego)
        else:
            if distancia != 0:
                self.posicion += self.movimiento.normalize() * distancia
            self.punto_destino += 1

    def rotar(self):
        """
        Rota la imagen del enemigo para que se alinee con su movimiento.
        """
        # Calcula la distancia al siguiente punto de ruta
        distancia = self.objetivo - self.posicion

        # Usa la distancia para calcular el ángulo
        self.angulo = math.degrees(math.atan2(-distancia[1], distancia[0]))

        # Rota la imagen y actualiza el rectángulo
        self.imagen = pg.transform.rotate(self.imagen_original, self.angulo)
        self.rectangulo = self.imagen.get_rect()
        self.rectangulo.center = self.posicion

    def verificar_vivo(self, mundo):
        """
        Verifica si el enemigo está vivo o no.

        Args:
            mundo (objeto): El objeto del mundo que contiene información del juego.
        """
        if self.salud <= 0:
            mundo.enemigos_abatidos += 1
            mundo.dinero += c.RECOMPENSA_ABATIR
            self.kill()
