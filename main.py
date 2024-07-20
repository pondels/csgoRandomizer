import time
import random
import json
import os

# Weapon name and price search
weapon_data = {
    'kevlar vest': 650,
    'kevlar & helmet': 1000,
    'zeus x27': 200,
    'defuse kit': 400,
    'r8 revolver': 600,
    'dual barettas': 300,
    'p250': 300,
    'desert eagle': 700,
    'cz75-auto': 500,
    'usp-s': 200,
    'p2000': 200,
    'five-seven': 500,
    'glock-18': 200,
    'tec-9': 500,
    'm249': 5200,
    'mp5-sd': 1500,
    'mp7': 1500,
    'negev': 1700,
    'nova': 1050,
    'p90': 2350,
    'pp-bizon': 1400,
    'ump-45': 1200,
    'xm1014': 2000,
    'mag-7': 1300,
    'mp9': 1250,
    'mac-10': 1050,
    'sawed-off': 1100,
    'awp': 4750,
    'ssg 08': 1700,
    'famas': 2050,
    'm4a1-s': 2900,
    'm4a4': 3000,
    'aug': 3300,
    'scar-20': 5000,
    'ak-47': 2700,
    'g3sg1': 5000,
    'galil ar': 1800,
    'sg 553': 3000,
    'flashbang': 200,
    'smoke grenade': 300,
    'high explosive grenade': 300,
    'decoy grenade': 50,
    'incendiary grenade': 500,
    'molotov': 400
}

team_data = {
    'shared': {
        'equipment': ['kevlar vest', 'kevlar & helmet', 'zeus x27'],
        'starter-pistols': [],
        'pistols': ['r8 revolver', 'dual barettas', 'p250', 'desert eagle', 'cz75-auto'],
        'mid-tier': ['m249', 'mp5-sd', 'mp7', 'negev', 'nova', 'p90', 'pp-bizon', 'ump-45', 'xm1014'],
        'rifles': ['awp', 'ssg 08'],
        'grenades': ['flashbang', 'smoke grenade', 'high explosive grenade', 'decoy grenade']
    },
    'ct': {
        'equipment': ['defuse kit'],
        'starter-pistols': ['usp-s', 'p2000'],
        'pistols': ['five-seven'],
        'mid-tier': ['mag-7', 'mp9'],
        'rifles': ['famas', 'm4a1-s', 'm4a4', 'aug', 'scar-20'],
        'grenades': ['incendiary grenade']
    },
    't': {
        'equipment': [],
        'starter-pistols': ['glock-18'],
        'pistols': ['tec-9'],
        'mid-tier': ['mac-10', 'sawed-off'],
        'rifles': ['ak-47', 'g3sg1', 'galil ar', 'sg 553'],
        'grenades': ['molotov']
    }
}

def data_fully_populated(user_data):
    """
    Return Dictionary of all information needed so
    that the user knows what they need to fill out
    """
    unpopulated = {}
    for team in user_data:
        for weapon_genre in user_data[team]:
            if weapon_genre in ['equipment', 'grenades']: continue
            total = 0
            for _ in user_data[team][weapon_genre]:
                total += 1
            if total != 5:
                if not unpopulated.get(team):
                    unpopulated[team] = [weapon_genre]
                else:
                    unpopulated[team].append(weapon_genre)

    return unpopulated

def pick_weapon(user_data, team, weapon_type):

    def select_weapon(weapon_list):
        choice = input("\t> ").lower()
        if choice == 'q': return 'q'
        try:
            choice = int(choice)
            if choice-1 >= len(weapon_list):
                print('Invalid Range!')
                return
            return weapon_list[choice-1]
        except:
            print('Invalid Input! Must be INT type!')
            return

    # Data to override user information
    override_info = []

    os.system('cls')
    special_options = []
    if weapon_type == 'pistols':
        special_options = team_data[team]['starter-pistols'][:]
    options = team_data['shared'][weapon_type] + team_data[team][weapon_type][:]
    slot = 1
    while True:
        os.system('cls')
        if slot > 5:
            for i, weapon in enumerate(override_info):
                print(f'{i+1}. {weapon.upper()}')
            confirmation = input('Look Good? (y/n)> ').lower()
            
            # Everything is good, modify the data
            if confirmation == 'y': break
            else: return None

        print(f'Pick a weapon for slot #{slot}')
        chosen_gun = None
        current_data = []
        if weapon_type == 'pistols' and slot == 1:
            current_data = special_options
            for i, option in enumerate(special_options):
                print(f'{i+1}. {option.upper()}')
            print(f'Q. Cancel')
            chosen_gun = select_weapon(special_options)
        else:    
            current_data = options
            for i, option in enumerate(options):
                print(f'{i+1}. {option.upper()}')
            print(f'Q. Cancel')
            chosen_gun = select_weapon(options)
        
        # Invalid input from user
        if not chosen_gun: continue
        
        # User wants to quit
        if chosen_gun == 'q': return True

        choice = input(f'Gun {chosen_gun.upper()} for slot {slot}? (y/n)> ').lower()
        if choice == 'y':
            if chosen_gun in current_data:
                current_data.remove(chosen_gun)
                override_info.append(chosen_gun)
            slot += 1

    user_data[team][weapon_type] = override_info
    return True

