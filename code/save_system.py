import json
import os



class SaveSystem:

## charchar start:  Save and load profile data ##
    player_names = []
    selected_index = 0
    wood_cnt = []
    apple_cnt = []
    corn_cnt = []
    tomato_cnt = []


    # loads the json containing player profile
    with open('game_data.json', 'r') as json_src:
            game_info = json.load(json_src)

    for dict_index, inner_dict in game_info.items():
            player_names.append(inner_dict['name'])
            wood_cnt.append(inner_dict['wood'])
            apple_cnt.append(inner_dict['apple'])
            corn_cnt.append(inner_dict['corn'])
            tomato_cnt.append(inner_dict['tomato'])


    for i, name in enumerate(player_names):
        print(f"{i}: {player_names[i]}")


    selected_player = player_names[selected_index]  

    wood_cnt = wood_cnt[selected_index]
    apple_cnt = apple_cnt[selected_index]
    corn_cnt = corn_cnt[selected_index]
    tomato_cnt = tomato_cnt[selected_index]

    print(f"Selected Player Profile: {selected_player}")
    print(f"wood: {wood_cnt}")
    print(f"apple: {apple_cnt}")
    print(f"corn: {corn_cnt}")
    print(f"tomato: {tomato_cnt}")

## charchar end: Save and load profile data ##
   
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
        ## self.data["player_name"] = "Player2-CharChar" 

        self.data["daily_history"].append(day_snapshot)
        self.data["current_day"] += 1
        print("[DEBUG] Starting with " + self.data["player_name"])
        self.save_game()

    def get_last_day(self):
        if self.data["daily_history"]:
            return self.data["daily_history"][-1]
        return None
    
   
    

