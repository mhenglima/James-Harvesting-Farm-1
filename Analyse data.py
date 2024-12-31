import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.font_manager as fm
import json
import os

# 📥 Load Data from JSON File
with open('save_data.json', 'r') as file:
    data = json.load(file)

# 📊 Extract Data Dynamically
days = []
money = []
inventory_data = {}

for day_data in data.get("daily_history", []):
    days.append(day_data.get("day", None))
    money.append(day_data.get("money", None))
    
    inventory = day_data.get("inventory", {})
    for item, value in inventory.items():
        if item not in inventory_data:
            inventory_data[item] = []
        inventory_data[item].append(value)
    
    # Ensure missing inventory keys are appended with None for consistency
    for existing_item in inventory_data.keys():
        if existing_item not in inventory:
            inventory_data[existing_item].append(None)

# 📝 Create a DataFrame Dynamically
df_data = {"Day": days, "Money": money}
df_data.update(inventory_data)

df = pd.DataFrame(df_data)

# Fill missing data with forward fill for smoother analysis
df.ffill(inplace=True)

# 💵 Calculate Spending Patterns
df['Daily_Spending'] = df['Money'].diff().fillna(0)
df['Purchase_Action'] = df['Daily_Spending'].apply(
    lambda x: 'Spent Money 🛒' if x < 0 else ('Earned Money 💰' if x > 0 else 'No Change')
)

# 📂 Ensure Client Folder Exists
output_folder = os.path.join(os.getcwd(), 'client')
os.makedirs(output_folder, exist_ok=True)

# 🛠️ Load Emoji-Supporting Font
font_path = "C:/Windows/Fonts/seguiemj.ttf"  # Path to emoji font (Windows default)
if not os.path.exists(font_path):
    raise FileNotFoundError("Emoji font not found! Ensure 'Segoe UI Emoji' is installed.")

emoji_font = fm.FontProperties(fname=font_path)

# 🎨 Child-Friendly Plot
fig, ax = plt.subplots(2, 1, figsize=(12, 10))
fig.patch.set_facecolor('#FFF7C2')

# 💵 Money Trend Analysis
ax[0].plot(df['Day'], df['Money'], marker='o', linestyle='-', color='#FFD700', label='Money Over Time')
ax[0].set_title('💰 Your Money Adventure 💰', fontsize=16, color='#6A5ACD', fontproperties=emoji_font)
ax[0].set_xlabel('📅 Day', fontsize=12, fontproperties=emoji_font)
ax[0].set_ylabel('💵 Money', fontsize=12, fontproperties=emoji_font)
ax[0].legend(prop=emoji_font)
ax[0].grid(True, color='lightgray', linestyle='--')

# 📦 Inventory Changes
colors = ['#FF4500', '#32CD32', '#1E90FF', '#DA70D6']
for idx, (resource, color) in enumerate(zip(inventory_data.keys(), colors)):
    ax[1].plot(df['Day'], df[resource], marker='o', linestyle='-', label=f'{resource.capitalize()}', color=color)
ax[1].set_title('🧺 Your Farm Friends Collection 🧺', fontsize=16, color='#6A5ACD', fontproperties=emoji_font)
ax[1].set_xlabel('📅 Day', fontsize=12, fontproperties=emoji_font)
ax[1].set_ylabel('📦 Inventory Count', fontsize=12, fontproperties=emoji_font)
ax[1].legend(prop=emoji_font)
ax[1].grid(True, color='lightgray', linestyle='--')

# 📊 Save Plot
output_file = os.path.join(output_folder, 'kids_farm_analysis.png')
plt.tight_layout()
plt.savefig(output_file, bbox_inches='tight', dpi=72)  # Reduced DPI
plt.close(fig)

# 🧠 Recommendations for Kids Based on Inventory
recommendations = []

if 'apple' in df.columns and df['apple'].mean() < 5:
    recommendations.append('🍎 Cut more apple trees for a sweet harvest!')
if 'corn' in df.columns and df['corn'].mean() < 3:
    recommendations.append('🌽 Grow more corn to feed your farm friends!')
if 'tomato' in df.columns and df['tomato'].mean() < 2:
    recommendations.append('🍅 Tomatoes are tasty! Plant more for your farm!')
if 'wood' in df.columns and df['wood'].mean() < 2:
    recommendations.append('🪵 Collect more wood to build awesome farm tools!')

# Default Recommendation if everything is good
if not recommendations:
    recommendations.append('🌟 Your farm is doing great! Keep up the good work!')

# 📄 Write Recommendations to File
rec_file_path = os.path.join(output_folder, 'kids_recommendations.txt')
with open(rec_file_path, 'w', encoding='utf-8') as rec_file:
    rec_file.write("🎮 **Game Recommendations for You!** 🎮\n\n")
    for rec in recommendations:
        rec_file.write(f"- {rec}\n")

# ✅ Confirmation
print(f"Kid-friendly analysis saved at: {output_file}")
print(f"Recommendations saved at: {rec_file_path}")
