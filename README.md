Pokémon CLI Adventure
A command-line Pokémon game inspired by the classic Pokémon Red/Blue and Pokémon Go, built in Python. Catch, train, and evolve Pokémon while filling your Pokédex!

Features
🎮 Core Gameplay
Catch Wild Pokémon: Encounter random Pokémon while hunting in tall grass

Rarity System: Common, rare (starters, fossils, eeveelutions, dragons), and legendary (Articuno, Zapdos, Moltres, Mewtwo, Mew) Pokémon

Pokédex: Track which Pokémon you've seen and caught across all 151 Gen 1 Pokémon

Evolution System: Pokémon evolve through leveling up or using evolution stones

Badge System: Earn type badges by catching multiple Pokémon of the same type

🎯 Catching Mechanics
Multiple Pokéball types with different catch rates:

Poké Ball (25% base)

Great Ball (37.5% base)

Ultra Ball (56.25% base)

Master Ball (90% base)

Berries for catching bonuses:

Razz Berry: +10% catch chance

Pinap Berry: Double candy reward on successful catch

Badge bonuses improve catch rates for specific types

Higher level Pokémon are harder to catch

📦 Inventory System
Pokéballs: Standard, Great, Ultra, and Master Balls

Berries: Razz and Pinap berries

Evolution Stones: Fire, Water, Thunder, Leaf, and Moon stones

Poké Candy: Used to level up Pokémon (1 candy = 1 level)

Badges: Bronze/Silver/Gold tiers for each Pokémon type

💾 Collection Management
Poké Belt: Carry up to 6 active Pokémon

PC Storage: Unlimited storage for extra Pokémon

Professor Oak: Transfer unwanted Pokémon for Poké Candy

🎁 Bonus Features
Poké Lottery: Daily chance to win free items

Stone Drops: Certain Pokémon have a 5% chance to drop evolution stones when caught

Shiny Pokémon: Random chance for shiny encounters

Rare Encounters: Starters, fossils, and legendary Pokémon have lower spawn rates

Installation
Prerequisites
Python 3.6 or higher

pip (Python package installer)

Setup
Clone or download the project files

Install required dependencies

bash
pip install requests colorama
Run the game

bash
python main_game.py
How to Play
Getting Started
Run python main_game.py

Enter your trainer name when prompted

Choose your starter Pokémon (Bulbasaur, Charmander, or Squirtle)

Begin your adventure from the main menu!

Main Menu Options
Option	Description
1. Go hunting	Find and catch wild Pokémon
2. View Poké Belt	Manage your active party (max 6)
3. View Poké PC	Access your Pokémon storage
4. View Inventory	Check items, use evolution stones, play lottery
5. View Pokédex	Track seen/caught Pokémon (all 151)
6. Quit game	Exit the game
Hunting Encounters
When you encounter a wild Pokémon, you have three options:

Use Berry (before catching)

Razz Berry: +10% catch chance

Pinap Berry: Double candy reward

Throw Pokéball

Choose which ball to use

Catch rate displayed before attempt

Pokémon may break free or flee

Run Away

Escape the encounter

Pokémon Management
In Belt/PC menus you can:

View Pokémon stats

Level up using Poké Candy

Evolve Pokémon (automatic at level thresholds)

Transfer to Professor Oak (for 1 candy)

Move between Belt and PC

Evolution Stones
Use stones from the Inventory menu on compatible Pokémon:

Fire Stone: Vulpix → Ninetales, Growlithe → Arcanine, Eevee → Flareon

Water Stone: Poliwhirl → Poliwrath, Shellder → Cloyster, Staryu → Starmie, Eevee → Vaporeon

Thunder Stone: Pikachu → Raichu, Eevee → Jolteon

Leaf Stone: Gloom → Vileplume, Weepinbell → Victreebel, Exeggcute → Exeggutor

Moon Stone: Nidorina → Nidoqueen, Nidorino → Nidoking, Clefairy → Clefable, Jigglypuff → Wigglytuff

Badge System
Catch multiple Pokémon of the same type to earn badges:

Tier	Caught	Bonus
Bronze	20+	+5% catch rate, max level 15 spawns
Silver	40+	+10% catch rate, max level 25 spawns
Gold	60+	+15% catch rate, max level 40 spawns
Rarity Tiers
Tier	Chance	Examples
Common	94.9%	Most Pokémon (Pidgey, Rattata, etc.)
Rare	5%	Starters, fossils, eeveelutions, dragons
Legendary	0.1%	Articuno, Zapdos, Moltres, Mewtwo, Mew
File Structure
text
pokemon_cli/
├── main_game.py      # Main game loop and menu system
├── pokemon.py        # Pokemon class and evolution data
├── player.py         # Player inventory (belt/PC management)
├── inventory.py      # Items, badges, and resources
├── pokedex.py        # Pokédex tracking and lottery
├── hunting_pokemon.py # Wild encounter system
└── README.md         # This file
API Integration
This game uses the PokéAPI to fetch real Pokémon data including:

Base stats (HP, Attack, Defense, Speed)

Types

Available moves

Sprites

If the API is unavailable, the game falls back to default data to ensure uninterrupted gameplay.

Tips & Tricks
Save your Master Balls for legendary encounters (0.1% chance!)

Use Pinap Berries on rare Pokémon to double candy rewards

Evolve strategically - some Pokémon learn better moves before evolving

Grind badges to increase spawn levels and catch rates

Check the lottery daily for free items

Transfer duplicates to Professor Oak for extra candy

Known Limitations
Currently only Gen 1 Pokémon (1-151)

No trainer battles (wild encounters only)

Simplified battle system (no actual combat yet)

Moves are for display only

Future Enhancements
Full battle system with type effectiveness

Trainer battles and gym leaders

Trading system

Day/night cycle for different spawns

More regions (Johto, Hoenn, etc.)

Save/load game functionality

Item crafting system

Troubleshooting
Issue: "Module not found: requests/colorama"
Solution: Run pip install requests colorama

Issue: Game crashes when encountering Pokémon
Solution: Check internet connection (requires PokéAPI access)

Issue: Colors not displaying correctly in terminal
Solution: Some terminals may not support ANSI colors. Try running in a modern terminal (Windows Terminal, iTerm2, etc.)

Credits
Pokémon data provided by PokéAPI

Color output using Colorama

Inspired by Pokémon Red/Blue and Pokémon Go

Enjoy your Pokémon adventure, Trainer! 🎮✨
