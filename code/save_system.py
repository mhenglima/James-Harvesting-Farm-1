import json
import os

class SaveSystem:
    def __init__(self, save_file='save_data.json'):
        self.save_file = save_file
        self.data = {
            "current_day": 1,
            "daily_history": []
        }
        self.load_game()

    def load_game(self):
        if os.path.exists(self.save_file):
            with open(self.save_file, 'r') as file:
                self.data = json.load(file)
        else:
            self.save_game()

    def save_game(self):
        with open(self.save_file, 'w') as file:
            json.dump(self.data, file, indent=4)

    def record_day(self, day, inventory, seed_inventory, money):
        print(f"[DEBUG] Saving Day {day}: Inventory={inventory}, Seeds={seed_inventory}, Money={money}")
        """Save the current day's inventory and money."""
        day_snapshot = {
            "day": day,
            "inventory": inventory,
            "seed_inventory": seed_inventory,
            "money": money
        }
        self.data["daily_history"].append(day_snapshot)
        self.data["current_day"] += 1
        self.save_game()

    def get_last_day(self):
        if self.data["daily_history"]:
            return self.data["daily_history"][-1]
        return None
