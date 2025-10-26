import os 
from pokemon import Pokemon
from player import Player
from inventory import Inventory
from pokedex import Pokedex
from hunting_pokemon import HuntingSystem


def clear_screen():
    os.system('cls' if os.name == 'nt' else 'clear') # clears the terminal screen


class PokemonGame:
# ============================================================
# main game class that orchestrates all systems
# ============================================================
    
    def __init__(self):
    # ============================================================
    # initialize the game and create all the systems we need
    # ============================================================
        self.player = None  # will be created when game starts
        self.inventory = Inventory()  # player's items (balls, berries, badges, etc.)
        self.pokedex = Pokedex()  # tracks which pokemon have been seen/caught
        self.hunting = HuntingSystem()  # handles wild pokemon encounters
        self.wild_pokemon = None  # currently encountered wild pokemon
        self.used_berry = None  # berry used in current encounter
    
    def start_game(self):
        # ============================================================
        # initialize game with Professor Oak's welcome
        # displays welcome message to the player
        # ============================================================
        print("\n" + "="*50)
        print("  WELCOME TO POKÉMON CLI ADVENTURE!")
        print("="*50)
        print("\nProfessor Oak: Hello there! Welcome to the world")
        print("of Pokémon! My name is Oak. People call me")
        print("the Pokémon Prof!")
        print("\nThis world is inhabited by creatures called")
        print("Pokémon! For some people, Pokémon are pets.")
        print("Others use them for fights. Myself...")
        print("I study Pokémon as a profession.")
        
        name = input("\nFirst, what is your name? ").strip() # get player's name only, no whitespace characters
        if not name:
            name = "Trainer"  # default name if player doesn't enter one
        
        self.player = Player(name) # create the player
        
        print(f"\nProfessor Oak: Ah, {name}! Your very own")
        print("Pokémon legend is about to unfold! A world")
        print("of dreams and adventures with Pokémon await!")
        print("But first, you'll need a partner Pokémon!")
        
        # marks starter pokemon as seen in pokedex
        self.pokedex.mark_seen(1)  # Bulbasaur
        self.pokedex.mark_seen(4)  # Charmander
        self.pokedex.mark_seen(7)  # Squirtle
        
        self.choose_starter() # let player choose their starter
        
        print(f"\nProfessor Oak: {name}, your Pokémon journey")
        print("begins now! Good luck, and remember to fill")
        print("your Pokédex!")
        
        self.main_menu()
        # ============================================================
        # calls the main game loop
        # ============================================================
    
    def choose_starter(self):
        # ============================================================
        # lets player choose their starter pokemon
        # classic choice between Bulbasaur, Charmander, and Squirtle
        # ============================================================
        print("\n" + "="*50)
        print("  CHOOSE YOUR STARTER POKEMON")
        print("="*50)
        print("\n1. Bulbasaur (Grass type)")
        print("   HP: 45 | Attack: 49 | A well-balanced starter!")
        print("\n2. Charmander (Fire type)")
        print("   HP: 39 | Attack: 52 | High attack power!")
        print("\n3. Squirtle (Water type)")
        print("   HP: 44 | Attack: 48 | Great defenses!")
        
        
        while True: # loop until player makes a valid choice
            choice = input("\nEnter 1, 2, or 3: ").strip()
            
            if choice == '1':
                pokemon_id = 1  # Bulbasaur
                break
            elif choice == '2':
                pokemon_id = 4  # Charmander
                break
            elif choice == '3':
                pokemon_id = 7  # Squirtle
                break
            else:
                print("Invalid choice! Please enter 1, 2, or 3.")
        
        data = Pokemon.get_pokemon_data(pokemon_id) # get pokemon data from the API
        # create the starter pokemon object
        starter = Pokemon(
            data['id'], data['name'], data['hp'], data['attack'],
            data['defense'], data['speed'], data['type'],
            data['sprite'], level=5, moves_list=data.get('moves', [])  # starters begin at level 5
        )
        
        # add to player's collection and mark in pokedex
        self.player.add_pokemon(starter)
        self.pokedex.mark_caught(pokemon_id, data)
        self.inventory.update_badge(starter.type)  # begins badge progress
        
        print(f"\nYou chose {starter.name.capitalize()}! Great choice!")
    
    def main_menu(self):
        # ============================================================
        # main game menu loop
        # ============================================================
        while True:  # keep looping until player quits
            clear_screen() 
            print(f"\n{'='*50}")
            print(f"  POKÉMON ADVENTURE - {self.player.name}")
            print(f"{'='*50}")
            print("1. Go hunting (find wild Pokémon)")
            print("2. View Poké Belt")
            print("3. View Poké PC")
            print("4. View Inventory")
            print("5. View Pokédex")
            print("6. Quit game")
            
            choice = input("\nWhat would you like to do? ").strip()
            
            # handle player's menu choice, hunt, inventory, pokedex, exit
            if choice == '1':
                clear_screen()
                self.go_hunting()  # find wild pokemon
            elif choice == '2':
                clear_screen()
                self.belt_menu()  # manage max 6 pokemon in belt
            elif choice == '3':
                clear_screen()
                self.pc_menu()  # manage pc stored pokemon
            elif choice == '4':
                clear_screen()
                self.inventory_menu()  # view/use items
            elif choice == '5':
                clear_screen()
                self.pokedex_menu()  # view pokedex
            elif choice == '6':
                clear_screen()
                print(f"\nThanks for playing, {self.player.name}!")
                print("Your adventure will continue next time!")
                break  # exits the game
            else:
                print("Invalid choice! Please try again.")
                input("Press Enter to continue...")
    
    def go_hunting(self):
        # ============================================================
        # player encounters a random wild pokemon
        # ============================================================
        print("\nYou venture into the tall grass...")
        print("Searching for Pokémon...")
        
        # get player's badge data to determine spawn chances
        badge_data = {}
        for ptype, data in self.inventory.badges.items():
            badge_data[ptype] = self.inventory.get_badge_bonus(ptype)
        
        # generate a random wild pokemon based on player's progress
        pokemon_id, level = self.hunting.generate_wild_pokemon(badge_data)
        
        # fetch pokemon data from the API
        data = Pokemon.get_pokemon_data(pokemon_id)
        # create the wild pokemon object
        self.wild_pokemon = Pokemon(
            data['id'], data['name'], data['hp'], data['attack'],
            data['defense'], data['speed'], data['type'],
            data['sprite'], level=level, moves_list=data.get('moves', [])
        )
        
        self.pokedex.mark_seen(pokemon_id) # mark as seen in pokedex (even if not caught)
        
        # displays encounter message
        print(f"\n{'='*50}")
        print(f"  A wild {self.wild_pokemon.name.capitalize()} appeared!")
        
        # special messages for rare pokemon
        if self.hunting.is_pokemon_legendary(pokemon_id):
            print("  THIS IS A LEGENDARY POKÉMON!")
        elif self.hunting.is_pokemon_rare(pokemon_id):
            print("  This is a rare Pokémon!")
        
        print(f"{'='*50}")
        self.wild_pokemon.info()  # show pokemon stats
        
        self.encounter_menu() # calls the encounter menu
    
    def encounter_menu(self):
        # ============================================================
        # player's encounter with wild pokemon - use berry, throw ball, run 
        # ============================================================
        self.used_berry = None  # reset berry usage for this encounter
        
        # loop until pokemon is caught, flees, or player runs away
        while self.wild_pokemon:
            print(f"\n{'='*50}")
            print("  ENCOUNTER OPTIONS")
            print(f"{'='*50}")
            print("1. Use Berry (before catching)")
            print("2. Throw Pokéball")
            print("3. Run Away")
            
            choice = input("\nWhat do you want to do? ").strip()
            
            if choice == '1':
                self.use_berry_menu()  # use a berry
            elif choice == '2':
                self.try_catch_pokemon()  # attempt to catch
                if not self.wild_pokemon:  # pokemon was caught or fled
                    input("\nPress Enter to continue...")
            elif choice == '3':
                # player runs away
                print(f"\nYou fled from the wild {self.wild_pokemon.name}!")
                self.wild_pokemon = None
                input("\nPress Enter to continue...")
                break
            else:
                print("Invalid choice!")
                input("Press Enter to continue...")
    
    def use_berry_menu(self):
        # ============================================================
        # let player use a berry before catching, similar to pokemon go
        # razz berry increases catch chance
        # pinap berry doubles candy reward after catching
        # ============================================================
        # checks if a berry was already used
        if self.used_berry:
            print("\nYou already used a berry for this encounter!")
            return
        
        print("\n=== USE BERRY ===")
        print(f"1. Razz Berry ({self.inventory.berries['razz']} available) - Increases catch chance")
        print(f"2. Pinap Berry ({self.inventory.berries['pinap']} available) - Doubles candy reward")
        print("3. Cancel")
        
        choice = input("\nChoose a berry: ").strip()
        
        # try to use the selected berry
        if choice == '1' and self.inventory.use_berry('razz'):
            self.used_berry = 'razz'
            print("\nYou used a Razz Berry! Catch chance increased!")
        elif choice == '2' and self.inventory.use_berry('pinap'):
            self.used_berry = 'pinap'
            print("\nYou used a Pinap Berry! You'll get double candy if caught!")
        elif choice == '3':
            return 
        else:
            print("\nYou don't have that berry!")
    
    def try_catch_pokemon(self):
        # ============================================================
        # attempt to catch the wild pokemon
        # success depends on ball type, badge bonuses, and berries used
        # ============================================================
        if not self.wild_pokemon:
            return
        
        # lets player choose which ball to use
        print("\n=== CHOOSE POKÉBALL ===")
        print(f"1. Poké Ball ({self.inventory.pokeballs['poké']} available) - Base catch rate")
        print(f"2. Great Ball ({self.inventory.pokeballs['great']} available) - 50% better")
        print(f"3. Ultra Ball ({self.inventory.pokeballs['ultra']} available) - 125% better")
        print(f"4. Master Ball ({self.inventory.pokeballs['master']} available) - 260% better")
        print("5. Cancel")
        
        choice = input("\nChoose a ball: ").strip()
        
        # map choices to ball types
        ball_types = {'1': 'poké', '2': 'great', '3': 'ultra', '4': 'master'}
        
        if choice == '5':
            return 
        
        if choice not in ball_types:
            print("Invalid choice!")
            return
        
        ball_type = ball_types[choice]
        
        # checks if player can use the selected ball
        if not self.inventory.use_pokeball(ball_type):
            print(f"\nYou don't have any {ball_type.capitalize()} Balls!")
            return
        
        # calculate catch rate based on multiple factors
        badge_bonus, _ = self.inventory.get_badge_bonus(self.wild_pokemon.type)
        catch_rate = self.hunting.calculate_catch_rate(
            self.wild_pokemon.id,
            self.wild_pokemon.level,
            ball_type,
            badge_bonus,
            self.used_berry
        )
        
        print(f"\nYou throw a {ball_type.capitalize()} Ball...")
        print(f"Catch rate: {catch_rate*100:.1f}%")
        print("...")
        
        result = self.hunting.attempt_catch(catch_rate) # attempt to catch the pokemon
        if result == 'caught':
            print(f"\nGotcha! {self.wild_pokemon.name.capitalize()} was caught!")
            
            location = self.player.add_pokemon(self.wild_pokemon) # add to the player's collection
            if location == "pc":
                print(f"{self.wild_pokemon.name} was sent to your PC!")
            
            # updates the pokedex
            data = Pokemon.get_pokemon_data(self.wild_pokemon.id)
            self.pokedex.mark_caught(self.wild_pokemon.id, data)
            
            # updates badge progress based on pokemon type
            self.inventory.update_badge(self.wild_pokemon.type)
            
            # adds poke candy as a reward
            candy_amount = 2 if self.used_berry == 'pinap' else 1
            self.inventory.add_candy(candy_amount)
            print(f"You received {candy_amount} Poké Candy!")
            
            # checks if a specific pokemon drops an evolution stone
            stone_drop = Pokemon.can_drop_stone(self.wild_pokemon.id)
            if stone_drop:
                self.inventory.add_stone(stone_drop)
                print(f"The Pokémon dropped a {stone_drop.capitalize()} Stone!")
            self.wild_pokemon = None 
        elif result == 'fled':
            print(f"\nOh no! {self.wild_pokemon.name.capitalize()} broke free and fled!")
            self.wild_pokemon = None     
        else:
            print(f"\n{self.wild_pokemon.name.capitalize()} broke free!")
            # pokemon stays, player can try again
    
    def belt_menu(self):
        # ============================================================
        # menu for poke belt management - view, level up, evolve, or transfer pokemon (for now)
        # ============================================================
        while True:
            clear_screen()
            self.player.show_belt()  # displays all pokemon player is carrying on their belt
            print("\n=== BELT OPTIONS ===")
            print("1. View Pokémon Stats")
            print("2. Level Up Pokémon")
            print("3. Evolve Pokémon")
            print("4. Transfer Pokémon to Professor Oak")
            print("5. Transfer Pokémon to PC")
            print("6. Back to Main Menu")
            
            choice = input("\nChoose an option: ").strip()
            
            if choice == '1':
                self.view_pokemon_stats("belt")
            elif choice == '2':
                self.level_up_pokemon("belt")
            elif choice == '3':
                self.evolve_pokemon("belt")
            elif choice == '4':
                self.transfer_to_oak("belt")
            elif choice == '5':
                self.transfer_belt_to_pc()
            elif choice == '6':
                break 
            else:
                print("Invalid choice!")
                input("Press Enter to continue...")
    
    def pc_menu(self):
        # ============================================================
        # menu for poke pc management 
        # ============================================================
        current_page = 1 
        
        while True:
            clear_screen()
            total_pages, current_page = self.player.show_pc(page=current_page, per_page=10)
            print("\n=== PC OPTIONS ===")
            print("1. View Pokémon Stats")
            print("2. Level Up Pokémon")
            print("3. Evolve Pokémon")
            print("4. Transfer Pokémon to Professor Oak")
            print("5. Transfer Pokémon to Belt")
            if total_pages > 1:
                print("\nType 'next' for next page, 'prev' for previous page")
            print("\n6. Back to Main Menu")
            choice = input("\nChoose an option: ").strip().lower()
            
            if choice == 'next' and current_page < total_pages:
                current_page += 1
                continue
            elif choice == 'prev' and current_page > 1:
                current_page -= 1
                continue
            
            if choice == '1':
                self.view_pokemon_stats("pc")
            elif choice == '2':
                self.level_up_pokemon("pc")
            elif choice == '3':
                self.evolve_pokemon("pc")
            elif choice == '4':
                self.transfer_to_oak("pc")
            elif choice == '5':
                self.transfer_pc_to_belt()
            elif choice == '6':
                break 
            else:
                print("Invalid choice!")
                input("Press Enter to continue...")
    
    def inventory_menu(self):
        # ============================================================
        # menu for inventory management - pokeballs, berries, and evolution stones(for now)
        # ============================================================
        while True:
            clear_screen()
            self.inventory.show_inventory()  # display all items
            print("\n=== INVENTORY OPTIONS ===")
            print("1. Use Evolution Stone")
            print("2. Poké Lottery")
            print("3. Back to Main Menu")
            
            choice = input("\nChoose an option: ").strip()
            
            if choice == '1':
                clear_screen()
                self.stone_evolution_menu()
            elif choice == '2':
                clear_screen()
                self.run_lottery()
            elif choice == '3':
                break 
            else:
                print("Invalid choice!")
                input("Press Enter to continue...")
    
    def pokedex_menu(self):
        # ============================================================
        # menu for pokedex viewing all 151 pokemon and view details 
        # ============================================================
        current_page = 1 
        
        while True:
            clear_screen()
            total_pages, current_page = self.pokedex.show_pokedex(Pokemon.get_pokemon_data, page=current_page, per_page=20)
            
            print("\n=== POKÉDEX OPTIONS ===")
            print("1. View Pokémon Details")
            print("2. Poké Lottery")
            
            if total_pages > 1:
                print("\nType 'next' for next page, 'prev' for previous page")
            print("\n3. Back to Main Menu")
            choice = input("\nChoose an option: ").strip().lower()
            
            if choice == 'next' and current_page < total_pages:
                current_page += 1
                continue
            elif choice == 'prev' and current_page > 1:
                current_page -= 1
                continue
            
            if choice == '1':
                try:
                    pokemon_id = int(input("\nEnter Pokémon ID (1-151): ").strip())
                    if 1 <= pokemon_id <= 151:
                        self.pokedex.show_pokemon_details(pokemon_id, Pokemon.get_pokemon_data)
                        input("\nPress Enter to continue...")
                    else:
                        print("Invalid ID! Must be between 1-151.")
                        input("Press Enter to continue...")
                except:
                    print("Invalid input!")
                    input("Press Enter to continue...")
            elif choice == '2':
                clear_screen()
                self.run_lottery()
            elif choice == '3':
                break
            else:
                print("Invalid choice!")
                input("Press Enter to continue...")
    
    def view_pokemon_stats(self, location):
        # ============================================================
        # view detailed stats of a pokemon
        # args(location) = "belt" or "pc"    
        # ============================================================
        try:
            index = int(input("\nWhich Pokémon? (number): ").strip()) - 1
            pokemon = self.player.get_pokemon(location, index)
            
            if pokemon:
                print("\n" + "="*50)
                pokemon.info()
                print("="*50)
                input("\nPress Enter to continue...")
            else:
                print("Invalid Pokémon!")
                input("Press Enter to continue...")
        except:
            print("Invalid input!")
            input("Press Enter to continue...")
    
    def level_up_pokemon(self, location):
        # ============================================================
        # level up a pokemon using candy 
        # can trigger evolution if pokemon reaches evolution level
        # args(location) = "belt" or "pc"
        # ============================================================
        print(f"\nPoké Candy Available: {self.inventory.poke_candy}")
        
        try:
            index = int(input("Which Pokémon? (number): ").strip()) - 1
            pokemon = self.player.get_pokemon(location, index)
            
            if not pokemon:
                print("Invalid Pokémon!")
                input("Press Enter to continue...")
                return
            
            candy = int(input("How many levels? (1 candy = 1 level): ").strip())
            
            if candy <= 0:
                print("Must use at least 1 candy!")
                input("Press Enter to continue...")
                return
            
            if candy > self.inventory.poke_candy:
                print("Not enough candy!")
                input("Press Enter to continue...")
                return
            
            old_level = pokemon.level
            pokemon.level += candy
            pokemon.update_stats()  # calculates new stats for new level
            self.inventory.use_candy(candy)  # removes candy from inventory
            
            print(f"\n{pokemon.name.capitalize()} leveled up from {old_level} to {pokemon.level}!")
            
            # check if pokemon should evolve
            evo_id = Pokemon.check_evolution(pokemon)
            if evo_id:
                evo_data = Pokemon.get_pokemon_data(evo_id)
                old_name = pokemon.name
                pokemon.id = evo_id
                pokemon.name = evo_data['name']
                pokemon.base_hp = evo_data['hp']
                pokemon.base_attack = evo_data['attack']
                pokemon.base_defense = evo_data['defense']
                pokemon.base_speed = evo_data['speed']
                pokemon.available_moves = evo_data.get('moves', [])
                pokemon.update_stats()
                print(f"\n{old_name.capitalize()} evolved into {pokemon.name.capitalize()}!")
                self.pokedex.mark_caught(evo_id, evo_data)
            
            input("\nPress Enter to continue...")
        except:
            print("Invalid input!")
            input("Press Enter to continue...")
    
    def evolve_pokemon(self, location):
        # ============================================================
        # menu for pokemon evolution
        # args(location) = "belt" or "pc"
        # ============================================================
        print("\n=== EVOLVE POKÉMON ===")
        print("Pokémon can evolve by:")
        print("  - Leveling up (automatic)")
        print("  - Using evolution stones (use Inventory menu)")
        input("\nPress Enter to continue...")
    
    def stone_evolution_menu(self):
        # ============================================================
        # menu for stone evolutions - only used on compatible pokemon
        # ============================================================
        print("\n=== STONE EVOLUTION ===")
        print("1. Use stone on Belt Pokémon")
        print("2. Use stone on PC Pokémon")
        print("3. Cancel")       
        choice = input("\nChoose: ").strip()

        if choice == '1':
            location = "belt"
            self.player.show_belt()
        elif choice == '2':
            location = "pc"
            self.player.show_pc()
        else:
            return
        
        try:
            index = int(input("\nWhich Pokémon? (number): ").strip()) - 1
            pokemon = self.player.get_pokemon(location, index)
            
            if not pokemon:
                print("Invalid Pokémon!")
                input("Press Enter to continue...")
                return
            
            print("\nAvailable stones: fire, water, thunder, leaf, moon")
            stone_type = input("Which stone? ").strip().lower()
            
            if stone_type not in self.inventory.stones:
                print("Invalid stone type!")
                input("Press Enter to continue...")
                return
            
            if self.inventory.stones[stone_type] <= 0:
                print("You don't have that stone!")
                input("Press Enter to continue...")
                return
            
            # attempts a stone evolution
            evo_id = Pokemon.stone_evolve(pokemon.id, stone_type)
            
            if evo_id:
                self.inventory.use_stone(stone_type)
                evo_data = Pokemon.get_pokemon_data(evo_id)
                old_name = pokemon.name
                pokemon.id = evo_id
                pokemon.name = evo_data['name']
                pokemon.base_hp = evo_data['hp']
                pokemon.base_attack = evo_data['attack']
                pokemon.base_defense = evo_data['defense']
                pokemon.base_speed = evo_data['speed']
                pokemon.available_moves = evo_data.get('moves', [])
                pokemon.update_stats()
                print(f"\n{old_name.capitalize()} evolved into {pokemon.name.capitalize()}!")
                self.pokedex.mark_caught(evo_id, evo_data)
                input("\nPress Enter to continue...")
            else:
                print("That Pokémon can't evolve with that stone!")
                input("Press Enter to continue...")
        except:
            print("Invalid input!")
            input("Press Enter to continue...")
    
    def transfer_to_oak(self, location):
        # ============================================================
        # transfer pokemon to Professor Oak - permanently removes the pokemon but gives 1 candy 
        # args(location) = "belt" or "pc"
        # ============================================================
        try:
            index = int(input("\nWhich Pokémon to transfer? (number): ").strip()) - 1
            pokemon = self.player.remove_pokemon(location, index)
            
            if pokemon:
                self.inventory.add_candy(1)
                print(f"\n{pokemon.name.capitalize()} was transferred to Professor Oak!")
                print("You received 1 Poké Candy!")
                input("\nPress Enter to continue...")
            else:
                print("Invalid Pokémon!")
                input("Press Enter to continue...")
        except:
            print("Invalid input!")
            input("Press Enter to continue...")
    
    def transfer_belt_to_pc(self):
        # ============================================================
        # transfer pokemon from belt to pc
        # ============================================================
        try:
            index = int(input("\nWhich Pokémon to transfer to PC? (number): ").strip()) - 1
            pokemon = self.player.transfer_to_pc(index)
            
            if pokemon:
                print(f"\n{pokemon.name.capitalize()} was transferred to PC!")
                input("\nPress Enter to continue...")
            else:
                print("Invalid Pokémon!")
                input("\nPress Enter to continue...")
        except:
            print("Invalid input!")
            input("Press Enter to continue...")
    
    def transfer_pc_to_belt(self):
        # ============================================================
        # transfer pokemon from pc to belt - if belt is full, pokemon goto pc
        # ============================================================
        try:
            index = int(input("\nWhich Pokémon to transfer to Belt? (number): ").strip()) - 1
            pokemon, swapped = self.player.transfer_to_belt(index)
            
            if pokemon:
                print(f"\n{pokemon.name.capitalize()} was transferred to Belt!")
                if swapped:
                    print(f"{swapped.name.capitalize()} was moved to PC (Belt was full)")
                input("\nPress Enter to continue...")
            else:
                print("Invalid Pokémon!")
                input("Press Enter to continue...")
        except:
            print("Invalid input!")
            input("Press Enter to continue...")
    
    def run_lottery(self):
        # ============================================================
        # runs the poke lottery - players can try their luck to win free items
        # ============================================================
        print("\n=== POKÉ LOTTERY ===")
        print("Try your luck for free items!")
        input("Press Enter to spin... ")
        print("\nSpinning...")
        
        result = self.pokedex.poke_lottery()
        
        if result:
            item_type, item_name, quantity = result
            if item_type == 'pokéball':
                self.inventory.add_pokeball(item_name, quantity)
                print(f"\nYou won {quantity} {item_name.capitalize()} Ball(s)!")
            elif item_type == 'berry':
                self.inventory.add_berry(item_name, quantity)
                print(f"\nYou won {quantity} {item_name.capitalize()} Berr{'y' if quantity == 1 else 'ies'}!")
            elif item_type == 'stone':
                self.inventory.add_stone(item_name, quantity)
                print(f"\nJACKPOT! You won a {item_name.capitalize()} Stone!")
        else:
            print("\nBetter luck next time!")
        
        input("\nPress Enter to continue...")

if __name__ == "__main__":
    game = PokemonGame()
    game.start_game()