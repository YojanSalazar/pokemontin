import random
import time
import os

try:
    from colorama import init, Fore, Style
    init(autoreset=True)  
    COLORES_DISPONIBLES = True
except ImportError:
    print("Consejo: Instala 'colorama' para ver el juego con colores (pip install colorama)")
    COLORES_DISPONIBLES = False
    class Fore:
        RED = GREEN = YELLOW = BLUE = CYAN = MAGENTA = WHITE = RESET = ""
    class Style:
        BRIGHT = RESET_ALL = ""


class Ataque:
    
    def __init__(self, nombre, tipo, poder):
        self.__nombre = nombre  
        self.__tipo = tipo
        self.__poder = poder
    
    def get_nombre(self):
        return self.__nombre
    
    def get_tipo(self):
        return self.__tipo
    
    def get_poder(self):
        return self.__poder
    
    def __str__(self):
        return f"{self.__nombre} (Tipo: {self.__tipo}, Poder: {self.__poder})"

class Pokemon:

    def __init__(self, nombre, tipo, hp_max):
        self.__nombre = nombre
        self.__tipo = tipo
        self.__hp_max = hp_max
        self.__hp_actual = hp_max  
        self.__ataques = []  
    
    def get_nombre(self):
        return self.__nombre
    
    def get_tipo(self):
        return self.__tipo
    
    def get_hp_actual(self):
        return self.__hp_actual
    
    def get_hp_max(self):
        return self.__hp_max
    
    def get_ataques(self):
        return self.__ataques
    
    def agregar_ataque(self, ataque):
        self.__ataques.append(ataque)
    
    def esta_debilitado(self):
        return self.__hp_actual <= 0
    
    def recibir_dano(self, cantidad):
        self.__hp_actual -= cantidad
        if self.__hp_actual < 0:
            self.__hp_actual = 0  
    
    def atacar(self, ataque, objetivo):
        dano_base = ataque.get_poder()

        multiplicador = self.__calcular_efectividad(ataque.get_tipo(), objetivo.get_tipo())

        dano_total = int(dano_base * multiplicador)
        
        objetivo.recibir_dano(dano_total)

        self.__mostrar_mensaje_ataque(ataque, objetivo, dano_total, multiplicador)
        
        return dano_total
    
    def __calcular_efectividad(self, tipo_ataque, tipo_defensor):

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
    
    def __mostrar_mensaje_ataque(self, ataque, objetivo, dano, multiplicador):
        color = self.__get_color_tipo()
        
        print(f"\n{color}💥 ¡{self.__nombre} usa {ataque.get_nombre()}!{Style.RESET_ALL}")
        time.sleep(0.5)
        
        if multiplicador > 1.0:
            print(f"{Fore.GREEN}⚡ ¡Es súper efectivo!{Style.RESET_ALL}")
        elif multiplicador < 1.0:
            print(f"{Fore.RED}🛡️ No es muy efectivo...{Style.RESET_ALL}")
        
        print(f"💔 Hace {dano} puntos de daño a {objetivo.get_nombre()}")
        time.sleep(0.8)
    
    def __get_color_tipo(self):
        if not COLORES_DISPONIBLES:
            return ""
        
        colores = {
            "fuego": Fore.RED,
            "planta": Fore.GREEN,
            "electrico": Fore.YELLOW,
            "normal": Fore.WHITE
        }
        return colores.get(self.__tipo, Fore.WHITE)
    
    def mostrar_estado(self):
        color = self.__get_color_tipo()
        barra_vida = self.__generar_barra_vida()
        print(f"{color}{self.__nombre}{Style.RESET_ALL} {barra_vida} {self.__hp_actual}/{self.__hp_max} HP")
    
    def __generar_barra_vida(self):
        porcentaje = self.__hp_actual / self.__hp_max
        total_bloques = 20
        bloques_llenos = int(porcentaje * total_bloques)
        
        if porcentaje > 0.5:
            color_barra = Fore.GREEN
        elif porcentaje > 0.25:
            color_barra = Fore.YELLOW
        else:
            color_barra = Fore.RED
        
        barra = "█" * bloques_llenos + "░" * (total_bloques - bloques_llenos)
        return f"{color_barra}[{barra}]{Style.RESET_ALL}"

class Pikachu(Pokemon):
  
    def __init__(self):
        super().__init__("Pikachu", "electrico", 100)       
        self.agregar_ataque(Ataque("Impactrueno", "electrico", 40))
        self.agregar_ataque(Ataque("Rayo", "electrico", 55))
        self.agregar_ataque(Ataque("Ataque Rápido", "normal", 30))


class Bulbasaur(Pokemon):
    
    def __init__(self):
        super().__init__("Bulbasaur", "planta", 110)      
        self.agregar_ataque(Ataque("Látigo Cepa", "planta", 45))
        self.agregar_ataque(Ataque("Hoja Afilada", "planta", 50))
        self.agregar_ataque(Ataque("Placaje", "normal", 30))