def edit_class(user_data: dict, team: str):

    while True:
        os.system('cls')
        print('\t1. Pistols')
        print('\t2. Mid-Tier')
        print('\t3. Rifles')
        print('\tQ. Quit')
        choice = input('\t> ').lower()
        
        # Quitting
        if choice == 'q': break
        
        # Updating Pistols
        if choice == '1':
            while True:
                if pick_weapon(user_data, team, 'pistols'):
                    break

        # Updating Mid-Tier
        if choice == '2':
            while True:
                if pick_weapon(user_data, team, 'mid-tier'):
                    break

        # Updating Rifles
        if choice == '3':
            while True:
                if pick_weapon(user_data, team, 'rifles'):
                    break

    return user_data

def display_data(user_data: dict):
    os.system('cls')
    for team, slots in user_data.items():
        print(f'{team.upper()}')
        for slot in slots:
            print(f'  {slot}')
            if not user_data[team][slot]:
                print(f'    UNPOPULATED')
            for item in user_data[team][slot]:
                print(f'    {item}')

def rebind(user_data: dict):
    """
    Replaces all current data with all their weapons
    """
    print("IMPORTANT! Make sure the weapons you choose are the right number under the right slot!")
    while True:
        os.system('cls')
        print('\t1. Show Weapon Info')
        print('\t2. Edit    CT')
        print('\t3. Edit     T')
        print('\tQ. Quit')
        choice = input('\t> ').lower()
        
        # Leaving the editor
        if choice == "q": break
        
        elif choice == "1":
            display_data(user_data)
            input('Hit Enter >')

        # Editing the counter terrorists
        elif choice in ["2", "3"]:
            user_data = edit_class(user_data, 'ct' if choice == '2' else 't')

    # Writing any changes the user made
    with open('./current_weapons_data.json', 'w') as file:
        json.dump(user_data, file)

def logger():
    """
    * starts the logging of information, but it's always running
        This includes restarting input in the case of a mistake
    "k/h" denote a damaged/broken kevlar and helmet respectively
    [0-9] denote the user's cash pool
    "l" denotes if you lived the previous round, modifying prioty buying system
    + ends the logger and returns the string of information
    / ends the program as a whole so you can leave
    """

def get_category_items(user_data, team, mode, category):
    """
    grab all items based on a category,
    mode and team around the user's loadout
    """
    all_items = user_data[team][category][:]

    # Filtering out mode-specific buys
    if category == 'equipment' and mode == 'casual':
        all_items.remove('kevlar vest')
        all_items.remove('kevlar & helmet')
        if team == 'ct': all_items.remove('defuse kit')
    return all_items

def get_possible_items(user_data, current_loadout, team, mode, balance, buy_helmet, buy_kevlar, grenade_slots):
    """
    based on user data, find all affordable items
    """
    # Finding valid categories to buy from
    valid_categories = []
    for category in current_loadout:
        if not current_loadout[category]:
            valid_categories.append(category)
        else:
            # Check grenade slots
            if category == 'grenades' and grenade_slots > 0:
                valid_categories.append(category)

    # Removing primary guns from the auto-buyer if they already have one
    if 'mid-tier' in valid_categories and not 'rifles' in valid_categories:
        valid_categories.remove('mid-tier')
    elif not 'mid-tier' in valid_categories and 'rifles' in valid_categories:
        valid_categories.remove('rifles')

    valid_buys = {}
    for category in valid_categories:
        all_items = get_category_items(user_data, team, mode, category)
        if category == 'equipment':
            if not buy_helmet and 'kevlar & helmet' in all_items: all_items.remove('kevlar & helmet')
            if not buy_kevlar and 'kevlar vest' in all_items: all_items.remove('kevlar vest')
        affordables = [i for i in all_items if weapon_data[i] <= balance]
        if affordables:
            valid_buys[category] = affordables

    return valid_buys

