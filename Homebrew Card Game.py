### Homebrew Card Game
### Jacque Fong, Joseph Chi, Peyton Yang

"""
# Player hp, damage system, draw card phase
Joseph Chi

# monster cards, combat phase, win/loss/end game
Peyton Yang

UI: #Mana system, deck (linked list), play card phase
Jacque Fong
"""
import random

class Player:
    def __init__(self, health=30, player_id=None):
        """
        Initializes the player's health, mana, and ID.

        Parameters:
        health (int): The health value of the player (default is 30).
        player_id (str or int): The ID of the player (default is None).

        Returns:
        None
        """
        self.health = health
        self.max_mana = 0
        self.mana = 0
        self.player_id = player_id
        self.field = []

    def __str__(self):
        """
        Returns a string representation of the player.

        Parameters:
        None

        Returns:
        str: A string indicating the player ID.
        """
        return f"Player {self.player_id}"

    def gain_mana(self):
        """
        Increases the player's mana each turn, up to a maximum of 10.
        Resets the available mana to the maximum mana value at the time.

        Parameters:
        None

        Returns:
        None
        """
        if self.max_mana < 10:
            self.max_mana += 1
        self.mana = self.max_mana

    def play_card(self, card):
        """
        Allows the player to play a card if they have enough mana.

        Parameters:
        card (Card): The card the player is attempting to play.

        Returns:
        bool: True if the card is playable, False if there isn't enough mana.
        """
        if self.mana >= card.cost:
            self.mana -= card.cost
            return True
        else:
            print(f"Not enough mana to play {card.name}. Mana: {self.mana}")
            return False

    def remove_unit_from_field(self, unit):
        """
        Removes a unit from the player's field, typically when the unit's health reaches 0.

        Parameters:
        unit (UnitCard): The unit to remove.

        Returns:
        None
        """
        if unit in self.field:
            self.field.remove(unit)
            print(f"{self} removed {unit.name} destroyed.")

    def show_field(self):
        """
        Displays the list of units currently on the player's field.

        Parameters:
        None

        Returns:
        None
        """
        if self.field:
            print(f"{self}'s field:")
            for unit in self.field:
                print(f"  - {unit.name}, HP: {unit.current_hp}, Attack: {unit.current_atk}")
        else:
            print(f"{self} has no units on the field.")

    def newHP(self, damageTaken):
        """
        Updates the player's health after taking damage.

        Parameters:
        damageTaken (int): The amount of damage the player has taken.

        Returns:
        None
        """
        self.health -= damageTaken

class Card:
    def __init__(self, name, cost, description):
        """
        Initializes a basic card with name, cost, and description.

        Parameters:
        name (str): The name of the card.
        cost (int): The mana cost of the card.
        description (str): The description of the card.

        Returns:
        None
        """
        self.name = name
        self.cost = cost
        self.description = description

class UnitCard(Card):
    def __init__(self, name, cost, description, base_atk, base_hp, current_atk, current_hp):
        """
        Initializes a unit card, which represents a monster or character.

        Parameters:
        name (str): The name of the unit.
        cost (int): The mana cost of the unit card.
        description (str): The description of the unit.
        base_atk (int): The unit's base attack value.
        base_hp (int): The unit's base health value.
        current_atk (int): The unit's current attack value (can be modified).
        current_hp (int): The unit's current health value (can be modified).
        """
        super().__init__(name, cost, description)
        self.base_atk = base_atk
        self.base_hp = base_hp
        self.current_atk = current_atk
        self.current_hp = current_hp
        self.turns_since_action = 2
        self.update_description()

    def update_description(self):
        """Updates the unit's description to reflect current HP and current attack."""
        # Format the description to include the current_hp dynamically
        self.description = self.description.format(current_hp=self.current_hp)

    def can_act(self):
        """
        Determines if the unit can act based on the number of turns since its last action.

        Parameters:
        None

        Returns:
        bool: True if the unit can act (has waited at least 2 turns), otherwise False.
        """
        return self.turns_since_action >= 2

    def increment_turn(self):
        """
        Increments the number of turns since the unit's last action. This affects its ability to act.

        Parameters:
        None

        Returns:
        None
        """
        self.turns_since_action += 1

    def attackMon(self, player, targetMon, targetMonHp=0):
        """
        Attacks an opponent's monster and applies damage to their health.

        Parameters:
        player (Player): The current player attacking the monster.
        targetMon (UnitCard): The target monster being attacked.
        targetMonHp (int): The current health of the target monster (default is 0).

        Returns:
        None
        """
        self.damageTaken = targetMonHp - self.current_atk
        # Applies damage to the opponent's HP and updates the current HP
        if self.damageTaken < 0:
            player.newHP(abs(self.damageTaken))  # Update player HP if damage taken
        if targetMonHp != 0 and targetMon.current_hp - self.current_atk < 0:
            targetMon.current_hp = 0
            targetMon.update_description()