class Charmander(Pokemon):
    
    def __init__(self):
        super().__init__("Charmander", "fuego", 105)       
        self.agregar_ataque(Ataque("Ascuas", "fuego", 40))
        self.agregar_ataque(Ataque("Lanzallamas", "fuego", 55))
        self.agregar_ataque(Ataque("Arañazo", "normal", 30))


class Entrenador:
 
    def __init__(self, nombre, pokemon, es_ia=False):
        self.__nombre = nombre
        self.__pokemon = pokemon
        self.__es_ia = es_ia
    
    def get_nombre(self):
        return self.__nombre
    
    def get_pokemon(self):
        return self.__pokemon
    
    def es_inteligencia_artificial(self):
        return self.__es_ia
    
    def elegir_ataque(self):
        ataques_disponibles = self.__pokemon.get_ataques()
        
        if self.__es_ia:
            return random.choice(ataques_disponibles)
        else:
            return self.__mostrar_menu_ataques(ataques_disponibles)
    
    def __mostrar_menu_ataques(self, ataques):
        while True:
            print(f"\n{Fore.CYAN}╔══════════════════════════════════════╗")
            print(f"║  ⚔️  ELIGE TU ATAQUE  ⚔️              ║")
            print(f"╚══════════════════════════════════════╝{Style.RESET_ALL}")
            
            for i, ataque in enumerate(ataques, 1):
                print(f"  {i}. {ataque}")
            
            try:
                eleccion = int(input(f"\n{Fore.YELLOW}Elige un ataque (1-{len(ataques)}): {Style.RESET_ALL}"))
                
                if 1 <= eleccion <= len(ataques):
                    return ataques[eleccion - 1]
                else:
                    print(f"{Fore.RED}❌ Opción inválida. Intenta de nuevo.{Style.RESET_ALL}")
            except ValueError:
                print(f"{Fore.RED}❌ Por favor ingresa un número.{Style.RESET_ALL}")


class Batalla:

    def _init_(self, jugador, rival):
        self.__jugador = jugador
        self.__rival = rival
        self.__turno = 1
    
    def iniciar(self):
        self.__mostrar_introduccion()
        
        while not self.__hay_ganador():
            self.__ejecutar_turno()
            self.__turno += 1
        
        self.__mostrar_resultado()
    
    def __mostrar_introduccion(self):
        limpiar_consola()
        print(f"{Fore.MAGENTA}{'='*50}")
        print(f"{'🎮 ¡COMIENZA LA BATALLA POKÉMON! 🎮'.center(50)}")
        print(f"{'='*50}{Style.RESET_ALL}\n")
        
        print(f"{Fore.CYAN}⚔️  {self._jugador.get_nombre()} envía a {self._jugador.get_pokemon().get_nombre()}!")
        print(f"⚔️  {self._rival.get_nombre()} envía a {self._rival.get_pokemon().get_nombre()}!{Style.RESET_ALL}\n")
        
        input(f"{Fore.YELLOW}Presiona ENTER para comenzar...{Style.RESET_ALL}")
    
    def __ejecutar_turno(self):
        limpiar_consola()
        print(f"{Fore.MAGENTA}═══════════════ TURNO {self.__turno} ═══════════════{Style.RESET_ALL}\n")
        print(f"{Fore.CYAN}TU POKÉMON:{Style.RESET_ALL}")
        self.__jugador.get_pokemon().mostrar_estado()
        print(f"\n{Fore.RED}POKÉMON RIVAL:{Style.RESET_ALL}")
        self.__rival.get_pokemon().mostrar_estado()
        print()
        
        ataque_jugador = self.__jugador.elegir_ataque()
        self._jugador.get_pokemon().atacar(ataque_jugador, self._rival.get_pokemon())
        
        if self.__rival.get_pokemon().esta_debilitado():
            return
        
        input(f"\n{Fore.YELLOW}Presiona ENTER para continuar...{Style.RESET_ALL}")
        print(f"\n{Fore.RED}--- Turno del rival ---{Style.RESET_ALL}")
        time.sleep(1)
        
        ataque_rival = self.__rival.elegir_ataque()
        self._rival.get_pokemon().atacar(ataque_rival, self._jugador.get_pokemon())
        
        input(f"\n{Fore.YELLOW}Presiona ENTER para el siguiente turno...{Style.RESET_ALL}")
    
    def __hay_ganador(self):
        return (self.__jugador.get_pokemon().esta_debilitado() or 
                self.__rival.get_pokemon().esta_debilitado())
    
    def __mostrar_resultado(self):
        limpiar_consola()
        
        if self.__jugador.get_pokemon().esta_debilitado():
            print(f"{Fore.RED}{'='*50}")
            print(f"{'💔 HAS PERDIDO LA BATALLA 💔'.center(50)}")
            print(f"{'='*50}{Style.RESET_ALL}\n")
            print(f"{self.__jugador.get_pokemon().get_nombre()} se ha debilitado...")
            print(f"¡{self.__rival.get_nombre()} es el ganador!")
        else:
            print(f"{Fore.GREEN}{'='*50}")
            print(f"{'🏆 ¡HAS GANADO LA BATALLA! 🏆'.center(50)}")
            print(f"{'='*50}{Style.RESET_ALL}\n")
            print(f"{self.__rival.get_pokemon().get_nombre()} se ha debilitado...")
            print(f"¡{self.__jugador.get_nombre()}, eres el ganador!")



