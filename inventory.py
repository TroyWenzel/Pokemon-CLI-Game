# this file manages the player's inventory
# it tracks: pokeballs, berries, evolution stones, candy, and badges

class Inventory:
    # ============================================================
    # the inventory is like the player's backpack - it holds everything the player needs to catch, evolve, and level up pokemon
    # ============================================================
    def __init__(self):
        # ============================================================
        # create a new inventory with starting items
        # players begin with some pokeballs and berries
        # ============================================================
        # dictionary of pokeballs (name: quantity)
        # better the ball, the higher the catch rates
        self.pokeballs = {
            'poké': 20,     # standard ball - 20 to start
            'great': 5,     # better ball - 5 to start
            'ultra': 2,     # even better - 2 to start
            'master': 1     # best ball - 1 to start (never fails)
        }
        
        # dictionary of berries (name: quantity)
        # berries provide bonuses when catching pokemon
        self.berries = {
            'razz': 5,   # increases catch chance
            'pinap': 5   # doubles candy reward on successful catch
        }
        
        # dictionary of evolution stones (name: quantity)
        # stones are used to evolve certain pokemon
        # start with 0 of each - must be found/won
        self.stones = {
            'fire': 0,      # evolves fire-type pokemon
            'water': 0,     # evolves water-type pokemon
            'thunder': 0,   # evolves electric-type pokemon
            'leaf': 0,      # evolves grass-type pokemon
            'moon': 0       # evolves fairy-type pokemon
        }
        
        # poke candy - used to level up pokemon
        # gained by catching pokemon or transferring them to Professor Oak
        self.poke_candy = 0
        
        # badge types - earned by catching pokemon of each type
        # higher badge tiers give bonuses when catching that type
        # dictionary structure: type_name: {'count': number caught, 'tier': badge level}
        self.badges = {
            'normal': {'count': 0, 'tier': None},
            'grass': {'count': 0, 'tier': None},
            'water': {'count': 0, 'tier': None},
            'fire': {'count': 0, 'tier': None},
            'electric': {'count': 0, 'tier': None},
            'psychic': {'count': 0, 'tier': None},
            'fighting': {'count': 0, 'tier': None},
            'poison': {'count': 0, 'tier': None},
            'ground': {'count': 0, 'tier': None},
            'flying': {'count': 0, 'tier': None},
            'bug': {'count': 0, 'tier': None},
            'ghost': {'count': 0, 'tier': None},
            'ice': {'count': 0, 'tier': None},
            'dragon': {'count': 0, 'tier': None},
            'rock': {'count': 0, 'tier': None}
        }
    
    def add_pokeball(self, ball_type, amount=1):
        # ============================================================
        # add pokeballs to inventory from the poke lottery
        # args(ball_type) - which type of ball ('poke', 'great', 'ultra', 'master')
        #     (amount) - how many to add (default 1)    
        # ============================================================
        if ball_type in self.pokeballs:
            self.pokeballs[ball_type] += amount
    
    def use_pokeball(self, ball_type):
        # ============================================================
        # use a pokeball to catch a wild pokemon (removes one from inventory)
        # args(ball_type) - which type of ball to use    
        # returns:true if ball was available and used
        # ============================================================
        # checks if player has this type of ball and has at least 1
        if ball_type in self.pokeballs and self.pokeballs[ball_type] > 0:
            self.pokeballs[ball_type] -= 1
            return True
        return False
    
    def add_berry(self, berry_type, amount=1):
        # ============================================================
        # add berries to the inventory
        # args(berry_type) - which type of berry ('razz', 'pinap')
        #     (amount) - how many to add (default 1)   
        # ============================================================
        if berry_type in self.berries:
            self.berries[berry_type] += amount
    
    def use_berry(self, berry_type):
        # ============================================================
        # use a berry before catching a pokemon(removes one from inventory)
        # args(berry_type) - which type of berry to use
        # returns:true if berry was available and used
        # ============================================================
        # checks if player has this type of berry and has at least 1
        if berry_type in self.berries and self.berries[berry_type] > 0:
            self.berries[berry_type] -= 1
            return True
        return False
    
    def add_stone(self, stone_type, amount=1):
        # ============================================================
        # adds evolution stone to inventory
        # args(stone_type) - which type of stone ('fire', 'water', 'thunder', 'leaf', 'moon')
        #     (amount) - how many to add (default 1) 
        # ============================================================
        if stone_type in self.stones:
            self.stones[stone_type] += amount
    
    def use_stone(self, stone_type):
        # ============================================================
        # Use an evolution stone (removes one from inventory and evolves selected pokemon)
        # args(stone_type) - which type of stone to use
        # returns:true if stone was available and used    
        # ============================================================
        # checks if player has this type of stone and has at least 1
        if stone_type in self.stones and self.stones[stone_type] > 0:
            self.stones[stone_type] -= 1
            return True
        return False
    
    def add_candy(self, amount=1):
        # ============================================================
        # add poke candy to inventory
        # args(amount) - how many candy to add (default 1)     
        # ============================================================
        self.poke_candy += amount
    
    def use_candy(self, amount=1):
        # ============================================================
        # use poke candy (removes from inventory and levels up selected pokemon)
        # args:(amount) how many candy to use (default 1)
        # returns: true if enough candy was available
        # ============================================================
        # checks if player has enough candy
        if self.poke_candy >= amount:
            self.poke_candy -= amount
            return True
        return False 
    
    def update_badge(self, pokemon_type):
        # ============================================================
        # update badge count and tier for catching a pokemon type
        # badge tiers:
        # - bronze: 20+ caught (5% catch bonus, level 15 max spawns)
        # - silver: 40+ caught (10% catch bonus, level 25 max spawns)
        # - gold: 60+ caught (15% catch bonus, level 40 max spawns)
        # args(pokemon_type) - the type of pokemon that was caught   
        # ============================================================
        # check if this is a valid type
        if pokemon_type in self.badges:
            self.badges[pokemon_type]['count'] += 1
            count = self.badges[pokemon_type]['count']
            
            # update tier based on count thresholds
            if count >= 60:
                self.badges[pokemon_type]['tier'] = 'gold'     # best tier
            elif count >= 40:
                self.badges[pokemon_type]['tier'] = 'silver'   # middle tier
            elif count >= 20:
                self.badges[pokemon_type]['tier'] = 'bronze'   # first tier
            # if count < 20, tier stays as none (no badge yet)
    
    def get_badge_bonus(self, pokemon_type):
        # ============================================================
        # used when calculating catch rates and wild pokemon spawns
        # args(pokemon_type) = the type of pokemon being caught
        # returns: tuple of (catch_bonus, max_level)
        #     - catch_bonus: percentage added to catch rate (0.0-0.15)
        #     - max_level: maximum level of wild pokemon that can spawn     
        # ============================================================
        # checks if this is a valid type
        if pokemon_type not in self.badges:
            return 0, 10  # default: no bonus, max level 10
        # get the badge tier for this type
        tier = self.badges[pokemon_type]['tier']
        
        # return bonuses based on tier
        if tier == 'gold':
            return 0.15, 40  # 15% catch bonus, max level 40
        elif tier == 'silver':
            return 0.10, 25  # 10% catch bonus, max level 25
        elif tier == 'bronze':
            return 0.05, 15  # 5% catch bonus, max level 15
        return 0, 10  # no badge: no bonus, max level 10
    
    def show_inventory(self):
        # ============================================================
        # displays all inventory items
        # ============================================================
        print("\n=== INVENTORY ===")
        
        # displays pokeballs section
        print("\n--- Pokéballs ---")
        for ball, count in self.pokeballs.items():
            print(f"  {ball.capitalize()} Ball: {count}")
        
        # displays berries section
        print("\n--- Berries ---")
        for berry, count in self.berries.items():
            print(f"  {berry.capitalize()} Berry: {count}")
        
        # displays evolution stones section
        # only show stones that player has (count > 0)
        print("\n--- Evolution Stones ---")
        stone_found = False  # flag to track if player has any stones
        for stone, count in self.stones.items():
            if count > 0:
                print(f"  {stone.capitalize()} Stone: {count}")
                stone_found = True  # player has at least one stone
        if not stone_found:
            print("  None")
        
        print(f"\n--- Poké Candy: {self.poke_candy} ---") # displays poke Candy
        
        # displays badge types section
        # only show badge types where player has caught pokemon
        print("\n--- Badges ---")
        badge_found = False  # flag to track if player has any badges
        for ptype, data in sorted(self.badges.items()):
            # if the player has earned a badge tier
            if data['tier']:
                print(f"  {ptype.capitalize()}: {data['tier'].upper()} ({data['count']} caught)")
                badge_found = True
            
            elif data['count'] > 0: # if player has caught some pokemon but not enough for a badge
                next_tier = 20 - data['count']  # calculates how many more pokemon are needed
                print(f"  {ptype.capitalize()}: {data['count']} caught ({next_tier} more for Bronze)")
                badge_found = True
        if not badge_found:
            print("  No badges earned yet")