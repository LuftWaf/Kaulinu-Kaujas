import json
import os

class Player:
    def __init__(self, hp=5, hearts=5):
        self.hp = hp            # Health points in battle scene
        self.hearts = hearts    # Hearts on the main screen
        self.max_hearts = 5     # Maximum hearts the player can have
    
    # Method to reduce the player's HP
    def take_damage(self, amount):
        self.hp -= amount
        if self.hp <= 0:
            self.hp = 0
            self.lose_heart()
    
    # Method to heal the player (in case of healing during the battle)
    def heal(self, amount):
        self.hp += amount
        if self.hp > self.max_hearts:
            self.hp = self.max_hearts
    
    # Method to reduce the hearts when the player loses a battle
    def lose_heart(self):
        if self.hearts > 0:
            self.hearts -= 1
    
    # Method to gain a heart (in case of recovery in the main scene)
    def gain_heart(self):
        if self.hearts < self.max_hearts:
            self.hearts += 1
    
    # Method to save the player's data to an external JSON file
    def save_data(self, filename="player_data.json"):
        data = {"hp": self.hp, "hearts": self.hearts}
        with open(filename, "w") as f:
            json.dump(data, f)
    
    # Method to load the player's data from the external JSON file
    @classmethod
    def load_data(cls, filename="player_data.json"):
        if os.path.exists(filename):
            with open(filename, "r") as f:
                data = json.load(f)
            return cls(hp=data.get("hp", 5), hearts=data.get("hearts", 5))
        else:
            return cls()  # Return a new player with default values if no save file exists
    
    # Method to reset the player's data
    def reset(self):
        self.hp = self.max_hearts
        self.hearts = self.max_hearts

# Example Usage
player = Player.load_data()  # Load player's data if available

# When player loses a battle
player.take_damage(1)  # This reduces HP and may cause the player to lose a heart

# When player wins or heals in the battle
player.heal(1)  # This restores HP (up to max hearts)

# Saving the player's progress after changes
player.save_data()

# If the player loses all hearts, reset the data and let them start fresh
if player.hearts == 0:
    player.reset()
    player.save_data()  # Reset the file after losing all hearts