def randomize_loop(user_data, team, mode):
    """
    user_data -> weapon loadout
    team -> ct/t
    mode -> casual/competitive

    no support for modes such as wingman, but I don't think that matters :/
    
    CASUAL
    ==========================================================
    Can't buy Armor or Defuse, but can buy zeus
    1 grenade slot per grenade up to 3 slots

    COMPETITIVE
    ==========================================================
    Can buy everything
    1 of every grenade, 2 of flash up to 4 total grenade slots
    
    PURCHASABLES (w/ Weights of Priority)
    ==========================================================
    TEAM---------------------------------------------| CT  ||  T
    Primary                                          | 38% || 40%
    Secondary                                        | 14% || 20%
    Defuse Kit (if applicable)                       | 10% || 00%
    Zeus                                             | 05% || 05%
    Armor (Kevlar, or kevlar and helmet, never both) | 20% || 20%
    Grenades (Up to 4 grenade purchases)             | 13% || 15%

    RATES (if you can afford it)
    ==========================================================
    1st purchase: 100%
    2nd purchase:  80%
    3rd purchase:  70%
    4th purchase:  60%
    5th purchase:  55%
    6th purchase:  50% Casual CT/T Max
    7th purchase:  45%
    8th purchase:  40% Competitive T Max
    9th purchase:  35% Competitive CT Max

    Buy using the category number according by index and the gun by index YTASYUDHG
    """
    # Used if the user lives and we want to know what they already likely have
    current_loadout = {
        'equipment': [],
        'pistols':   [],
        'mid-tier':  [],
        'rifles':    [],
        'grenades':  []
    }
    while True:
        # User value = money and data regarding what they can afford
        # user_value = logger()
        
        # Test strings to work with
        user_value = '*10000'
        
        # for user_value in user_values:
        buy_kevlar = True if 'k' in user_value else False
        buy_helmet = True if 'h' in user_value else False
        lived      = True if 'l' in user_value else False
        user_value = user_value.translate(str.maketrans('', '', 'khl*'))
        balance = int(user_value)
        
        # Reset current loadout if they didn't live
        if not lived:
            current_loadout = {key: [] for key in current_loadout}

        rates = [1, 0.8, 0.7, 0.6, 0.55, 0.5, 0.45, 0.4, 0.35]
        if mode == 'casual': rates = rates[:6]
        elif team == 'ct': rates = rates[:9]
        elif team == 't': rates = rates[:8]

        # Determining max buys based on mode and team
        print('What can I buy? hmmmMmM')
        grenade_slots = 3 if mode == 'casual' else 4
        grenade_slots -= len(current_loadout['grenades'])
        for rate in rates:

            # No more buying :(
            if random.random() > rate: break

            # Choosing a random item (weights can be applied later)
            possible_items = get_possible_items(user_data, current_loadout, team, mode, balance, buy_helmet, buy_kevlar, grenade_slots)
            
            # Broke ass bitch
            if not possible_items: break

            # Buy your shit
            random_category = random.choice(list(possible_items.keys()))
            
            if random_category == 'grenades':
                # Filter grenades so we don't buy duplicates
                grenade_blacklist = []
                first_flash_found = False
                for grenade in current_loadout['grenades']:
                    if grenade == 'flashbang' and not first_flash_found and mode == 'competitive':
                        first_flash_found = True
                    else: grenade_blacklist.append(grenade)
                random_item = random.choice([i for i in list(possible_items[random_category]) if i not in grenade_blacklist])
                current_loadout[random_category].append(random_item)
                grenade_slots -= 1
            else:
                random_item = random.choice(list(possible_items[random_category]))
                current_loadout[random_category].append(random_item)
            balance -= weapon_data[random_item]
            print(f'Bought {random_item} from {random_category}. New Balance: ${balance:,.2f}')
        
        # Commence the autobuyer
        buy_items(user_data, current_loadout, team)
        break

