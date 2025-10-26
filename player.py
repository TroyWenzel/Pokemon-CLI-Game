# this file manages the player's pokemon collection
# it handles storing pokemon in two locations: belt (active party) and pc (storage)

class Player:
    # ============================================================
    # manages player's pokemon collection with belt and pc storage
    # belt: holds up to 6 pokemon that the player carries with them
    # pc: unlimited storage for extra pokemon
    # ============================================================
    
    def __init__(self, name):
        # ============================================================
        # creates a new player 
        # args(name) - the player's trainer name    
        # ============================================================
        self.name = name
        self.poke_belt = []  # list to store up to 6 pokemon on the belt
        self.poke_pc = []    # list to store extra pokemon in pc storage
    
    def add_pokemon(self, pokemon):
        # ============================================================
        # add a caught pokemon to the player's collection - goes to belt if there's room, otherwise goes to PC
        # args(pokemon) The pokemon object to add
        # returns: "belt" if added to belt, "pc" if added to pc  
        # ============================================================
        # checks if belt has space (less than 6 pokemon)
        if len(self.poke_belt) < 6:
            self.poke_belt.append(pokemon)  # add to belt
            return "belt"
        else:
            self.poke_pc.append(pokemon)    # belt is full, add to pc
            return "pc"
    
    def remove_pokemon(self, location, index):
        # ============================================================
        # remove a pokemon from belt or pc
        # this is used when transferring pokemon to Professor Oak
        # args(location) - either "belt" or "pc"
        #     (index) - the position of the pokemon (0-based)    
        # returns: the pokemon object if found 
        # ============================================================
        # checks if removing from belt and index is valid
        if location == "belt" and 0 <= index < len(self.poke_belt):
            return self.poke_belt.pop(index)  # removes pokemon
        # checks if removing from pc and index is valid
        elif location == "pc" and 0 <= index < len(self.poke_pc):
            return self.poke_pc.pop(index)    # removes pokemon
        return None
    
    def get_pokemon(self, location, index):
        # ============================================================
        # get a pokemon from belt or pc without removing it
        # used to view or interact with pokemon
        # args(location) - either "belt" or "pc"
        #     (index) - the position of the pokemon (0-based)   
        # returns: the pokemon object if found    
        # ============================================================
        # checks if getting from belt and index is valid
        if location == "belt" and 0 <= index < len(self.poke_belt):
            return self.poke_belt[index]  # returns pokemon (doesn't remove it)
        # checks if getting from pc and index is valid
        elif location == "pc" and 0 <= index < len(self.poke_pc):
            return self.poke_pc[index]    # returns pokemon (doesn't remove it)
        return None 
    
    def transfer_to_pc(self, belt_index):
        # ============================================================
        # transfer a pokemon from the belt to pc storage
        # args(belt_index) - position of pokemon on belt (0-based)
        # returns: the Pokemon object if successful
        # ============================================================
        # checks if the belt index is valid
        if 0 <= belt_index < len(self.poke_belt):
            pokemon = self.poke_belt.pop(belt_index)  # remove from belt
            self.poke_pc.append(pokemon)              # add to pc
            return pokemon
        return None
    
    def transfer_to_belt(self, pc_index):
        # ============================================================
        # transfer a pokemon from pc to belt
        # if belt is full, the last pokemon on belt swaps places with the pc pokemon
        # args(pc_index) - position of pokemon in pc (0-based)
        # returns: tuple of (transferred_pokemon, swapped_pokemon)
        #     swapped_pokemon is None if belt wasn't full
        # ============================================================
        # checks if the pcindex is valid
        if 0 <= pc_index < len(self.poke_pc):
            pokemon = self.poke_pc.pop(pc_index)  # Remove from PC
            
            # Check if belt has room
            if len(self.poke_belt) < 6:
                self.poke_belt.append(pokemon)  # Add to belt
                return pokemon, None  # No swap needed
            else:
                # Belt is full - need to swap
                swapped = self.poke_belt.pop()      # Remove last Pokemon from belt
                self.poke_belt.append(pokemon)      # Add new Pokemon to belt
                self.poke_pc.append(swapped)        # Put old Pokemon in PC
                return pokemon, swapped  # Return both Pokemon involved
        return None, None  # Invalid index
    
    def show_belt(self):
        # ============================================================
        # displays all pokemon currently on the player's belt
        # ============================================================
        print("\n=== POKÉ BELT (6 max) ===")
        
        # checks if belt is empty
        if not self.poke_belt:
            print("  Empty")
        else:
            # loop through each pokemon on the belt
            for i, pokemon in enumerate(self.poke_belt, 1):
                print(f"  {i}. {pokemon.name.capitalize()} (Lv.{pokemon.level}) - Type: {pokemon.type.capitalize()}")
                print(f"     HP: {pokemon.hp} | ATK: {pokemon.attack} | DEF: {pokemon.defense} | SPD: {pokemon.speed}")
    
    def show_pc(self, page=1, per_page=10):
        # ============================================================
        # displays pokemon in pc storage
        # args(page) - current page number (starts at 1)
        #     (per_page) - how many pokemon to show per page (default 10)
        # returns: tuple of (total_pages, current_page)
        #     
        # ============================================================
        print("\n=== POKÉ PC (Storage) ===")
        
        # checks if pc is empty
        if not self.poke_pc:
            print("  Empty")
            return 1, 1 
        
        # calculates how many pages
        total_pokemon = len(self.poke_pc)  # total number of pokemon in pc
        total_pages = (total_pokemon + per_page - 1) // per_page
        
        # makes sure page number is valid
        page = max(1, min(page, total_pages))
        
        # calculates which pokemon to show
        start_index = (page - 1) * per_page  # first pokemon on this page
        end_index = min(start_index + per_page, total_pokemon)  # last pokemon on this page
        
        # displays page info
        print(f"Page {page}/{total_pages} (Showing {start_index + 1}-{end_index} of {total_pokemon})")
        print()
        
        for i in range(start_index, end_index):
            pokemon = self.poke_pc[i]
            # print pokemon info (number shown is actual position in pc)
            print(f"  {i + 1}. {pokemon.name.capitalize()} (Lv.{pokemon.level}) - Type: {pokemon.type.capitalize()}")
            print(f"     HP: {pokemon.hp} | ATK: {pokemon.attack} | DEF: {pokemon.defense} | SPD: {pokemon.speed}")
        
        if total_pages > 1:
            print()
            if page < total_pages:
                print("  Type 'next' to see next page")
            if page > 1:
                print("  Type 'prev' to see previous page")
        
        return total_pages, page
    
    def total_count(self):
        # ============================================================
        # calculates total number of pokemon the player has caught
        # returns: total count of pokemon in belt + pc 
        # ============================================================
        return len(self.poke_belt) + len(self.poke_pc)