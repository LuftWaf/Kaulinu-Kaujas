import json
import os

class Player:

    
    def __init__(self, hp=5, hearts=5, cs=0):
        self.hp = hp            # Health points in battle scene
        self.hearts = hearts    # Hearts on the main screen
        self.max_hearts = 5 
        self.completed_stages = cs    # Maximum hearts the player can have
    # Method to reduce the hearts when the player loses a battle
    def lose_heart(self):
        if self.hearts > 0:
            self.hearts -= 1
    
 
    # Method to save the player's data to an external JSON file
    def save_data(self, filename="player_data.json"):
        data = {"hp": self.hp, "hearts": self.hearts, "completed_stages": self.completed_stages}
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
        self.completed_stages = 0

    def reset_player_data(filename="player_data.json"):
        player = Player()  # Create a new player with default values
        player.reset()     # Reset the player's data
        player.save_data(filename)  # Save the reset data to the JSON file
# Example Usage
# player = Player.load_data()  # Load player's data if available

# # Saving the player's progress after changes
# player.save_data()