class SpellCard(Card):
    def __init__(self, name, cost, description, effect_type, effect_value, target_type):
        """
        Initializes the spell card.

        Parameters:
        name (str): The name of the spell card.
        cost (int): The mana cost of the card.
        description (str): The description of the card.
        effect_type (str): Type of the effect (buff, regen, damage, etc.).
        effect_value (int): The value associated with the effect (e.g., buff amount, damage amount).
        target_type (str): The target type for the spell (e.g., "current_player", "opponent").

        Return:
        None
        """
        super().__init__(name, cost, description)
        self.effect_type = effect_type
        self.effect_value = effect_value
        self.target_type = target_type
        self.requires_target = target_type in ["current_player", "opponent"]
        self.description = self.description.format(effect=effect_value)

    def apply_effect(self, target):
        """
        Apply the spell's effect to a target.

        Parameters:
        target (UnitCard or Player): The target of the spell.

        Returns:
        None
        """
        raise NotImplementedError("Cannot utilize non-descript spell cards.")

class BuffSpell(SpellCard):
    def __init__(self, name, cost, description, effect_value):
        """
        Initializes a buff spell card.

        Parameters:
        name (str): The name of the spell card.
        cost (int): The mana cost of the card.
        description (str): The description of the card.
        effect_value (int): The attack value to increase the target's attack by.

        Return:
        None
        """
        super().__init__(name, cost, description, "buff", effect_value, target_type="current_player")

    def apply_effect(self, target):
        """
        Applies the attack buff to the target.

        Parameters:
        target (UnitCard): The target of the buff (must be a unit controlled by the player).
        current_player (Player): The player who is casting the spell.

        Returns:
        None
        """
        if isinstance(target, UnitCard):
            target.current_atk += self.effect_value
            target.current_hp += self.effect_value
            target.update_description()
            print(f"{target.name} gets a buff of {self.effect_value} attack and HP!")
            print(f"New {target.name}: Attack = {target.current_atk}, HP = {target.current_hp}")

class HPRegenSpell(SpellCard):
    def __init__(self, name, cost, description, effect_value):
        """
        Initializes a HP regeneration spell card.

        Parameters:
        name (str): The name of the spell card.
        cost (int): The mana cost of the card.
        description (str): The description of the card.
        effect_value (int): The amount of HP to regenerate.

        Return:
        None
        """
        super().__init__(name, cost, description, "regen", effect_value, target_type="current_player")

    def apply_effect(self, target):
        """
        Applies HP regeneration to the target.

        Parameters:
        target (UnitCard): The target of the HP regen (must be a unit controlled by the player).
        current_player (Player): The player who is casting the spell.

        Returns:
        None
        """
        if isinstance(target, UnitCard):
            target.current_hp += self.effect_value
            print(f"{target.name} regenerates {self.effect_value} HP!")

