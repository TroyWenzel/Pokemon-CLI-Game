# this file manages the pokedex - a digital encyclopedia of pokemon
# it tracks which pokemon the player has seen and caught
# it also includes a lottery system for winning free items

import random 

class Pokedex:
    # ============================================================
    # tracks seen and caught pokemon, includes a lottery system
    
    # The pokedex keeps a record of:
    # - pokemon the player has encountered (seen)
    # - pokemon the player has caught
    # - full data about caught pokémon
    # ============================================================
    
    def __init__(self):
        # ============================================================
        # creates a new empty pokedex
        # ============================================================
        self.seen = set()     # set of pokemon IDs that have been seen (sets don't allow duplicates)
        self.caught = {}      # dictionary: pokemon ID -> full data dict
    
    def mark_seen(self, pokemon_id):
        # ============================================================
        # mark a pokemon as seen in the pokedex when player encounters it
        # args(pokemon_id) - the ID number of the pokemon (1-151)    
        # ============================================================
        self.seen.add(pokemon_id)  # Add to set of seen Pokemon
    
    def mark_caught(self, pokemon_id, pokemon_data):
        # ============================================================
        # mark a pokemon as caught with full data if caught
        # args(pokemon_id) - the ID number of the pokemon (1-151)
        #     (pokemon_data) - dictionary containing all pokemon info (stats, type, etc.)    
        # ============================================================
        self.seen.add(pokemon_id)  # Also mark as seen
        if pokemon_id not in self.caught:
            self.caught[pokemon_id] = pokemon_data  # Store full data
    
    def is_caught(self, pokemon_id):
        # ============================================================
        # checks if a specific pokemon has been caught
        # args(pokemon_id) the ID number to check
        # returns: true if caught    
        # ============================================================
        return pokemon_id in self.caught
    
    def is_seen(self, pokemon_id):
        # ============================================================
        # checks if a specific pokemon has been seen
        # args(pokemon_id) - the ID number to check
        # returns: true if seen    
        # ============================================================
        return pokemon_id in self.seen
    
    def show_pokedex(self, get_pokemon_data_func, page=1, per_page=20):
        # ============================================================
        # displays the pokedex with seen and caught pokemon
        # Args:(get_pokemon_data_func) Function to get Pokemon data (from Pokemon class)
        #     (page) Current page number (starts at 1)
        #     (per_page) How many Pokemon to show per page (default 20) 
        # returns: tuple of (total_pages, current_page)
        # ============================================================
        print("\n=== POKÉDEX ===")
        print(f"Seen: {len(self.seen)} | Caught: {len(self.caught)} | Total: 151")
        print("\nLegend: ??? (Not Seen) | NAME (Seen) | √ NAME (Caught)\n")
        
        # calculates how many pages for the 151 pokemon
        total_pokemon = 151  # total pokemon in gen 1
        total_pages = (total_pokemon + per_page - 1) // per_page 
        
        # make sure page number is valid
        page = max(1, min(page, total_pages))
        
        # calculate which pokemon to show
        start_id = (page - 1) * per_page + 1  # first pokemon ID on this page
        end_id = min(start_id + per_page, total_pokemon + 1)  # last pokemon ID + 1
        
        print(f"Page {page}/{total_pages} (Showing #{start_id}-#{end_id - 1})")
        print()
        
        for i in range(start_id, end_id):
            # check if pokemon has been caught
            if i in self.caught:
                data = self.caught[i]
                # show checkmark, name, and type for caught pokemon
                print(f"  #{i:03d}: √ {data['name'].capitalize()} - Type: {data['type']}")
            # check if pokemon has been seen (but not caught)
            elif i in self.seen:
                try:
                    data = get_pokemon_data_func(i)  # get basic data
                    print(f"  #{i:03d}: {data['name'].capitalize()} (Seen only)") # show name for seen pokemon
                except:
                    # if data fetch fails, show as not seen
                    print(f"  #{i:03d}: ??? (Not seen)")
            else:
                print(f"  #{i:03d}: ??? (Not seen)")
        
        if total_pages > 1:
            print()
            if page < total_pages:
                print("  Type 'next' to see next page")
            if page > 1:
                print("  Type 'prev' to see previous page")
        
        return total_pages, page
    
    def show_pokemon_details(self, pokemon_id, get_pokemon_data_func):
        # ============================================================
        # show detailed information for a specific pokemon
        # different info shown based on whether pokemon is caught or just seen
        
        # Args(pokemon_id)the ID of the pokemon to display (1-151)
        #     (get_pokemon_data_func) - function to get pokemon data
        # ============================================================
        # check if pokemon has been caught
        if pokemon_id in self.caught:
            data = self.caught[pokemon_id]
            # show full stats for caught pokemon
            print(f"\n=== {data['name'].upper()} (#{pokemon_id:03d}) ===")
            print(f"Type: {data['type'].capitalize()}")
            print(f"HP: {data['hp']}")
            print(f"Attack: {data['attack']}")
            print(f"Defense: {data['defense']}")
            print(f"Speed: {data['speed']}")
            print(f"Status: CAUGHT √")
        elif pokemon_id in self.seen: # check if Pokemon has been seen
            try:
                data = get_pokemon_data_func(pokemon_id) # show limited info for seen Pokemon
                print(f"\n=== {data['name'].upper()} (#{pokemon_id:03d}) ===")
                print(f"Type: {data['type'].capitalize()}")
                print(f"Status: SEEN (Not caught yet)")
                print("Catch this Pokémon to see full stats!")
            except:
                print("Pokémon data not available.")
        else:
            print(f"\n=== #{pokemon_id:03d} ===")
            print("Status: NOT SEEN")
            print("You haven't encountered this Pokémon yet!")
    
    def poke_lottery(self):
        # ============================================================
        # run the poke Lottery for random items - can win pokeballs, berries, evolution stones, or nothing
        # returns: tuple of (item_type, item_name, quantity) if won, none if lost
        # ============================================================
        
        # define all possible lottery prizes with their probabilities
        # format: (item_type, item_name, quantity, weight)- higher weight = more likely to win
        lottery_pool = [
            ('pokéball', 'poké', 10, 25),    # common: 10 poke balls
            ('pokéball', 'great', 5, 15),    # nncommon: 5 great balls
            ('pokéball', 'ultra', 1, 5),     # rare: 1 ultra ball
            ('pokéball', 'master', 1, 2),    # very rare: 1 master ball
            ('berry', 'razz', 5, 20),        # common: 5 razz berries
            ('berry', 'pinap', 5, 20),       # common: 5 pinap berries
            ('stone', 'fire', 1, 2),         # very rare: fire stone
            ('stone', 'water', 1, 2),        # very rare: water stone
            ('stone', 'thunder', 1, 2),      # very rare: thunder stone
            ('stone', 'leaf', 1, 2),         # very rare: leaf stone
            ('stone', 'moon', 1, 2),         # very rare: moon stone
            ('nothing', 'nothing', 0, 1)     # lose ticket
        ]
        
        # calculate total weight of all prizes
        total_weight = sum(item[3] for item in lottery_pool)
        
        # generate random number between 0 and total_weight
        roll = random.uniform(0, total_weight)
        
        # determine which prize was won
        current_weight = 0
        for item_type, item_name, quantity, weight in lottery_pool:
            current_weight += weight
            if roll <= current_weight:
                if item_type == 'nothing':
                    return None 
                return (item_type, item_name, quantity)
        
        return None
    
    def completion_percentage(self):
        # ============================================================
        # calculate what percentage of the pokedex has been completed
        # returns: a float percentage between (0-100)    
        # ============================================================
        return (len(self.caught) / 151) * 100