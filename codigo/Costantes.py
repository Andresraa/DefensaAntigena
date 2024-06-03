# Dimensiones
FILAS = 15   # Número de filas del juego
COLUMNAS = 15  # Número de columnas del juego
TAMAÑO_CASILLA = 48  # Tamaño de cada casilla en píxeles
# Dimensiones de la pantalla
ANCHO_PANTALLA = TAMAÑO_CASILLA * COLUMNAS  # Ancho total de la pantalla del juego en píxeles
ALTO_PANTALLA = TAMAÑO_CASILLA * FILAS  # Alto total de la pantalla del juego en píxeles
# Panel lateral
PANEL_LATERAL = 300  # Ancho del panel lateral en píxeles
# Configuración del juego
FPS = 60  # Cuadros por segundo, frecuencia de actualización del juego
VIDA = 100  # Salud inicial del jugador
DINERO = 650  # Dinero inicial del jugador Depende tammbien de como quieras ponerle
NIVELES_TOTALES = 15  # Número total de niveles en el juego
# Constantes de los enemigos
TIEMPO_ENTRE_APARICIONES = 400  # Tiempo de espera entre la aparición de enemigos en milisegundos

# Constantes de las torretas
NIVELES_TORRETA = 4  # Número de niveles de mejora de las torretas ( Actualmente 4)  Mas ?
COSTO_COMPRA = 200  # Costo de compra de una torreta
COSTO_MEJORA = 100  # Costo de mejorar una torreta
RECOMPENSA_POR_MATAR = 1  # Recompensa en dinero por matar a un enemigo
RECOMPENSA_POR_NIVEL_COMPLETADO = 100  # Recompensa en dinero por completar un nivel

# Constantes de animación
PASOS_ANIMACION = 8  # Número de pasos en la animación de las torretas
DELAY_ANIMACION = 15  # Retardo en la animación de las torretas en milisegundos

# Constantes de daño
DANO = 5  # Daño que inflige una torreta a un enemigo
