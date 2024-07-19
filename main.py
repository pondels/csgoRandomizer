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
    TEAM---------------------------------------------| CT ||   T
    Primary                                          | 38 || 40.00%
    Secondary                                        | 14 || 20.00%
    Defuse Kit (if applicable)                       | 10 || 00.00%
    Zeus                                             | 05 || 05.00%
    Armor (Kevlar, or kevlar and helmet, never both) | 20 || 20.00%
    Grenades (Up to 4 grenade purchases)             | 13 || 15.00%

    RATES (if you can afford it)
    ==========================================================
    1st purchase: 100%
    2nd purchase:  80%
    3rd purchase:  70%
    4th purchase:  60%
    5th purchase:  55%
    6th purchase:  50%
    7th purchase:  45%
    8th purchase:  40%
    """

    pass

def start_randomizer(user_data):
    print(user_data)
    os.system('cls')
    while True:
        print("Select A Team")
        print("\t1.   CT")
        print("\t2.    T")
        print("\tQ. Quit")
        team = input('\t> ').lower()

        if team in ['t', 'ct', '1', '2']:
            os.system('cls')
            while True:
                print("Select A Mode")
                print("\t1.      Casual")
                print("\t2. Competitive")
                print("\tB.        Back")
                print("\tQ.        Quit")
                game = input('\t> ').lower()
                if game in ['1', '2', 'casual', 'competitive']:
                    
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

def main():

    user_data = {}
    with open('./current_weapons_data.json', 'r') as file:
        user_data = json.load(file)
    rebind_crap = input('Would you like to rebind your layout? (y/n) -> ').lower()
    if rebind_crap and rebind_crap[0] == 'y': rebind(user_data)
    start_randomizer(user_data)

main()

# def main():

#     check_balance = []
#     team, mode, check_deagle, check_m4a4 = '', '', '', ''

#     while team != 't' and team != 'ct':
#         team = input("ct or t: ").lower()
#     while mode != '1' and mode != '2':
#         mode = input("Casual or Competitive (1 / 2)? ")
#     while check_deagle != 'y' and check_deagle != 'n':
#         check_deagle = input("Are you using the deagle (y / n): ").lower()
#     if team == 'ct':
#         while check_m4a4 != 'y' and check_m4a4 != 'n':
#             check_m4a4 = input("Are you using the m4a4 (y / n): ").lower()
#     print("Ready For Input!")


#     def filtered():
#         purchasables = []
#         unaffordables = []

#         for i in pistol:
#             if pistol[i] <= balance:
#                 if 'pistol' not in purchasables:
#                     purchasables.append('pistol')
#             else:
#                 unaffordables.append(i)
            
#         for i in heavy:
#             if heavy[i] <= balance:
#                 if 'heavy' not in purchasables:
#                     purchasables.append('heavy')
#             else:
#                 unaffordables.append(i)

#         for i in smg:
#             if smg[i] <= balance:
#                 if 'smg' not in purchasables:
#                     purchasables.append('smg')
#             else:
#                 unaffordables.append(i)

#         for i in rifle:
#             if rifle[i] <= balance:
#                 if 'rifle' not in purchasables:
#                     purchasables.append('rifle')
#             else:
#                 unaffordables.append(i)

#         for i in equipment:
#             if equipment[i] <= balance:
#                 if 'equipment' not in purchasables:
#                     purchasables.append('equipment')
#             else:
#                 unaffordables.append(i)

#         for i in grenade:
#             if grenade[i] <= balance:
#                 if 'grenade' not in purchasables:
#                     purchasables.append('grenade')
#             else:
#                 unaffordables.append(i)
        
#         return purchasables, unaffordables

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
        
#         if quit[0]:
#             return

#         if len(check_balance) > 0:

#             grenade_slots = 3

#             pistol =    {'B 1 1':  200, 'B 1 2':  400, 'B 1 3':  300, 'B 1 4':  500}
#             heavy =     {'B 2 1': 1050, 'B 2 2': 2000, 'B 2 4': 5200, 'B 2 5': 1700}
#             smg =       {'B 3 2': 1500, 'B 3 3': 1200, 'B 3 4': 2350, 'B 3 5': 1400}
#             rifle =     {'B 4 3': 1700, 'B 4 5': 4750, 'B 4 6': 5000}
#             equipment = {'B 5 3':  200}
#             grenade =   {'B 6 2':   50, 'B 6 3':  200, 'B 6 4':  300, 'B 6 5':  300}

#             # 50

#             if team == 't':
#                 smg['B 3 1'] = 1050
#                 heavy['B 2 3'] = 1100
#                 rifle['B 4 1'] = 1800
#                 rifle['B 4 2'] = 2700
#                 rifle['B 4 4'] = 3000
#                 grenade['B 6 1'] = 400
#             else:
#                 smg['B 3 1'] = 1250
#                 heavy['B 2 3'] = 1300
#                 rifle['B 4 1'] = 2050

#                 if check_m4a4 == 'y':
#                     rifle['B 4 2'] = 3100
#                 else:
#                     rifle['B 4 2'] = 2900
                    
#                 rifle['B 4 4'] = 3300
#                 if mode == '2':
#                     equipment['B 5 4'] = 400

#                 grenade['B 6 1'] = 600
            
#             if mode == '2':
#                 equipment['B 5 1'] = 650
#                 equipment['B 5 2'] = 1000

#             if check_deagle == 'y':
#                 pistol['B 1 5'] = 700
#             else:
#                 pistol['B 1 5'] = 600

#             # ------------------------------------------------------------ #

#             balance = ''
#             for num in check_balance:
#                 balance += str(num)
#             balance = int(balance)
#             check_balance = []

#             purchasables, unaffordables = filtered()

#             for delete in unaffordables:
#                 if delete[2] == '1':
#                     del pistol[delete]

#                 elif delete[2] == '2':
#                     del heavy[delete]

#                 elif delete[2] == '3':
#                     del smg[delete]

#                 elif delete[2] == '4':
#                     del rifle[delete]

#                 elif delete[2] == '5':
#                     del equipment[delete]

#                 elif delete[2] == '6':
#                     del grenade[delete]

#             import keyboard
#             for i in range(1, 5):
#                 if i == 4: # Grenades
#                     for j in range(4):
#                         keyboard.press(str(i))
#                         keyboard.release(str(i))
#                         time.sleep(.05)
#                         keyboard.press("g")
#                         keyboard.release("g")
#                         time.sleep(.05)
#                 else:
#                     keyboard.press(str(i))
#                     keyboard.release(str(i))
#                     time.sleep(.05)
#                     keyboard.press("g")
#                     keyboard.release("g")
#                     time.sleep(.05)

#             while len(purchasables) > 0:
#                 buy = random.choice(purchasables)
#                 chance = random.random()
#                 if buy != 'grenade':
#                     purchasables.remove(buy)

#                 # 50% chance to buy that weapon
#                 if chance > .5:

#                     if buy == 'pistol':
#                         buy = random.choice(list(pistol))
#                         balance -= pistol[buy]
                        
#                     elif buy == 'heavy':
#                         buy = random.choice(list(heavy))
#                         balance -= heavy[buy]
#                         if 'smg' in purchasables:   purchasables.remove('smg')
#                         if 'rifle' in purchasables: purchasables.remove('rifle')
                        
#                     elif buy == 'smg':
#                         buy = random.choice(list(smg))
#                         balance -= smg[buy]
#                         if 'heavy' in purchasables: purchasables.remove('heavy')
#                         if 'rifle' in purchasables: purchasables.remove('rifle')
                        
#                     elif buy == 'rifle':
#                         buy = random.choice(list(rifle))
#                         balance -= rifle[buy]
#                         if 'smg' in purchasables:   purchasables.remove('smg')
#                         if 'heavy' in purchasables: purchasables.remove('heavy')
                        
#                     elif buy == 'equipment':
#                         buy = random.choice(list(equipment))
#                         balance -= equipment[buy]
                        
#                     elif buy == 'grenade':
#                         buy = random.choice(list(grenade))
#                         balance -= grenade[buy]
#                         del grenade[buy]
#                         grenade_slots -= 1
#                         chance = random.random()
#                         if chance > .75 or grenade == {} or grenade_slots == 0:
#                             purchasables.remove('grenade')

#                     import keyboard

#                     i = buy.split(' ')
#                     keyboard.press('b')
#                     keyboard.release('b')
#                     time.sleep(.05)
#                     keyboard.press(i[1])
#                     keyboard.release(i[1])
#                     time.sleep(.05)
#                     keyboard.press(i[2])
#                     keyboard.release(i[2])
#                     time.sleep(.05)
#                     keyboard.press('esc')
#                     keyboard.release('esc')
#                     time.sleep(.05)
#                     if i[1] == '6' or i[1] == '5':
#                         keyboard.press('esc')
#                         keyboard.release('esc')
#                         time.sleep(.05)
                    
#                     _, unaffordables = filtered()

#                     # Filters out all the weapons that I can't afford
#                     for delete in unaffordables:
#                         if delete[2] == '1':
#                             del pistol[delete]
#                             if pistol == {}:
#                                 if 'pistol' in purchasables:
#                                     purchasables.remove('pistol')

#                         elif delete[2] == '2':
#                             del heavy[delete]
#                             if heavy == {}:
#                                 if 'heavy' in purchasables:
#                                     purchasables.remove('heavy')

#                         elif delete[2] == '3':
#                             del smg[delete]
#                             if smg == {}:
#                                 if 'smg' in purchasables:
#                                     purchasables.remove('smg')

#                         elif delete[2] == '4':
#                             del rifle[delete]
#                             if rifle == {}:
#                                 if 'rifle' in purchasables:
#                                     purchasables.remove('rifle')

#                         elif delete[2] == '5':
#                             del equipment[delete]
#                             if equipment == {}:
#                                 if 'equipment' in purchasables:
#                                     purchasables.remove('equipment')

#                         elif delete[2] == '6':
#                             del grenade[delete]
#                             if grenade == {}:
#                                 if 'grenade' in purchasables:
#                                     purchasables.remove('grenade')
# main()

# while True:
#     again = input("Do you want to run again (y / n): ").lower()
#     if again == 'y':
#         main()
#     elif again == 'n':
#         break
#     else:
#         print("Looks like you had unwanted characters in the input field. Please try again!")

# # TODO
# '''
#     Custom Loadouts
#     UI
#         Control which team you are on.
#         Control which weapons are purchased.

#         When start is clicked, the macros begin
#         When the end is clicked, the script ends
#         when the close is clicked, the program shuts down
#     etc
# '''