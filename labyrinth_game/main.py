#!/usr/bin/env python3

from .player_actions import get_input, move_player, show_inventory, take_item, use_item
from .utils import attempt_open_treasure, describe_current_room, show_help, solve_puzzle


def main():
    """
    Основная функция игры
    """

    print("Добро пожаловать в Лабиринт сокровищ!")

    game_state = {
        'player_inventory': [],
        'current_room': 'entrance',
        'game_over': False,
        'steps_taken': 0
    }

    describe_current_room(game_state)

    while not game_state['game_over']:
        command = get_input("> ")
        
        process_command(game_state, command)

def process_command(game_state, command):
    """
    Фукнция для обработки пользовательских команд
    
    Параметры:
        game_state - словарь, содержит информацию о состоянии игрока
        command - строка, содержит ввод пользователя
    """
    commands = command.strip().lower().split()

    if not commands:
        return 

    user_command = commands[0]

    match user_command:
        case 'look':
            describe_current_room(game_state)
            
        case 'go':
            if len(commands) > 1:
                direction = commands[1]
                move_player(game_state, direction)
            else:
                print("Укажите направление движения.")
                
        case 'take':
            if len(commands) > 1:
                item_name = commands[1]
                take_item(game_state, item_name)
            else:
                print("Укажите предмет, который необходимо взять.")
                
        case 'use':
            if len(commands) > 1:
                item_name = commands[1]
                use_item(game_state, item_name)
            else:
                print("Укажите предмет, который необходимо использовать.")
                
        case 'inventory':
            show_inventory(game_state)

        case 'solve':
            curr_room = game_state['current_room']
            if curr_room == 'treasure_room':
                attempt_open_treasure(game_state)
            else:
                solve_puzzle(game_state)

        case 'help':
            show_help()
            
        case 'quit' | 'exit':
            print("Выход из игры.")
            game_state['game_over'] = True
            
        case _:
            print(f"Неизвестная команда: '{user_command}'")
            print("Введите 'help' для списка команд.")

if __name__ == "__main__":
    main()