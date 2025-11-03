import flet as ft
import random
import time
from typing import Optional

# ===== CLASES DEL JUEGO (Backend) =====

class Ataque:
    def __init__(self, nombre, tipo, poder):
        self.nombre = nombre
        self.tipo = tipo
        self.poder = poder

class Pokemon:
    def __init__(self, nombre, tipo, hp_max, sprite_url=""):
        self.nombre = nombre
        self.tipo = tipo
        self.hp_max = hp_max
        self.hp_actual = hp_max
        self.ataques = []
        self.sprite_url = sprite_url
    
    def agregar_ataque(self, ataque):
        self.ataques.append(ataque)
    
    def esta_debilitado(self):
        return self.hp_actual <= 0
    
    def recibir_dano(self, cantidad):
        self.hp_actual -= cantidad
        if self.hp_actual < 0:
            self.hp_actual = 0
    
    def atacar(self, ataque, objetivo):
        dano_base = ataque.poder
        multiplicador = self._calcular_efectividad(ataque.tipo, objetivo.tipo)
        dano_total = int(dano_base * multiplicador)
        objetivo.recibir_dano(dano_total)
        return dano_total, multiplicador
    
    def _calcular_efectividad(self, tipo_ataque, tipo_defensor):
        ventajas = {
            "fuego": "planta",
            "planta": "electrico",
            "electrico": "fuego"
        }
        
        if tipo_ataque in ventajas and ventajas[tipo_ataque] == tipo_defensor:
            return 1.5
        if tipo_defensor in ventajas and ventajas[tipo_defensor] == tipo_ataque:
            return 0.75
        return 1.0

# Datos de Pokémon disponibles
POKEMON_DATA = {
    "Pikachu": {
        "tipo": "electrico",
        "hp": 100,
        "sprite_url": "https://raw.githubusercontent.com/PokeAPI/sprites/master/sprites/pokemon/25.png",
        "ataques": [
            ("Impactrueno", "electrico", 40),
            ("Rayo", "electrico", 55),
            ("Ataque Rápido", "normal", 30)
        ]
    },
    "Bulbasaur": {
        "tipo": "planta",
        "hp": 110,
        "sprite_url": "https://raw.githubusercontent.com/PokeAPI/sprites/master/sprites/pokemon/1.png",
        "ataques": [
            ("Látigo Cepa", "planta", 45),
            ("Hoja Afilada", "planta", 50),
            ("Placaje", "normal", 30)
        ]
    },
    "Charmander": {
        "tipo": "fuego",
        "hp": 105,
        "sprite_url": "https://raw.githubusercontent.com/PokeAPI/sprites/master/sprites/pokemon/4.png",
        "ataques": [
            ("Ascuas", "fuego", 40),
            ("Lanzallamas", "fuego", 55),
            ("Arañazo", "normal", 30)
        ]
    }
}

def crear_pokemon(nombre):
    """Crea una instancia de Pokémon a partir de los datos predefinidos."""
    if nombre not in POKEMON_DATA:
        raise ValueError(f"Pokémon desconocido: {nombre}")
    
    data = POKEMON_DATA[nombre]
    pokemon = Pokemon(nombre, data["tipo"], data["hp"], data["sprite_url"])
    
    # Agregar ataques
    for nombre_ataque, tipo, poder in data["ataques"]:
        pokemon.agregar_ataque(Ataque(nombre_ataque, tipo, poder))
    
    return pokemon

# ===== INTERFAZ GRÁFICA =====