def start_randomizer(user_data):
    
    unfilled_data = data_fully_populated(user_data)
    if unfilled_data:
        print('Team Data Not Filled Out! Please rebind the following and try again.')
        for team in unfilled_data:
            for weapon_genre in unfilled_data[team]:
                print(f'{team.upper()} -> {weapon_genre.upper()}')
        input('ok... > ')
        
        # Restarting
        main()
        return

    os.system('cls')
    while True:
        print("Select A Team")
        print("\t1.   CT")
        print("\t2.    T")
        print("\tQ. Quit")
        team = input('\t> ').lower()

        if team in ['t', 'ct', '1', '2']:
            team = 'ct' if team == '1' else 't'
            os.system('cls')
            while True:
                print("Select A Mode")
                print("\t1.      Casual")
                print("\t2. Competitive")
                print("\tB.        Back")
                print("\tQ.        Quit")
                game = input('\t> ').lower()
                if game in ['1', '2', 'casual', 'competitive']:
                    game = 'casual' if game == "1" else 'competitive'
                    # Start the loop
                    randomize_loop(user_data, team, game)
                    if input('Continue Running? (y/n) > ').lower() == 'n':
                        return
                    os.system('cls')
                    break
                os.system('cls')
                if game == 'b': break
                if game == 'q': return
                else:
                    print('Invalid option!')
        
        elif team == 'q': return
        else:
            os.system('cls')
            print('Invalid Choice!')

def find_weapon_slot(user_data, team, category, item_to_compare):
    for i, item in enumerate(user_data[team][category]):
        if item == item_to_compare:
            return i+1

def press_key(key):
    import keyboard
    keyboard.press(key)
    time.sleep(.05)
    keyboard.release(key)
    time.sleep(.5)

def buy_items(user_data, purchaseables, team):
    import keyboard
    time.sleep(4)
    press_key('b')
    print('b')
    for i, category in enumerate(purchaseables):
        for item in purchaseables[category]:
            weapon_slot = find_weapon_slot(user_data, team, category, item)
            press_key(i+2)
            print(i+2)
            press_key(weapon_slot+1)
            print(weapon_slot+1)

    keyboard.press('esc')
    keyboard.release('esc')

def main():

    os.system('cls')
    while True:
        user_data = {}
        with open('./current_weapons_data.json', 'r') as file:
            user_data = json.load(file)
        print('1. Rebind Team Layouts')
        print('2. Start Random Auto-Buyer')
        print('Q. Quit')
        choice = input('Choose an Option -> ').lower()
        if choice == '1': rebind(user_data)
        elif choice == '2': start_randomizer(user_data)
        elif choice == 'q': return
        else:
            os.system('cls')
            print('Invalid Choice!')

main()

#     while True:
#         quit = [False]

#         def on_press(key):
#             try:
#                 if check_balance == [] and str(key) == "'y'": check_balance.append('y')
#                 elif check_balance != []:
#                     if check_balance[0] == 'y' and (str(key) == '<96>' or str(key) == "'0'"):
#                         check_balance.append(0)
#                     elif check_balance[0] == 'y' and (str(key) == '<97>' or str(key) == "'1'"):
#                         check_balance.append(1)
#                     elif check_balance[0] == 'y' and (str(key) == '<98>' or str(key) == "'2'"):
#                         check_balance.append(2)
#                     elif check_balance[0] == 'y' and (str(key) == '<99>' or str(key) == "'3'"):
#                         check_balance.append(3)
#                     elif check_balance[0] == 'y' and (str(key) == '<100>' or str(key) == "'4'"):
#                         check_balance.append(4)
#                     elif check_balance[0] == 'y' and (str(key) == '<101>' or str(key) == "'5'"):
#                         check_balance.append(5)
#                     elif check_balance[0] == 'y' and (str(key) == '<102>' or str(key) == "'6'"):
#                         check_balance.append(6)
#                     elif check_balance[0] == 'y' and (str(key) == '<103>' or str(key) == "'7'"):
#                         check_balance.append(7)
#                     elif check_balance[0] == 'y' and (str(key) == '<104>' or str(key) == "'8'"):
#                         check_balance.append(8)
#                     elif check_balance[0] == 'y' and (str(key) == '<105>' or str(key) == "'9'"):
#                         check_balance.append(9)
#             except AttributeError:
#                 pass

#         def on_release(key):
#             if str(key) == 'Key.enter' and len(check_balance) > 1:
#                 # Stop listener
#                 check_balance.pop(0)
#                 return False
#             elif str(key) == "'-'":
#                 quit[0] = True
#                 return False
#             elif str(key) == "'*'":
#                 for _ in range(1, len(check_balance)):
#                     check_balance.pop()
                
#             elif str(key) == "Key.backspace" and len(check_balance) > 0: check_balance.pop()

#         from pynput import keyboard
#         with keyboard.Listener(on_press=on_press, on_release=on_release) as listener:
#             listener.join()