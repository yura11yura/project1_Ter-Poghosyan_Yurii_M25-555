# labyrinth_game/player_actions.py

from .constants import ROOMS
from .utils import attempt_open_treasure, describe_current_room


def show_inventory(game_state):
    """
    Фукнция для вывода информации об инвентаре
    
    Параметры:
        game_state - словарь, содержит информацию о состоянии игрока
    """
    inventory = game_state['player_inventory']
    if inventory:
        print("Инвентарь:", ", ".join(inventory))
    else:
        print("Инвентарь пуст.")

def get_input(prompt="> "):
    """
    Фукнция для получения ввода от игрока
    """
    try:
        user_input = input(prompt)
        return user_input
    except (KeyboardInterrupt, EOFError):
        print("\nВыход из игры.")
        return "quit" 

def move_player(game_state, direction):
    """
    Фукнция для совершения движений игроком
    
    Параметры:
        game_state - словарь, содержит информацию о состоянии игрока
        direction - строка, содержит направление движения
    """
    curr_room_name = game_state['current_room']
    curr_room = ROOMS[curr_room_name]

    if direction in curr_room['exits']:
        game_state['current_room'] = curr_room['exits'][direction]
        game_state['steps_taken'] += 1
        describe_current_room(game_state)
    else:
        print("Нельзя пойти в этом направлении.")

def take_item(game_state, item_name):
    """
    Фукнция для взятия предмета
    
    Параметры:
        game_state - словарь, содержит информацию о состоянии игрока
        item_name - строка, содержит название предмета
    """
    curr_room_name = game_state['current_room']
    curr_room = ROOMS[curr_room_name]

    if item_name in curr_room['items']:

        if item_name == 'treasure_chest':
            print("Вы не можете поднять сундук, он слишком тяжелый.")
            return

        game_state['player_inventory'].append(item_name)
        curr_room['items'].remove(item_name)
        print(f"Вы подняли: {item_name}")
    else:
        print("Такого предмета здесь нет.")

def use_item(game_state, item_name):
    """
    Фукнция для использования предмета
    
    Параметры:
        game_state - словарь, содержит информацию о состоянии игрока
        item_name - строка, содержит название предмета
    """
    if item_name not in game_state['player_inventory']:
        print("У вас нет такого предмета.")
        return

    match item_name:
        case 'torch':
            print("Факел освещает комнату. Стало светлее.")            

        case 'sword':
            print("Вы размахиваете мечом. Чувствуете себя увереннее.")

        case 'bronze_box':
            print("Вы открываете бронзовую шкатулку...")
            if 'rusty_key' not in game_state['player_inventory']:
                game_state['player_inventory'].append('rusty_key')
                print("Внутри вы нашли старый ржавый ключ!")
            else:
                print("Шкатулка пуста.")        

        case "treasure_key":
            if game_state['current_room'] == 'treasure_room':
                attempt_open_treasure(game_state=game_state)
            else:
                print("Нельзя использовать ключ от сундука сокровищ в этой комнате.")

        case 'golden_ring':
            print("Золотое кольцо загадочно мерцает.")

        case 'spider_silk':
            print("Паучий шелк очень прочный.")

        case 'blue_crystal':
            print("Синий кристалл светится мягким светом.")

        case 'rusty_key':
            print("Старый ржавый ключ. Непонятно, для чего он.")

        case _:
            print("Вы не знаете, как использовать данный предмет.")
