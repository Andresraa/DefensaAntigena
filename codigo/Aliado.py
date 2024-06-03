import pygame as pg
import math
import constants as c
from turret_data import DATOS_DE_TORRETA

class Torreta(pg.sprite.Sprite):

    # Clase para representar una torreta en el juego.
    """
    Atributos:
        imagen (Surface): La imagen que representa la torreta.
        cassila_x (int): La posición X de la casilla donde se encuentra la torreta.
        cassila_y (int): La posición Y de la casilla donde se encuentra la torreta.
        x (float): La coordenada X del centro de la torreta en la pantalla.
        y (float): La coordenada Y del centro de la torreta en la pantalla.
        rect (Rect): El rectángulo que delimita la torreta en la pantalla.
    """

class Torreta(pg.sprite.Sprite):
    def __init__(self, hojas_sprites, posicion_x, posicion_y, efecto_disparo):
        pg.sprite.Sprite.__init__(self)
        self.nivel_mejora = 1
        self.rango = DATOS_DE_TORRETA[self.nivel_mejora - 1].get("rango")
        self.enfriamiento = DATOS_DE_TORRETA[self.nivel_mejora - 1].get("enfriamiento")
        self.ultimo_disparo = pg.time.get_ticks()
        self.seleccionada = False
        self.objetivo = None

        # Variables de posición
        self.posicion_x = posicion_x
        self.posicion_y = posicion_y
        # Calcula las coordenadas del centro
        self.x = (self.posicion_x + 0.5) * c.TAMAÑO_DE_CASILLA
        self.y = (self.posicion_y + 0.5) * c.TAMAÑO_DE_CASILLA
        # Efecto de sonido del disparo
        self.efecto_disparo = efecto_disparo

        # Variables de animación
        self.hojas_sprites = hojas_sprites
        self.lista_animaciones = self.cargar_imagenes(self.hojas_sprites[self.nivel_mejora - 1])
        self.indice_cuadro = 0
        self.tiempo_de_actualización = pg.time.get_ticks()

        # Actualizar imagen
        self.ángulo = 90
        self.imagen_original = self.lista_animaciones[self.indice_cuadro]
        self.imagen = pg.transform.rotate(self.imagen_original, self.ángulo)
        self.rectángulo = self.imagen.get_rect()
        self.rectángulo.center = (self.x, self.y)

        # Crear círculo transparente que muestra el rango
        self.imagen_rango = pg.Surface((self.rango * 2, self.rango * 2))
        self.imagen_rango.fill((0, 0, 0))
        self.imagen_rango.set_colorkey((0, 0, 0))
        pg.draw.circle(self.imagen_rango, "gris100", (self.rango, self.rango), self.rango)
        self.imagen_rango.set_alpha(100)
        self.rectángulo_rango = self.imagen_rango.get_rect()
        self.rectángulo_rango.center = self.rectángulo.center

    def cargar_imagenes(self, hoja_sprites):
        # Extrae las imágenes de la hoja de sprites
        tamaño = hoja_sprites.get_height()
        lista_animaciones = []
        for x in range(c.PASOS_DE_ANIMACIÓN):
            temp_img = hoja_sprites.subsurface(x * tamaño, 0, tamaño, tamaño)
            lista_animaciones.append(temp_img)
        return lista_animaciones

    def actualizar(self, grupo_enemigos, mundo):
        # Si se elige un objetivo, reproduce la animación de disparo
        if self.objetivo:
            self.reproducir_animación()
        else:
            # Busca un nuevo objetivo una vez que la torreta se haya enfriado
            if pg.time.get_ticks() - self.ultimo_disparo > (self.enfriamiento / mundo.velocidad_juego):
                self.elegir_objetivo(grupo_enemigos)

    def elegir_objetivo(self, grupo_enemigos):
        # Encuentra un enemigo a quien apuntar
        x_dist = 0
        y_dist = 0
        # Verifica la distancia a cada enemigo para ver si está dentro del rango
        for enemigo in grupo_enemigos:
            if enemigo.salud > 0:
                x_dist = enemigo.posicion[0] - self.x
                y_dist = enemigo.posicion[1] - self.y
                dist = math.sqrt(x_dist ** 2 + y_dist ** 2)
                if dist < self.rango:
                    self.objetivo = enemigo
                    self.ángulo = math.degrees(math.atan2(-y_dist, x_dist))
                    # Daña al enemigo
                    self.objetivo.salud -= c.DAÑO
                    # Reproduce el efecto de sonido
                    self.efecto_disparo.play()
                    break

    def reproducir_animación(self):
        # Actualiza la imagen
        self.imagen_original = self.lista_animaciones[self.indice_cuadro]
        # Verifica si ha pasado suficiente tiempo desde la última actualización
        if pg.time.get_ticks() - self.tiempo_de_actualización > c.DEMORA_DE_ANIMACIÓN:
            self.tiempo_de_actualización = pg.time.get_ticks()
            self.indice_cuadro += 1
            # Verifica si la animación ha terminado y vuelve al estado inactivo
            if self.indice_cuadro >= len(self.lista_animaciones):
                self.indice_cuadro = 0
                # Registra el tiempo completado y elimina el objetivo para que pueda comenzar el enfriamiento
                self.ultimo_disparo = pg.time.get_ticks()
                self.objetivo = None

    def mejorar(self):
        self.nivel_mejora += 1
        self.rango = DATOS_DE_TORRETA[self.nivel_mejora - 1].get("rango")
        self.enfriamiento = DATOS_DE_TORRETA[self.nivel_mejora - 1].get("enfriamiento")
        # Actualizar imagen de la torreta
        self.lista_animaciones = self.cargar_imagenes(self.hojas_sprites[self.nivel_mejora - 1])
        self.imagen_original = self.lista_animaciones[self.indice_cuadro]

        # Actualizar círculo de rango
        self.imagen_rango = pg.Surface((self.rango * 2, self.rango * 2))
        self.imagen_rango.fill((0, 0, 0))
        self.imagen_rango.set_colorkey((0, 0, 0))
        pg.draw.circle(self.imagen_rango, "gris100", (self.rango, self.rango), self.rango)
        self.imagen_rango.set_alpha(100)
        self.rectángulo_rango = self.imagen_rango.get_rect()
        self.rectángulo_rango.center = self.rectángulo.center

    def dibujar(self, superficie):
        self.imagen = pg.transform.rotate(self.imagen_original, self.ángulo - 90)
        self.rectángulo = self.imagen.get_rect()
        self.rectángulo.center = (self.x, self.y)
        superficie.blit(self.imagen, self.rectángulo)
        if self.seleccionada:
            superficie.blit(self.imagen_rango, self.rectángulo_rango)
