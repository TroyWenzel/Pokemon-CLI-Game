# this file defines the pokemon class and handles pokemon data
# it manages pokemon stats, evolution, moves, and fetches data from the pokeapi

import random
import requests

class Pokemon:
    # ============================================================
    # represents a single pokemon with stats, level, and moves
    # each pokemon has:
    # - base stats (HP, attack, defense, speed) that scale with level
    # - a type (fire, water, grass, etc.)
    # - random moves chosen from their actual move pool based on level
    # - evolution possibilities (level-up or stone evolution)
    # ============================================================
    
    # evolution data for level-up evolutions
    # format: pokemon_id: (evolution_level, evolved_id)
    # example: 1: (16, 2) means Bulbasaur (1) evolves to Ivysaur (2) at level 16
    EVOLUTIONS = {
        1: (16, 2), 2: (32, 3),  # Bulbasaur line
        4: (16, 5), 5: (36, 6),  # Charmander line
        7: (16, 8), 8: (36, 9),  # Squirtle line
        10: (7, 11), 11: (10, 12),  # Caterpie line
        13: (7, 14), 14: (10, 15),  # Weedle line
        16: (18, 17), 17: (36, 18),  # Pidgey line
        19: (20, 20),  # Rattata
        21: (20, 22),  # Spearow
        23: (22, 24),  # Ekans
        25: (26, 26),  # Pikachu
        27: (22, 28),  # Sandshrew
        29: (16, 30),  # Nidoran F
        32: (16, 33),  # Nidoran M
        35: (36, 36),  # Clefairy
        37: (38, 38),  # Vulpix
        39: (40, 40),  # Jigglypuff
        41: (22, 42),  # Zubat
        43: (21, 44), 44: (45, 45),  # Oddish line
        46: (24, 47),  # Paras
        48: (31, 49),  # Venonat
        50: (26, 51),  # Diglett
        52: (28, 53),  # Meowth
        54: (33, 55),  # Psyduck
        56: (28, 57),  # Mankey
        58: (59, 59),  # Growlithe
        60: (25, 61),  # Poliwag
        63: (16, 64), 64: (65, 65),  # Abra line
        66: (28, 67), 67: (68, 68),  # Machop line
        69: (21, 70), 70: (71, 71),  # Bellsprout line
        72: (30, 73),  # Tentacool
        74: (25, 75), 75: (76, 76),  # Geodude line
        77: (40, 78),  # Ponyta
        79: (37, 80),  # Slowpoke
        81: (30, 82),  # Magnemite
        84: (31, 85),  # Doduo
        86: (34, 87),  # Seel
        88: (38, 89),  # Grimer
        90: (91, 91),  # Shellder
        92: (25, 93), 93: (94, 94),  # Gastly line
        96: (26, 97),  # Drowzee
        98: (28, 99),  # Krabby
        100: (30, 101),  # Voltorb
        102: (103, 103),  # Exeggcute
        104: (28, 105),  # Cubone
        109: (35, 110),  # Koffing
        111: (42, 112),  # Rhyhorn
        116: (32, 117),  # Horsea
        118: (33, 119),  # Goldeen
        120: (120, 121),  # Staryu
        129: (20, 130),  # Magikarp
        133: (133, 134, 135, 136),  # Eevee (special case - multiple evolutions)
        138: (40, 139),  # Omanyte
        140: (40, 141),  # Kabuto
        147: (30, 148), 148: (55, 149),  # Dratini line

    }
    
    # stone evolution mappings
    # format: stone_type: {pokemon_id: evolved_id}
    # example: 'fire': {37: 38} means Vulpix (37) evolves to Ninetales (38) with fire stone
    STONE_EVOLUTIONS = {
        'fire': {37: 38, 58: 59, 133: 136},  # Vulpix->Ninetales, Growlithe->Arcanine, Eevee->Flareon
        'water': {61: 62, 90: 91, 120: 121, 133: 134},  # Poliwhirl->Poliwrath, Shellder->Cloyster, Staryu->Starmie, Eevee->Vaporeon
        'thunder': {25: 26, 133: 135},  # Pikachu->Raichu, Eevee->Jolteon
        'leaf': {44: 45, 70: 71, 102: 103},  # Gloom->Vileplume, Weepinbell->Victreebel, Exeggcute->Exeggutor
        'moon': {30: 31, 33: 34, 35: 36, 39: 40}  # Nidorina->Nidoqueen, Nidorino->Nidoking, Clefairy->Clefable, Jigglypuff->Wigglytuff
    }
    
    # pokemon that can drop evolution stones when caught
    # format: stone_type: [list of pokemon_ids]
    # 5% chance to drop when caught
    STONE_DROPPERS = {
        'fire': [37, 58, 133],      # fire stone droppers
        'water': [61, 90, 120, 133],  # water stone droppers
        'thunder': [25, 133],        # thunder stone droppers
        'leaf': [44, 70, 102],       # leaf stone droppers
        'moon': [29, 32, 35, 39]     # moon stone droppers
    }
    
    def __init__(self, pokemon_id, name, hp, attack, defense, speed, pokemon_type, sprite_url, level=5, moves_list=None):
        # ============================================================
        # create a new pokemon instance
        # args(pokemon_id) - pokemon's ID number (1-151)
        #     (name) - pokemon's name
        #     (hp:) - base HP stat
        #     (attack:) - base attack stat
        #     (defense:) - base defense stat
        #     (speed:) - base speed stat
        #     (pokemon_type:) - pokemon's type (fire, water, etc.)
        #     (sprite_url) - URL to pokemon's image
        #     (level) - starting level (default 5)
        #     (moves_list) - list of all available moves for this pokemon (optional)
        # ============================================================
        # store basic pokemon information
        self.id = pokemon_id
        self.name = name
        self.base_hp = hp
        self.base_attack = attack
        self.base_defense = defense
        self.base_speed = speed
        self.type = pokemon_type
        self.sprite_url = sprite_url
        self.level = level
        
        # store the full moves list for this pokemon
        self.available_moves = moves_list if moves_list else []
        
        # Calculates current stats based on level
        self.hp = self._calculate_stat(self.base_hp)
        self.attack = self._calculate_stat(self.base_attack)
        self.defense = self._calculate_stat(self.base_defense)
        self.speed = self._calculate_stat(self.base_speed)
        
        # generates random moves (2-4 moves based on level) from this pokemon's move pool
        self.moves = self._generate_moves()
    
    def _calculate_stat(self, base_stat):
        # ============================================================
        # calculates actual stat from base stat and level
        # formula: base_stat + (level * 2)
        # args(base_stat) - the base value of the stat
        # returns: calculated stat value as integer   
        # ============================================================
        return int(base_stat + (self.level * 2))
    
    def _generate_moves(self):
        # ============================================================
        # generates 2-4 random moves based on level from this pokemon's actual move pool
        # - level 1-10: 2 random moves
        # - level 11-25: 3 random moves
        # - level 26+: 4 random moves
        # returns: list of move names specific to this pokemon    
        # ============================================================
        if not self.available_moves:
            return []
        
        # determines how many moves based on level
        if self.level <= 10:
            num_moves = 2  # low level: 2 moves
        elif self.level <= 25:
            num_moves = 3  # mid level: 3 moves
        else:
            num_moves = 4  # high level: 4 moves
        
        # makes sure we don't try to select more moves than available
        num_moves = min(num_moves, len(self.available_moves))
        # randomly select moves from this pokemon's move pool
        selected_moves = random.sample(self.available_moves, num_moves)
        # format move names nicely (replace hyphens with spaces)
        return [move.replace('-', ' ').title() for move in selected_moves]
    
    def update_stats(self):
        # ============================================================
        # recalculate stats after leveling up or evolving
        # also regenerates moves to match new level
        # ============================================================
        self.hp = self._calculate_stat(self.base_hp)
        self.attack = self._calculate_stat(self.base_attack)
        self.defense = self._calculate_stat(self.base_defense)
        self.speed = self._calculate_stat(self.base_speed)
        self.moves = self._generate_moves()  # regenerate moves based on new level
    
    def info(self):
        # ============================================================
        # displays all pokemon important stats and moves
        # ============================================================
        print(f"{self.name.capitalize()} (ID: {self.id}) - Level {self.level}")
        print(f"   Type: {self.type.capitalize()}")
        print(f"   HP: {self.hp} | ATK: {self.attack} | DEF: {self.defense} | SPD: {self.speed}")
        if self.moves:
            print(f"   Moves: {', '.join(self.moves)}")
    
    def __str__(self):
        # ============================================================
        # used when converting pokemon to string (e.g., print(pokemon))
        # returns: string with pokemon name and level   
        # ============================================================
        return f"{self.name} (Lv.{self.level})"
    
    # @staticmethod is a decorator that makes this method belong to the class itself,
    # not to any specific pokemon instance. 
    # this means:
    # 1. you can call it without creating a pokemon: Pokemon.check_evolution(my_pokemon)
    # 2. it doesn't need "self" - it doesn't access instance data like self.name or self.level
    # 3. it's useful for utility functions that relate to pokemon in general, not one specific pokemon
    # think of it like a tool in the pokemon toolbox that anyone can use, rather than
    # a feature of one particular pokemon.
    @staticmethod
    def check_evolution(pokemon):
        # ============================================================
        # checks if pokemon should evolve based on level
        # args(pokemon) - pokemon object to check
        # returns: evolved pokemon ID if should evolve
        # ============================================================
        # checks if this pokemon has a level-up evolution
        if pokemon.id in Pokemon.EVOLUTIONS:
            evo_data = Pokemon.EVOLUTIONS[pokemon.id]
            # checks if it's a simple evolution (not Eevee's multiple evolutions)
            if isinstance(evo_data, tuple) and len(evo_data) == 2:
                evo_level, evo_id = evo_data
                # checks if pokemon is high enough level
                if pokemon.level >= evo_level:
                    return evo_id
        return None 
    
    # @staticmethod means this function belongs to the pokemon class, not a specific pokemon.
    # why use it here? because checking if *any* pokemon can evolve with a stone
    # doesn't require data from a specific pokemon instance - we just need the ID and stone type.
    # this makes the code cleaner: Pokemon.can_stone_evolve(25, 'thunder')
    # instead of having to create a pokemon just to check evolution rules.
    @staticmethod
    def can_stone_evolve(pokemon_id, stone_type):
        # ============================================================
        # checks if pokemon can evolve with given stone
        # args(pokemon_id) - the pokemon's ID number
        #     (stone_type) - type of evolution stone (fire, water, thunder, leaf, moon)
        # returns: true if pokemon can evolve with this stone   
        # ============================================================
        return stone_type in Pokemon.STONE_EVOLUTIONS and pokemon_id in Pokemon.STONE_EVOLUTIONS[stone_type]
    
    # @staticmethod makes this a class-level function rather than an instance method.
    # it's perfect here because getting a stone evolution result is a lookup operation
    # that only needs the pokemon ID and stone type - no individual pokemon's data needed.
    # you can call this anywhere: evolved_id = Pokemon.stone_evolve(37, 'fire')
    @staticmethod
    def stone_evolve(pokemon_id, stone_type):
        # ============================================================
        # get evolution ID for stone evolution
        # args(pokemon_id) - the pokemon's ID number
        #     (stone_type) - type of evolution stone being used
        # returns: evolved pokemon ID if valid
        # ============================================================
        # checks if this is a valid stone evolution
        if Pokemon.can_stone_evolve(pokemon_id, stone_type):
            return Pokemon.STONE_EVOLUTIONS[stone_type][pokemon_id]
        return None
    
    # @staticmethod decorator means this function doesn't need access to any specific pokemon's data.
    # why? because stone drop chances are based on pokemon species (ID), not individual pokemon.
    # making it static means we can check drop chances from anywhere in the code:
    # stone = Pokemon.can_drop_stone(25) - without needing a pokemon object.
    # it also makes logical sense: "can species #25 drop stones?" vs "can this Pikachu drop stones?"
    @staticmethod
    def can_drop_stone(pokemon_id):
        # ============================================================
        # checks if pokemon can drop a stone and return stone type
        # 5% chance to drop when caught
        # args(pokemon_id) - the pokemon's ID number
        # returns: stone type (string) if drops    
        # ============================================================
        # checks each stone type to see if this pokemon can drop it
        for stone_type, pokemon_list in Pokemon.STONE_DROPPERS.items():
            if pokemon_id in pokemon_list:
                # 5% chance to actually drop
                if random.random() < 0.05:
                    return stone_type
        return None 
    
    # @staticmethod makes this a utility function that belongs to pokemon class but doesn't
    # need any pokemon instance data. this is ideal for API calls because:
    # 1. we're fetching data to create a pokemon, so no pokemon exists yet
    # 2. the function only needs an ID number - nothing from self.name, self.level, etc.
    # 3. it can be called easily: data = Pokemon.get_pokemon_data(25)
    # without @staticmethod, we'd need "self" parameter and an existing pokemon to call it.
    @staticmethod
    def get_pokemon_data(pokemon_id):
        # ============================================================ 
        # makes an HTTP request from pokeapi to get official pokemon stats and moves
        # args(pokemon_id) - the pokemon's ID number (1-151)
        # returns: dictionary with pokemon data (id, name, stats, type, sprite, moves)
        #     returns fallback data if API request fails 
        # ============================================================
        try:
            # build URL for pokeapi request
            url = f"https://pokeapi.co/api/v2/pokemon/{pokemon_id}"
            # make get request to API
            response = requests.get(url)
            
            if response.status_code == 200:
                data = response.json()
                
                # extract move names from the moves list
                moves_list = [move["move"]["name"] for move in data["moves"]]
                
                # extract and organize relevant data
                stats = {
                    "id": data['id'],
                    "name": data['name'],
                    "hp": data["stats"][0]["base_stat"],        # HP is first stat
                    "attack": data["stats"][1]["base_stat"],    # attack is second
                    "defense": data["stats"][2]["base_stat"],   # defense is third
                    "speed": data["stats"][5]["base_stat"],     # speed is sixth
                    "type": data["types"][0]["type"]["name"],   # primary type
                    "sprite": data["sprites"]["front_default"],  # image URL
                    "moves": moves_list  # list of all moves this pokemon can learn
                }
                return stats
            else:
                # API request failed
                print(f"Failed to fetch Pokémon {pokemon_id}")
                return None
        
        except Exception as e:
            # error occurred (network error, invalid ID, etc.)
            print(f"Error fetching Pokémon data: {e}")
            # return fallback data so game doesn't crash
            return {
                'id': pokemon_id,
                'name': f'pokemon_{pokemon_id}',
                'hp': 50,
                'attack': 50,
                'defense': 50,
                'speed': 50,
                'type': 'normal',
                'sprite': 'N/A',
                'moves': ['tackle', 'scratch']  # basic fallback moves
            }