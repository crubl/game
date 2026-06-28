from pathlib import Path

shop_path = Path('Main_menu/shop.py')
windows_path = Path('Main_menu/windows.py')

# Изменяет shop.py
text = shop_path.read_text(encoding='utf-8')
text = text.replace("Exp = 1                     #получаймый опыт\n", "")
text = text.replace("            'exp': {'name': 'Опыт', 'base_price': 120, 'increase': 0.1}\n", "")
text = text.replace("            'exp': 0,\n", "")
text = text.replace("        #elif upgrade_name == 'exp':\n", "")
text = text.replace("         #   self.hero.exp_multiplier += increase\n", "")
text = text.replace("        hero.exp_multiplier = 1.0 + self.upgrades['exp'] * self.upgrades_info['exp']['increase']\n", "")
text = text.replace("            'exp': (100, 255, 200)\n", "")
text = text.replace("            'exp': 'Множитель опыта +0.1x'\n", "")
text = text.replace("            'exp': (100, 255, 200),\n", "")
text = text.replace("            'exp': 'Множитель опыта +0.1x',\n", "")
text = text.replace("            'exp': 0,\n", "")
text = text.replace("            'exp': {'name': 'Опыт', 'base_price': 120, 'increase': 0.1},\n", "")
text = text.replace("    #         (f\"Множитель опыта: {hero.exp_multiplier:.1f}x\", (100, 255, 200)),\n", "")
text = text.replace("    #         (f\"Опыт: {hero.exp}/{hero.exp_to_next_level}\", (200, 200, 100))\n", "")

text_lines = text.splitlines()
cleaned_lines = []
for line in text_lines:
    if "'exp'" in line and "'exp'" not in line.replace("'exp'", ""):
        if "'exp'" in line and ('upgrades_info' in line or 'upgrades' in line or 'upgrade_names_ru' in line):
            
            continue
    cleaned_lines.append(line)
text = '\n'.join(cleaned_lines) + '\n'
shop_path.write_text(text, encoding='utf-8')

# Изменяет windows.py
text = windows_path.read_text(encoding='utf-8')
text = text.replace("            'exp': (100, 255, 200)\n", "")
text = text.replace("            'exp': 'Множитель опыта +0.1x'\n", "")
windows_path.write_text(text, encoding='utf-8')
print('exp removed')
