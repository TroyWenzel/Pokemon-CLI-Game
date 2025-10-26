# this file manages wild pokemon encounters
# tt determines which pokemon appear, their levels, rarity, and catch rates

import random 

class HuntingSystem:
    # ============================================================
    # manages wild pokemon encounters and rarity mechanics
    # this system handles:
    # - generating random wild pokemon based on rarity
    # - determining pokemon levels based on player badges
    # - calculating catch rates with various modifiers
    # ============================================================
    # These lists are used to determine spawn rates and catch difficulty
    
    # starter pokemon and their evolutions (Bulbasaur, Charmander, Squirtle lines)
    STARTERS = [1, 2, 3, 4, 5, 6, 7, 8, 9]
    
    # fossil pokemon and their evolutions (Omanyte, Omastar, Kabuto, Kabutops)
    FOSSILS = [138, 139, 140, 141]
    
    # eeveelutions (Vaporeon, Jolteon, Flareon)
    EEVEELUTIONS = [134, 135, 136]
    
    # dragon type pokemon (Dratini, Dragonair, Dragonite)
    DRAGONS = [147, 148, 149]
    
    # legendary pokemon (Articuno, Zapdos, Moltres, Mewtwo, Mew)
    # these are the rarest pokemon in the game
    LEGENDARIES = [144, 145, 146, 150, 151]
    
    # combine all rare pokemon into one list (everything except legendaries)
    RARE_POKEMON = STARTERS + FOSSILS + EEVEELUTIONS + DRAGONS
    
    def __init__(self):
        # ============================================================
        # initialize the hunting system
        # ============================================================
        self.wild_pokemon = None  # currently encountered pokemon
    
    def generate_wild_pokemon(self, badge_tier_data):
        # ============================================================
        # generate a wild pokemon based on rarity and badge levels
        # uses weighted random selection for different rarity tiers
        # args(badge_tier_data) - dictionary of badge bonuses for each type
        # returns: tuple of (pokemon_id, level)
        # ============================================================
        # roll a random number to determine rarity tier
        roll = random.random()  # returns float between 0.0 and 1.0
        
        # legendary pokemon: 0.1% chance (roll < 0.001)
        if roll < 0.001:
            pokemon_id = random.choice(self.LEGENDARIES)  # pick random legendary
            level = random.randint(40, 50)  # legendaries spawn at high levels
        
        # rare pokemon: 5% chance (roll < 0.05, but not legendary)
        elif roll < 0.05:
            pokemon_id = random.choice(self.RARE_POKEMON)  # pick random rare pokemon
            # get max level based on player's badges
            max_level = self._get_max_level_for_pokemon(pokemon_id, badge_tier_data)
            level = random.randint(5, min(max_level, 30))  # level 5-30
        
        # common pokemon: 94.9% chance (everything else)
        else:
            # create pool of all pokemon except legendaries
            common_pool = [i for i in range(1, 152) if i not in self.LEGENDARIES]
            pokemon_id = random.choice(common_pool)  # pick random common pokemon
            # get max level based on player's badges
            max_level = self._get_max_level_for_pokemon(pokemon_id, badge_tier_data)
            level = random.randint(1, max_level)  # Level 1 to max_level
        
        return pokemon_id, level
    
    def _get_max_level_for_pokemon(self, pokemon_id, badge_tier_data):
        # ============================================================
        # get max level for pokemon based on its type and player's badges
        # higher badge tiers allow higher level pokemon to spawn
        # args(pokemon_id) the pokemon's ID number
        #     (badge_tier_dat) dictionary of badge bonuses for each type
        # returns: maximum level this pokemon can spawn at (10-50)
        # ============================================================
        max_level = 10  # default: level 10 max with no badges
        
        # check all badge tiers and find the highest max level
        if badge_tier_data:
            # get list of all max levels from badges (ignoring the catch bonus)
            max_levels = [data[1] for data in badge_tier_data.values() if data[1] > max_level]
            if max_levels:
                max_level = max(max_levels)
        
        # ensure max_level is between 10 and 50(for now)
        return max(10, min(max_level, 50))
    
    def calculate_catch_rate(self, pokemon_id, pokemon_level, ball_type, badge_bonus, berry_used=None):
        # ============================================================
        # calculate catch rate for a pokemon - multiple factors affect catch difficulty
        # args(pokemon_id) - the pokemon's ID number
        #     (pokemon_level) - the pokemon's current level
        #     (ball_type) - which pokeball is being used
        #     (badge_bonus) - bonus from type badge (0.0-0.15)
        #     (berry_used) - which berry was used, if any ('razz' or None)    
        # returns: final catch rate as a float (0.05-0.95, meaning 5%-95%)  
        # ============================================================
        # base catch rates for different pokeballs
        base_rates = {
            'poké': 0.25,                    # 25% base rate
            'great': 0.25 * 1.5,             # 37.5% base rate (50% better)
            'ultra': 0.25 * 1.5 * 1.5,       # 56.25% base rate (125% better)
            'master': 0.25 * 1.5 * 1.5 * 1.6  # 90% base rate (260% better)
        }
        
        # start with base rate for selected ball
        catch_rate = base_rates.get(ball_type, 0.25)
        
        # add badge bonus (0-15% depending on badge tier)
        catch_rate += badge_bonus
        
        # add berry bonus if razz berry was used
        if berry_used == 'razz':
            catch_rate += 0.10  # +10% catch rate
        
        # subtract level penalty (harder to catch higher level pokemon)
        level_penalty = (pokemon_level - 1) * 0.002 # each level above 1 reduces catch rate by 0.2%
        catch_rate -= level_penalty
        
        # applying rarity penalties
        if pokemon_id in self.LEGENDARIES: # legendary pokemon are much harder to catch
            catch_rate -= 0.20 
        elif pokemon_id in self.RARE_POKEMON: # rare pokemon are harder to catch
            catch_rate -= 0.05
        
        # catch rate between 5% and 95%
        catch_rate = max(0.05, min(0.95, catch_rate))
        
        # no pokemon is impossible to catch, and none are guaranteed
        return catch_rate
    
    def attempt_catch(self, catch_rate):
        # ============================================================
        # attempt to catch pokemon with given catch rate - catch succeeds, fails, or pokemon flees
        # args(catch_rate) probability of successful catch (0.0-1.0)
        # returns:string result - 'caught', 'failed', or 'fled'   
        # ============================================================
        # roll for catch success
        roll = random.random()  # random float between 0.0 and 1.0
        
        if roll < catch_rate:
            return 'caught'  # success! pokemon was caught
        else:
            # catch failed - 25% chance pokemon flees
            if random.random() < 0.25:
                return 'fled'  # pokemon ran away
            return 'failed'  # pokemon broke free but stayed
    
    def is_pokemon_rare(self, pokemon_id):
        # ============================================================
        # checks if pokemon is in the rare category - (starters and their evolutions, fossils, eeveelutions, and dragons) 
        # args(pokemon_id) - the pokemon's ID number
        # returns: true if rare    
        # ============================================================
        return pokemon_id in self.RARE_POKEMON
    
    def is_pokemon_legendary(self, pokemon_id):
        # ============================================================
        # checks if pokemon is legendary
        # args(pokemon_id) - the pokemon's ID number  
        # returns: true if legendary
        # ============================================================
        return pokemon_id in self.LEGENDARIES