def limpiar_consola():
    os.system('cls' if os.name == 'nt' else 'clear')


def mostrar_titulo():
    limpiar_consola()
    print(f"{Fore.YELLOW}{Style.BRIGHT}")
    print("  ╔═══════════════════════════════════════════════╗")
    print("  ║                                               ║")
    print("  ║        ⚡ BATALLA POKÉMON ⚡                  ║")
    print("  ║        Edición Consola - POO                  ║")
    print("  ║                                               ║")
    print("  ╚═══════════════════════════════════════════════╝")
    print(f"{Style.RESET_ALL}\n")


def elegir_pokemon_inicial():

    print(f"{Fore.CYAN}Elige tu Pokémon inicial:{Style.RESET_ALL}\n")
    
    opciones = {
        1: Pikachu(),
        2: Bulbasaur(),
        3: Charmander()
    }
    
    print(f"  {Fore.YELLOW}1. ⚡ Pikachu (Tipo: Eléctrico){Style.RESET_ALL}")
    print(f"     HP: 100 | Ataques: Impactrueno, Rayo, Ataque Rápido\n")
    
    print(f"  {Fore.GREEN}2. 🌿 Bulbasaur (Tipo: Planta){Style.RESET_ALL}")
    print(f"     HP: 110 | Ataques: Látigo Cepa, Hoja Afilada, Placaje\n")
    
    print(f"  {Fore.RED}3. 🔥 Charmander (Tipo: Fuego){Style.RESET_ALL}")
    print(f"     HP: 105 | Ataques: Ascuas, Lanzallamas, Arañazo\n")
    
    while True:
        try:
            eleccion = int(input(f"{Fore.YELLOW}Elige tu Pokémon (1-3): {Style.RESET_ALL}"))
            
            if eleccion in opciones:
                pokemon_elegido = opciones[eleccion]
                print(f"\n{Fore.GREEN}✓ ¡Has elegido a {pokemon_elegido.get_nombre()}!{Style.RESET_ALL}")
                time.sleep(1)
                return pokemon_elegido
            else:
                print(f"{Fore.RED}❌ Opción inválida. Elige 1, 2 o 3.{Style.RESET_ALL}")
        except ValueError:
            print(f"{Fore.RED}❌ Por favor ingresa un número.{Style.RESET_ALL}")


def elegir_pokemon_rival(pokemon_jugador):

    tipo_jugador = pokemon_jugador.get_tipo()
    
    if tipo_jugador == "electrico":
        return Bulbasaur()  
    elif tipo_jugador == "planta":
        return Charmander()  
    else:  
        return Pikachu()  


def preguntar_jugar_de_nuevo():

    print(f"\n{Fore.CYAN}{'─'*50}{Style.RESET_ALL}")
    respuesta = input(f"\n{Fore.YELLOW}¿Quieres jugar de nuevo? (s/n): {Style.RESET_ALL}").lower()
    return respuesta in ['s', 'si', 'sí', 'y', 'yes']



def main():
    
    while True:
        mostrar_titulo()
        
        nombre_jugador = input(f"{Fore.CYAN}Ingresa tu nombre: {Style.RESET_ALL}").strip()
        if not nombre_jugador:
            nombre_jugador = "Ash"
        
        print(f"\n{Fore.GREEN}¡Bienvenido, {nombre_jugador}!{Style.RESET_ALL}\n")
        time.sleep(1)
        
        pokemon_jugador = elegir_pokemon_inicial()
        
        pokemon_rival = elegir_pokemon_rival(pokemon_jugador)
        
        print(f"\n{Fore.RED}Tu rival ha elegido a {pokemon_rival.get_nombre()}!{Style.RESET_ALL}")
        time.sleep(2)
        
        jugador = Entrenador(nombre_jugador, pokemon_jugador, es_ia=False)
        rival = Entrenador("Entrenador Rival", pokemon_rival, es_ia=True)
        
        batalla = Batalla(jugador, rival)
        batalla.iniciar()
        
        if not preguntar_jugar_de_nuevo():
            limpiar_consola()
            print(f"\n{Fore.YELLOW}{'='*50}")
            print(f"{'¡Gracias por jugar! 👋'.center(50)}")
            print(f"{'='*50}{Style.RESET_ALL}\n")
            break


if _name_ == "_main_":
    main()