class DamageSpell(SpellCard):
    def __init__(self, name, cost, description, effect_value):
        """
        Initializes a damage spell card.

        Parameters:
        name (str): The name of the spell card.
        cost (int): The mana cost of the card.
        description (str): The description of the card.
        effect_value (int): The amount of damage to deal.

        Return:
        None
        """
        super().__init__(name, cost, description, "damage", effect_value, target_type="enemy")

    def apply_effect(self, target, current_player, opponent):
        """
        Applies damage to the target, either an enemy unit or the enemy player.
        If the target is a unit and its HP drops to zero or below, remove it from the field.

        Parameters:
        target (UnitCard or Player): The target of the damage (can be any unit or player).
        current_player (Player): The player who is casting the spell.
        opponent (Player): The opponent player.

        Returns:
        None
        """
        if isinstance(target, UnitCard):
            target.current_hp -= self.effect_value
            print(f"{target.name} takes {self.effect_value} damage! Current HP: {target.current_hp}")
            
            # If the monster's HP drops to 0 or below, remove it from the field
            if target.current_hp <= 0:
                print(f"{target.name} has been defeated!")
                # Remove the defeated monster from the opponent's field
                if current_player == current_player:
                    opponent.field.remove(target)
                else:
                    current_player.field.remove(target)
        elif isinstance(target, Player):
            target.newHP(self.effect_value)
            print(f"{target} takes {self.effect_value} damage!")
        else:
            print(f"Invalid target for {self.name}. No damage applied.")
            
class Node:
    def __init__(self, card):
        """
        Initializes a node in the linked list to represent a card in the deck.

        Parameters:
        card (Card): The card to be stored in the node.

        Returns:
        None
        """
        self.card = card
        self.next = None

class Deck:
    def __init__(self):
        """
        Initializes an empty deck represented as a linked list.

        Parameters:
        None

        Returns:
        None
        """
        self.head = None

    def add_card(self, card):
        """
        Adds a new card to the deck (linked list).

        Parameters:
        card (Card): The card to be added to the deck.

        Returns:
        None
        """
        new_node = Node(card)
        if not self.head:
            self.head = new_node
        else:
            current = self.head
            while current.next:
                current = current.next
            current.next = new_node

    def draw_card(self):
        """
        Draws a card from the deck, removing it from the linked list.
        If the deck is empty, returns None.

        Returns:
        Card: The drawn card, or None if the deck is empty.

        Return:
        None
        """
        # Edge-case: No more cards in deck, leads to loss
        if not self.head:
            return None
        drawn_card = self.head.card
        self.head = self.head.next
        return drawn_card

    def format_card(card):
        """
        Formats the card display based on its type.

        Parameters:
        card (Card): The card object to format.

        Returns:
        str: The formatted card string.
        """
        card_info = f"{card.name}, Cost: {card.cost}, Description: {card.description}"
        if isinstance(card, UnitCard):
            card_info += f", Attack: {card.current_atk}, HP: {card.current_hp}"
        return card_info

    def generate_random_deck(self, num_cards=25):
        """
        Generates a deck of number of desired cards based on dictionaries of potential cards.

        Parameters:
        num_cards (int): The number of cards to generate for the deck. Defaults to 25 if not specified.

        Return:
        None 
        """
        unit_types = {
            "Warrior": {"cost": 3, "HP": 5, "attack": 3, "description": "A warrior human with {current_hp} HP"},
            "Tank": {"cost": 5, "HP": 10, "attack": 3, "description": "A tank human with {current_hp} HP"},
            "Assassin": {"cost": 4, "HP": 3, "attack": 7, "description": "An assassin human with {current_hp} HP"},
            "Goblin": {"cost": 1, "HP": 1, "attack": 1, "description": "A goblin unit with {current_hp} HP"},
            "Mage": {"cost": 2, "HP": 2, "attack": 4, "description": "A mage human with {current_hp} HP"}
        }
        damage_spells = {
            "Fireball": {"cost": 2, "effect": 3, "description": "Fireball spell deals {effect} damage to one target."},
            "Blizzard": {"cost": 5, "effect": 6, "description": "Blizzard spell deals {effect} damage to one target."},
            "Armageddon": {"cost": 10, "effect": 10, "description": "Armageddon spell deals {effect} damage to one target."}
        }
        hp_regen_spells = {
            "Steelskin": {"cost": 2, "effect": 4, "description": "Steelskin increases Health of a target by {effect}."},
            "Overheal": {"cost": 4, "effect": 8, "description": "Overheal increases Health of a target by {effect}."}
        }
        buff_spells = {
            "Enrage": {"cost": 3, "effect": 2, "description": "Enrage increases attack of a target by {effect}."},
            "Berserk": {"cost": 5, "effect": 5, "description": "Berserk increases attack of a target by {effect}."}
        }
        for _ in range(num_cards):
            if random.random() < 0.5:
                card_type = random.choice(list(unit_types.keys()))
                unit = unit_types[card_type]
                base_attack = unit["attack"]
                base_HP = unit["HP"]
                current_hp = base_HP  # Initialize current_hp as base_HP

                # Set the description with current_hp
                description = unit["description"].format(current_hp=current_hp)
                
                # Create the UnitCard object
                card = UnitCard(
                    card_type,
                    unit["cost"],
                    description,
                    base_attack,
                    base_HP,
                    base_attack,
                    base_HP
                )
                card.update_description()
            else:
                spell_type = random.choice([damage_spells, hp_regen_spells, buff_spells])
                if spell_type == damage_spells:
                    spell_name = random.choice(list(damage_spells.keys()))
                    spell = damage_spells[spell_name]
                    card = DamageSpell(
                        spell_name,
                        spell["cost"],
                        spell["description"].format(effect=spell["effect"]),
                        spell["effect"]
                    )
                elif spell_type == hp_regen_spells:
                    spell_name = random.choice(list(hp_regen_spells.keys()))
                    spell = hp_regen_spells[spell_name]
                    card = HPRegenSpell(
                        spell_name,
                        spell["cost"],
                        spell["description"].format(effect=spell["effect"]),
                        spell["effect"]
                    )
                else:
                    spell_name = random.choice(list(buff_spells.keys()))
                    spell = buff_spells[spell_name]
                    card = BuffSpell(
                        spell_name,
                        spell["cost"],
                        spell["description"].format(effect=spell["effect"]),
                        spell["effect"]
                    )
            self.add_card(card)