class PokemonBatallaApp:
    def __init__(self, page: ft.Page):
        self.page = page
        self.page.title = "Batalla Pokémon"
        self.page.window_width = 800
        self.page.window_height = 600
        self.page.padding = 0
        
        self.jugador_pokemon: Optional[Pokemon] = None
        self.rival_pokemon: Optional[Pokemon] = None
        self.turno_jugador = True
        self.mensaje_batalla = ""
        
        self.mostrar_menu_principal()
    
    def get_color_tipo(self, tipo):
        colores = {
            "fuego": ft.Colors.RED_400,
            "planta": ft.Colors.GREEN_400,
            "electrico": ft.Colors.YELLOW_700,
            "normal": ft.Colors.GREY_400
        }
        return colores.get(tipo, ft.Colors.BLUE_400)
    
    def mostrar_menu_principal(self):
        self.page.clean()
        
        titulo = ft.Container(
            content=ft.Column([
                ft.Text("⚡ BATALLA POKÉMON ⚡", 
                       size=40, 
                       weight=ft.FontWeight.BOLD,
                       color=ft.Colors.YELLOW_400),
                ft.Text("Edición Flet - POO", 
                       size=20, 
                       color=ft.Colors.WHITE70),
            ], horizontal_alignment=ft.CrossAxisAlignment.CENTER),
            alignment=ft.alignment.center,
            padding=40
        )
        
        nombre_input = ft.TextField(
            label="Tu nombre",
            hint_text="Ash",
            width=300,
            text_align=ft.TextAlign.CENTER,
        )
        
        def iniciar_juego(e):
            nombre = nombre_input.value.strip() or "Ash"
            self.nombre_jugador = nombre
            self.mostrar_seleccion_pokemon()
        
        boton_iniciar = ft.ElevatedButton(
            "COMENZAR AVENTURA",
            on_click=iniciar_juego,
            width=300,
            height=50,
            style=ft.ButtonStyle(
                color=ft.Colors.WHITE,
                bgcolor=ft.Colors.GREEN_600,
            )
        )
        
        self.page.add(
            ft.Container(
                content=ft.Column([
                    titulo,
                    nombre_input,
                    ft.Container(height=20),
                    boton_iniciar,
                ], horizontal_alignment=ft.CrossAxisAlignment.CENTER),
                gradient=ft.LinearGradient(
                    begin=ft.alignment.top_center,
                    end=ft.alignment.bottom_center,
                    colors=[ft.Colors.BLUE_900, ft.Colors.BLUE_700]
                ),
                expand=True,
                alignment=ft.alignment.center
            )
        )
    
    def mostrar_seleccion_pokemon(self):
        self.page.clean()
        
        def crear_carta_pokemon(nombre_pokemon, numero):
            pokemon = crear_pokemon(nombre_pokemon)
            
            def seleccionar(e):
                self.jugador_pokemon = crear_pokemon(nombre_pokemon)
                self.elegir_rival()
                self.iniciar_batalla()
            
            return ft.Container(
                content=ft.Column([
                    ft.Image(src=pokemon.sprite_url, width=100, height=100),
                    ft.Text(pokemon.nombre, size=20, weight=ft.FontWeight.BOLD, color=ft.Colors.BLACK),
                    ft.Text(f"Tipo: {pokemon.tipo.upper()}", size=14, color=ft.Colors.BLACK),
                    ft.Text(f"HP: {pokemon.hp_max}", size=14, color=ft.Colors.BLACK),
                    ft.ElevatedButton(
                        "ELEGIR",
                        on_click=seleccionar,
                        bgcolor=self.get_color_tipo(pokemon.tipo),
                        color=ft.Colors.WHITE
                    )
                ], horizontal_alignment=ft.CrossAxisAlignment.CENTER, spacing=10),
                bgcolor=ft.Colors.WHITE,
                border_radius=15,
                padding=20,
                width=200,
                border=ft.border.all(3, self.get_color_tipo(pokemon.tipo))
            )
        
        self.page.add(
            ft.Container(
                content=ft.Column([
                    ft.Text("Elige tu Pokémon inicial", 
                           size=30, 
                           weight=ft.FontWeight.BOLD,
                           color=ft.Colors.WHITE),
                    ft.Container(height=30),
                    ft.Row([
                        crear_carta_pokemon("Pikachu", 1),
                        crear_carta_pokemon("Bulbasaur", 2),
                        crear_carta_pokemon("Charmander", 3),
                    ], alignment=ft.MainAxisAlignment.CENTER, spacing=20),
                ], horizontal_alignment=ft.CrossAxisAlignment.CENTER),
                gradient=ft.LinearGradient(
                    begin=ft.alignment.top_center,
                    end=ft.alignment.bottom_center,
                    colors=[ft.Colors.PURPLE_900, ft.Colors.PURPLE_700]
                ),
                expand=True,
                alignment=ft.alignment.center,
                padding=40
            )
        )
    
    def elegir_rival(self):
        # Elegir rival aleatoriamente (no basado en la elección del jugador)
        opciones = list(POKEMON_DATA.keys())
        # Opcional: evitar elegir exactamente la misma especie que el jugador
        try:
            nombre_jugador = self.jugador_pokemon.nombre
            candidatos = [n for n in opciones if n != nombre_jugador]
            if not candidatos:
                candidatos = opciones
        except Exception:
            candidatos = opciones
        
        self.rival_pokemon = crear_pokemon(random.choice(candidatos))
    
    def crear_barra_hp(self, pokemon):
        porcentaje = pokemon.hp_actual / pokemon.hp_max
        
        if porcentaje > 0.5:
            color = ft.Colors.GREEN
        elif porcentaje > 0.25:
            color = ft.Colors.YELLOW
        else:
            color = ft.Colors.RED
        
        # Barra externa (fondo) y barra interna (indicador)
        barra_interna = ft.Container(
            bgcolor=color,
            width=200 * porcentaje,
            height=20,
            border_radius=5,
        )

        barra_externa = ft.Container(
            content=ft.Row([barra_interna]),
            width=200,
            height=20,
            bgcolor=ft.Colors.GREY_800,
            border_radius=5,
        )

        # Guardamos la referencia a la barra interna para actualizarla después
        barra_externa.barra_interna = barra_interna
        return barra_externa
    
    def iniciar_batalla(self):
        self.page.clean()
        
        # Información del Pokémon rival (arriba)
        self.rival_nombre_text = ft.Text(
            f"{self.rival_pokemon.nombre}",
            size=20,
            weight=ft.FontWeight.BOLD,
            color=ft.Colors.WHITE
        )
        self.rival_hp_text = ft.Text(
            f"Lv. 42",
            size=16,
            color=ft.Colors.WHITE70
        )
        self.rival_hp_bar = self.crear_barra_hp(self.rival_pokemon)
        self.rival_hp_numero = ft.Text(
            f"{self.rival_pokemon.hp_actual}/{self.rival_pokemon.hp_max}",
            size=14,
            color=ft.Colors.WHITE
        )
        
        rival_info = ft.Container(
            content=ft.Column([
                ft.Row([self.rival_nombre_text, self.rival_hp_text], spacing=10),
                ft.Row([
                    ft.Text("HP", size=14, color=ft.Colors.WHITE),
                    self.rival_hp_bar,
                ], spacing=5),
                self.rival_hp_numero,
            ], spacing=5),
            bgcolor=ft.Colors.with_opacity(0.8, ft.Colors.BLACK),
            padding=15,
            border_radius=10,
            width=300,
        )
        
        # Sprite rival
        rival_sprite = ft.Image(
            src=self.rival_pokemon.sprite_url,
            width=150,
            height=150,
        )
        
        # Información del Pokémon jugador (abajo)
        self.jugador_nombre_text = ft.Text(
            f"{self.jugador_pokemon.nombre}",
            size=20,
            weight=ft.FontWeight.BOLD,
            color=ft.Colors.WHITE
        )
        self.jugador_hp_text = ft.Text(
            f"Lv. 42",
            size=16,
            color=ft.Colors.WHITE70
        )
        self.jugador_hp_bar = self.crear_barra_hp(self.jugador_pokemon)
        self.jugador_hp_numero = ft.Text(
            f"{self.jugador_pokemon.hp_actual}/{self.jugador_pokemon.hp_max}",
            size=14,
            color=ft.Colors.WHITE
        )
        
        jugador_info = ft.Container(
            content=ft.Column([
                ft.Row([self.jugador_nombre_text, self.jugador_hp_text], spacing=10),
                ft.Row([
                    ft.Text("HP", size=14, color=ft.Colors.WHITE),
                    self.jugador_hp_bar,
                ], spacing=5),
                self.jugador_hp_numero,
            ], spacing=5),
            bgcolor=ft.Colors.with_opacity(0.8, ft.Colors.BLACK),
            padding=15,
            border_radius=10,
            width=300,
        )
        
        # Sprite jugador
        jugador_sprite = ft.Image(
            src=self.jugador_pokemon.sprite_url,
            width=150,
            height=150,
        )
        
        # Mensaje de batalla
        self.mensaje_text = ft.Text(
            f"¿Qué hará {self.jugador_pokemon.nombre}?",
            size=20,
            color=ft.Colors.WHITE,
            weight=ft.FontWeight.BOLD,
        )
        
        mensaje_box = ft.Container(
            content=self.mensaje_text,
            bgcolor=ft.Colors.with_opacity(0.95, ft.Colors.BLACK),
            # Asegurar texto legible
            padding=22,
            border_radius=10,
            width=420,
            height=100,
        )
        
        # Botones de ataque
        botones_ataque = []
        for ataque in self.jugador_pokemon.ataques:
            btn = ft.ElevatedButton(
                f"{ataque.nombre}\n({ataque.tipo} - {ataque.poder})",
                on_click=lambda e, a=ataque: self.ejecutar_ataque(a),
                width=180,
                height=80,
                bgcolor=self.get_color_tipo(ataque.tipo),
                color=ft.Colors.WHITE,
            )
            botones_ataque.append(btn)
        # Guardar referencia a los botones para habilitar/deshabilitar sin cambiar layout
        self.botones_ataque = botones_ataque
        
        # Mantener siempre el mismo contenedor; solo deshabilitaremos botones durante animaciones
        self.botones_container = ft.Container(
            content=ft.Column([
                ft.Row([botones_ataque[0], botones_ataque[1]], spacing=10),
                ft.Row([botones_ataque[2]], spacing=10) if len(botones_ataque) > 2 else ft.Container(),
            ], spacing=10),
            visible=True
        )
        
        # Layout principal
        campo_batalla = ft.Stack([
            # Fondo
            ft.Container(
                gradient=ft.LinearGradient(
                    begin=ft.alignment.top_center,
                    end=ft.alignment.bottom_center,
                    colors=[ft.Colors.CYAN_300, ft.Colors.GREEN_300]
                ),
                expand=True,
            ),
            
            # Rival (arriba derecha)
            ft.Container(
                content=rival_sprite,
                top=40,
                right=80,
            ),
            ft.Container(
                content=rival_info,
                top=30,
                right=200,
            ),
            
            # Jugador (abajo izquierda)
            ft.Container(
                content=jugador_sprite,
                bottom=140,
                left=80,
            ),
            ft.Container(
                content=jugador_info,
                bottom=120,
                left=200,
            ),
        ])
        
        menu_batalla = ft.Container(
            content=ft.Column([
                mensaje_box,
                ft.Container(height=10),
                self.botones_container,
            ], horizontal_alignment=ft.CrossAxisAlignment.CENTER),
            bgcolor=ft.Colors.with_opacity(0.9, ft.Colors.BLACK),
            padding=20,
            border_radius=ft.border_radius.only(top_left=15, top_right=15),
        )
        
        self.page.add(
            ft.Column([
                ft.Container(content=campo_batalla, expand=True),
                menu_batalla,
            ], spacing=0, expand=True)
        )
    
    def ejecutar_ataque(self, ataque):
        # Deshabilitar botones (sin cambiar el layout)
        for b in getattr(self, 'botones_ataque', []):
            b.disabled = True
        self.page.update()
        
        # Ataque del jugador
        dano, efectividad = self.jugador_pokemon.atacar(ataque, self.rival_pokemon)
        
        mensaje = f"¡{self.jugador_pokemon.nombre} usa {ataque.nombre}!"
        if efectividad > 1.0:
            mensaje += " ¡Es súper efectivo!"
        elif efectividad < 1.0:
            mensaje += " No es muy efectivo..."
        
        self.mensaje_text.value = mensaje
        self.actualizar_barras_hp()
        self.page.update()
        
        time.sleep(2)
        
        # Verificar si el rival fue derrotado
        if self.rival_pokemon.esta_debilitado():
            self.fin_batalla(True)
            return
        
        # Ataque del rival
        ataque_rival = random.choice(self.rival_pokemon.ataques)
        dano_rival, efectividad_rival = self.rival_pokemon.atacar(ataque_rival, self.jugador_pokemon)
        
        mensaje_rival = f"¡{self.rival_pokemon.nombre} usa {ataque_rival.nombre}!"
        if efectividad_rival > 1.0:
            mensaje_rival += " ¡Es súper efectivo!"
        elif efectividad_rival < 1.0:
            mensaje_rival += " No es muy efectivo..."
        
        self.mensaje_text.value = mensaje_rival
        self.actualizar_barras_hp()
        self.page.update()
        
        time.sleep(2)
        
        # Verificar si el jugador fue derrotado
        if self.jugador_pokemon.esta_debilitado():
            self.fin_batalla(False)
            return
        
        # Restaurar menú y habilitar botones
        self.mensaje_text.value = f"¿Qué hará {self.jugador_pokemon.nombre}?"
        for b in getattr(self, 'botones_ataque', []):
            b.disabled = False
        self.page.update()
    
    def actualizar_barras_hp(self):
        # Actualizar barra del jugador
        try:
            porcentaje_j = self.jugador_pokemon.hp_actual / self.jugador_pokemon.hp_max
        except Exception:
            porcentaje_j = 0
        if hasattr(self.jugador_hp_bar, 'barra_interna'):
            self.jugador_hp_bar.barra_interna.width = 200 * porcentaje_j
        else:
            # fallback: reemplazar
            self.jugador_hp_bar = self.crear_barra_hp(self.jugador_pokemon)
        self.jugador_hp_numero.value = f"{self.jugador_pokemon.hp_actual}/{self.jugador_pokemon.hp_max}"

        # Actualizar barra del rival
        try:
            porcentaje_r = self.rival_pokemon.hp_actual / self.rival_pokemon.hp_max
        except Exception:
            porcentaje_r = 0
        if hasattr(self.rival_hp_bar, 'barra_interna'):
            self.rival_hp_bar.barra_interna.width = 200 * porcentaje_r
        else:
            self.rival_hp_bar = self.crear_barra_hp(self.rival_pokemon)
        self.rival_hp_numero.value = f"{self.rival_pokemon.hp_actual}/{self.rival_pokemon.hp_max}"
    
    def fin_batalla(self, victoria):
        self.page.clean()
        
        if victoria:
            titulo = "🏆 ¡VICTORIA! 🏆"
            mensaje = f"¡Has derrotado a {self.rival_pokemon.nombre}!"
            color_fondo = ft.Colors.GREEN_700
        else:
            titulo = "💔 DERROTA 💔"
            mensaje = f"{self.jugador_pokemon.nombre} fue derrotado..."
            color_fondo = ft.Colors.RED_700
        
        def jugar_de_nuevo(e):
            self.mostrar_menu_principal()
        
        self.page.add(
            ft.Container(
                content=ft.Column([
                    ft.Text(titulo, size=50, weight=ft.FontWeight.BOLD, color=ft.Colors.WHITE),
                    ft.Container(height=20),
                    ft.Text(mensaje, size=25, color=ft.Colors.WHITE70),
                    ft.Container(height=40),
                    ft.ElevatedButton(
                        "JUGAR DE NUEVO",
                        on_click=jugar_de_nuevo,
                        width=250,
                        height=50,
                        bgcolor=ft.Colors.BLUE_600,
                        color=ft.Colors.WHITE
                    ),
                ], horizontal_alignment=ft.CrossAxisAlignment.CENTER),
                gradient=ft.LinearGradient(
                    begin=ft.alignment.top_center,
                    end=ft.alignment.bottom_center,
                    colors=[color_fondo, ft.Colors.BLACK]
                ),
                expand=True,
                alignment=ft.alignment.center
            )
        )

def main(page: ft.Page):
    PokemonBatallaApp(page)

ft.app(target=main)