def combat_phase(attackers, defenders, player, opponent):
    """
    Conduct the combat phase where attackers choose which monsters to attack with,
    and defenders choose which monsters to block with.
    After the battle, any monsters with 0 HP are removed from the field.

    Parameters:
    attackers (list): list of attacking monsters from the current player's field
    defenders (list): list of defending monsters from the opponent's field
    player (Player): the attacking player
    opponent (Player): the defending player

    Return:
    None
    """
    # Attacker selects attacking monsters
    print("\nAttacker's Turn:")
    attacker_list = []
    # Only include attackers who have waited at least 2 turns
    applicable_attackers = [monster for monster in attackers if monster.turns_since_action >= 2]
    # Keep track of monsters already selected for attack
    selected_attackers = set()
    while applicable_attackers:
        print("Available Attackers:")
        for idx, monster in enumerate(applicable_attackers, 1):
            print(f"{idx}) {monster.name} - Attack: {monster.current_atk}, HP: {monster.current_hp}")
        selected_attacker = input("\nSelect an attacker to use (or 0 to finish selecting): ")
        if selected_attacker.isnumeric():
            selected_attacker = int(selected_attacker)
            if selected_attacker == 0:
                break
            elif 1 <= selected_attacker <= len(applicable_attackers):
                attacker = applicable_attackers[selected_attacker - 1]
                if attacker.turns_since_action < 2:
                    print(f"{attacker.name} cannot attack this turn because it has recently acted.")
                elif attacker in selected_attackers:
                    print(f"{attacker.name} has already been selected for attack.")
                else:
                    attacker_list.append(attacker)
                    selected_attackers.add(attacker)
                    applicable_attackers.remove(attacker)
                    print(f"{attacker.name} added to the attack list.")
            else:
                print("Invalid choice. Please select a valid attacker.")
        # If no more attackers are left to select, skip to defender selection
        if not applicable_attackers:
            print("All attackers selected, moving to the Defender's Turn.")
            break
    # If no attackers were selected, skip to the next turn
    if not attacker_list:
        print("No attackers selected, skipping Battle Phase.")
        return
    
    # Defender selects defenders to block attackers
    print("\nDefender's Turn:")
    defender_list = [None] * len(attacker_list)  # Ensure defender_list matches the size of attacker_list
    # If defender has no monsters, skip defender selection phase
    if not defenders:
        print("Defender has no monsters. All attacks will go through directly.")
        for i in range(len(attacker_list)):
            defender_list[i] = None  # No defenders, all attacks go through
    else:
        applicable_defenders = [monster for monster in defenders if monster.turns_since_action >= 2]
        selected_defenders = set()
        while len(selected_defenders) < len(attacker_list):  # Ensure defenders match attackers
            print("\nAvailable Defenders:")
            for idx, defender in enumerate(applicable_defenders, 1):
                print(f"{idx}) {defender.name} - Attack: {defender.current_atk}, HP: {defender.current_hp}")
            # For each attacker, let the defender decide which monster to block
            for i in range(len(attacker_list)):
                if defender_list[i] is None:  # Only ask for a defender if one hasn't been assigned yet
                    print(f"\nFor {attacker_list[i].name}'s attack, do you want to block?")
                    defender_choice = input(f"Choose a defender for {attacker_list[i].name} (or 0 to skip): ")
                    if defender_choice.isnumeric():
                        defender_choice = int(defender_choice)
                        if 0 <= defender_choice <= len(applicable_defenders):
                            if defender_choice == 0:
                                defender_list[i] = None
                                print(f"{attacker_list[i].name} will deal damage directly to the opponent.")
                            else:
                                defender = applicable_defenders[defender_choice - 1]
                                if defender.turns_since_action >= 2 and defender not in selected_defenders:
                                    defender_list[i] = defender
                                    selected_defenders.add(defender)
                                    applicable_defenders.remove(defender)
                                    print(f"{attacker_list[i].name} will attack {defender.name}.")
                                elif defender in selected_defenders:
                                    print(f"{defender.name} has already been selected to block another attacker.")
                                else:
                                    print(f"{defender.name} cannot defend this turn, please select another defender.")
                        else:
                            print("Invalid choice. Please select a valid defender.")
                    else:
                        print("Invalid input. Please enter a number.")
            # If all attackers have a defender, break out of loop
            if all(defender is not None for defender in defender_list):
                print("All defenders selected, moving to the Battle Phase.")
                break
    # If no defenders selected, skip to battle phase
    if not any(defender_list):
        print("No defenders selected, all attacks go through.")
    
    # Battle Phase
    print("\nBattle Phase:")
    total_damage_to_player = 0
    total_damage_to_opponent = 0
    for i in range(len(attacker_list)):
        attacker = attacker_list[i]
        defender = defender_list[i]
        if defender:
            # Defender blocks the attacker
            print(f"{attacker.name} attacks {defender.name}!")
            attacker.attackMon(opponent, defender, defender.current_hp)
            # Calculates residual damage to players
            attacker_damage = max(0, attacker.current_atk - defender.current_hp)
            defender_damage = max(0, defender.current_atk - attacker.current_hp)
            # Apply the damage to the monsters
            attacker.current_hp -= defender.current_atk
            defender.current_hp -= attacker.current_atk
            # Residual damage is applied to the player
            if defender.current_hp <= 0:
                print(f"{defender.name} has been defeated!")
                total_damage_to_player += attacker_damage
            if attacker.current_hp <= 0:
                print(f"{attacker.name} has been defeated!")
                total_damage_to_opponent += defender_damage
        else:
            # No defender, direct damage to the opponent
            print(f"{attacker.name} attacks directly!")
            total_damage_to_player += attacker.current_atk
        
        # After the attack, set `turns_since_action` to 0
        attacker.turns_since_action = 0  # Reset turn counter after the action
        if defender:
            defender.turns_since_action = 0  # Reset defender's turn counter after defending
    
    # Apply damage to players
    if total_damage_to_player > 0:
        print(f"\n{total_damage_to_player} damage goes through to the opponent!")
        opponent.newHP(total_damage_to_player)
    if total_damage_to_opponent > 0:
        print(f"\n{total_damage_to_opponent} damage goes through to the attacker!")
        player.newHP(total_damage_to_opponent)
    
    # Output both players' HP
    print(f"\n{player} has {player.health} HP remaining.")
    print(f"{opponent} has {opponent.health} HP remaining.")
    
    # Remove any monsters with 0 HP
    print("\nRemoving defeated monsters from the field:")
    for field in [player.field, opponent.field]:
        for monster in field[:]:
            if monster.current_hp <= 0:
                print(f"{monster.name} has been removed from the field.")
                field.remove(monster)

    # Increment turns since action for all monsters
    for monster in attackers + defenders:
        if monster.turns_since_action < 2:
            monster.turns_since_action += 1

def new_game():
    """
    Starts a new card game, initializing players, decks, and game loop.

    Parameters:
    None

    Returns:
    None
    """
    player1 = Player(player_id=1)
    player2 = Player(player_id=2)
    deck1 = Deck()
    deck2 = Deck()
    deck1.generate_random_deck(25)
    deck2.generate_random_deck(25)
    players = [player1, player2]
    turn = 0
    player1hand = []
    player2hand = []
    for _ in range(5):
        player1hand.append(deck1.draw_card())
        player2hand.append(deck2.draw_card())
    while True:
        current_player = players[turn % 2]
        opponent = players[(turn + 1) % 2]
        current_player.gain_mana()
        print(f"\n==== Turn {turn + 1} ====")
        print(f"\nTurn {turn + 1}: Player {1 if current_player == player1 else 2}'s turn")
        print(f"{current_player} has {current_player.health} HP.")
        print(f"{current_player} has {current_player.mana} mana.")
        # Draw card phase (try to draw a card after gaining mana)
        if current_player == player1:
            # Checks if player is able to draw cards, if no more cards in deck, player loses
            new_card = deck1.draw_card()
            if new_card is None:
                print(f"{current_player} cannot draw a card and loses the game!")
                break
            if len(player1hand) >= 9:
                print(f"{current_player} draws {new_card.name}, but discards it as they already have 9 cards in hand.")
            else:
                player1hand.append(new_card)
        elif current_player == player2:
            new_card = deck2.draw_card()
            if new_card is None:
                print(f"{current_player} cannot draw a card and loses the game!")
                break
            if len(player2hand) >= 9:
                print(f"{current_player} draws {new_card.name}, but discards it as they already have 9 cards in hand.")
            else:
                player2hand.append(new_card)
        # Play cards phase (loop until player no longer wants to play cards)
        while current_player.mana > 0:
            print(f"\nMana available: {current_player.mana}")
            print(f'Select a card to play, forfeit (type "forfeit"), or 0 to pass:')
            
            hand_to_use = player1hand if current_player == player1 else player2hand
            for i, c in enumerate(hand_to_use, 1):
                if isinstance(c, UnitCard):
                    print(f"{i}): {c.name}, Cost: {c.cost}, Attack: {c.current_atk}, HP: {c.current_hp}, Description: {c.description}")
                else:
                    print(f"{i}): {c.name}, Cost: {c.cost}, Description: {c.description}")
            print(f"0): Stop playing cards")
            selectedCard = input(">> ").strip().lower()
            if selectedCard == "forfeit":
                print(f"{current_player} forfeits the game. {opponent} wins!")
                return
            elif selectedCard.isnumeric():
                selectedCard = int(selectedCard)
                if selectedCard == 0:
                    break
                elif selectedCard <= len(hand_to_use) and selectedCard > 0:
                    selectedCard = hand_to_use[selectedCard - 1]
                    if isinstance(selectedCard, UnitCard):
                        if current_player.mana >= selectedCard.cost:
                            # Deduct mana AFTER ensuring the card is valid to play
                            current_player.mana -= selectedCard.cost
                            print(f"{current_player} plays {selectedCard.name} to the field!")
                            hand_to_use.remove(selectedCard)
                            current_player.field.append(selectedCard)
                            print(f"Remaining mana: {current_player.mana}")
                        else:
                            print(f"{current_player} doesn't have enough mana to play {selectedCard.name}.")
                    elif isinstance(selectedCard, SpellCard):
                        print(f"Applying effect of {selectedCard.name}.")
                        valid_target = True
                        if isinstance(selectedCard, DamageSpell):
                            if selectedCard.target_type == 'enemy':
                                if len(opponent.field) == 0:
                                    print("No enemies on the field, targeting the opponent directly.")
                                    selectedCard.apply_effect(opponent, current_player, opponent)
                                else:
                                    print("Select a unit to target from the opponent's field:")
                                    for idx, unit in enumerate(opponent.field, 1):
                                        print(f"{idx}): {unit.name} - HP: {unit.current_hp}")
                                    print(f"0): Target opponent directly.")
                                    target_idx = input("Select target (number): ")
                                    if target_idx.isnumeric() and 1 <= int(target_idx) <= len(opponent.field):
                                        target = opponent.field[int(target_idx) - 1]
                                        selectedCard.apply_effect(target, current_player, opponent)
                                    elif target_idx == "0":
                                        selectedCard.apply_effect(opponent, current_player, opponent)
                                    else:
                                        print("Invalid target. No mana used.")
                                        valid_target = False
                        elif isinstance(selectedCard, BuffSpell):
                            if len(current_player.field) == 0:
                                print(f"No monsters on your field to target with the Buff spell. You have {current_player.mana} mana.")
                                valid_target = False
                            else:
                                print("Select a monster to target from your field:")
                                for idx, unit in enumerate(current_player.field, 1):
                                    print(f"{idx}): {unit.name} - HP: {unit.current_hp}")
                                target_idx = input("Select target (number): ")
                                if target_idx.isnumeric() and 1 <= int(target_idx) <= len(current_player.field):
                                    target = current_player.field[int(target_idx) - 1]
                                    selectedCard.apply_effect(target)
                                    target.update_description()
                                else:
                                    print(f"Invalid target. You have {current_player.mana} mana. No mana used.")
                                    valid_target = False
                        elif isinstance(selectedCard, HPRegenSpell):
                            if len(current_player.field) == 0:
                                print(f"No monsters on your field to target with the HP Regen spell. You have {current_player.mana} mana.")
                                valid_target = False
                            else:
                                print("Select a monster to target from your field:")
                                for idx, unit in enumerate(current_player.field, 1):
                                    print(f"{idx}): {unit.name} - HP: {unit.current_hp}")
                                target_idx = input("Select target (number): ")
                                if target_idx.isnumeric() and 1 <= int(target_idx) <= len(current_player.field):
                                    target = current_player.field[int(target_idx) - 1]
                                    selectedCard.apply_effect(target)
                                else:
                                    print(f"Invalid target. You have {current_player.mana} mana. No mana used.")
                                    valid_target = False
                        if valid_target:
                            current_player.mana -= selectedCard.cost
                            hand_to_use.remove(selectedCard)
                            print(f"Remaining mana: {current_player.mana}")
                        # After card is played, display the field state
                        print("\n--- Field State ---")
                        print(f"{current_player}'s Field:")
                        if len(current_player.field) > 0:
                            for unit in current_player.field:
                                unit.update_description()
                                print(f"{unit.name} - HP: {unit.current_hp} Attack: {unit.current_atk}")
                        else:
                            print("No monsters on your field.")
                        print(f"\n{opponent}'s Field:")
                        if len(opponent.field) > 0:
                            for unit in opponent.field:
                                unit.update_description()
                                print(f"{unit.name} - HP: {unit.current_hp} Attack: {unit.current_atk}")
                        else:
                            print("No monsters on opponent's field.")
                    else:
                        print("Invalid card selection.")
                else:
                    print(f"Invalid card selection. You have {current_player.mana} mana.")
            else:
                print(f"Invalid input. You have {current_player.mana} mana.")
        # Combat phase
        if len(current_player.field) == 0:
            print(f"\n{current_player} has no units on the field. Skipping combat phase.")
        else:
            print(f"\nCombat phase between {current_player} and {opponent}.")
            combat_phase(current_player.field, opponent.field, current_player, opponent)
        # Reset monsters' stats to their default values
        print(f"\nResetting all monsters' stats to their default values.")
        for field in [player1.field, player2.field]:
            for monster in field:
                monster.current_atk = monster.base_atk
                monster.current_hp = monster.base_hp
                print(f"{monster.name} is reset to {monster.base_atk} attack and {monster.base_hp} HP.")
        # End of turn
        turn += 1
        # Check if the game ends (any player has no health left)
        if player1.health <= 0 and player2.health <= 0:
            print(f"Both players have 0 health. Tie game!")
            break
        elif player1.health <= 0:
            print(f"player 1 loses! Player 2 wins!")
            break
        elif player2.health <= 0:
            print(f"player 1 wins! Player 2 loses!")
            break

if __name__ == "__main__":
    new_game()