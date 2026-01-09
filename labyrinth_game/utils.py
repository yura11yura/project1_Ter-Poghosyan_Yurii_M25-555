# labyrinth_game/utils.py

from .constants import ROOMS


def describe_current_room(game_state):
    """
    Фукнция для вывода информации о текущей комнате
    
    Параметры:
        game_state - словарь, содержит информацию о состоянии игрока
    """
    curr_room_name = game_state['current_room']
    curr_room = ROOMS[curr_room_name]
    print(f"== {curr_room_name.upper()} ==")
    print(curr_room['description'])

    if curr_room['items']:
        print("Заметные предметы:", ", ".join(curr_room['items']))
    exits = curr_room['exits']
    print("Выходы:", ", ".join([f"{direction} -> {room}" 
        for direction, room in exits.items()]))
    if curr_room['puzzle']:
        print("Кажется, здесь есть загадка (используйте команду solve).")

def solve_puzzle(game_state):
    """
    Фукнция для решения загадок
    
    Параметры:
        game_state - словарь, содержит информацию о состоянии игрока
    """
    curr_room_name = game_state['current_room']
    curr_room = ROOMS[curr_room_name]

    if not curr_room['puzzle']:
        print("Загадок здесь нет.")
        return

    question, correct_answer = curr_room['puzzle']
    print(question)

    user_answer = input("Ваш ответ: ").strip()

    if user_answer.lower() == str(correct_answer).lower():
        print("Загадка решена!")
        curr_room['puzzle'] = None
        
        match curr_room_name:
            case 'hall':
                game_state['player_inventory'].append('silver_key')

            case 'library':
                game_state['player_inventory'].append('ancient_amulet')

            case 'trap_room':
                game_state['player_inventory'].append('rusty_key')

            case 'spider_room':
                game_state['player_inventory'].append('golden_ring')

            case 'crystal_cavern':
                game_state['player_inventory'].append('treasure_key')
        print("Поздравляем! Ваша награда: ", game_state['player_inventory'][-1])
    else:
        print("Неверно. Попробуйте снова.")

def attempt_open_treasure(game_state):
    """
    Фукнция для попытки открыть сундук сокровищ
    
    Параметры:
        game_state - словарь, содержит информацию о состоянии игрока
    """
    if 'treasure_key' in game_state['player_inventory']:
        print("Вы применяете ключ, и замок щёлкает. Сундук открыт!")
        ROOMS[game_state['current_room']]['items'].remove('treasure_chest')
        print("В сундуке сокровище! Вы победили!")
        print("Число выполненных ходов: ", game_state['steps_taken'])
        game_state['game_over'] = True
    
    else:
        users_answer = input("Сундук заперт. ... Ввести код? (да/нет) ")
        
        if users_answer.lower() == "да":
            print(ROOMS[game_state['current_room']]['puzzle'][0])
            users_code = input("Введние код: ")
            
            if users_code == ROOMS[game_state['current_room']]['puzzle'][1]:
                print("Вы правильно вводите код, раздаётся щелчок, "
                    "и крышка сундука поднимается!")
                ROOMS[game_state['current_room']]['items'].remove('treasure_chest')
                print("В сундуке сокровище! Вы победили!")
                print("Число выполненных ходов: ", game_state['steps_taken'])
                game_state['game_over'] = True
            
            else:
                print("Код был введён неправильно. Пожалуйста, повторите попытку.")
            
        else:
            print("Вы отступаете от сундука.")

def show_help():
    print("\nДоступные команды:")
    print("  go <direction>  - перейти в направлении (north/south/east/west)")
    print("  look            - осмотреть текущую комнату")
    print("  take <item>     - поднять предмет")
    print("  use <item>      - использовать предмет из инвентаря")
    print("  inventory       - показать инвентарь")
    print("  solve           - попытаться решить загадку в комнате")
    print("  quit            - выйти из игры")
    print("  help            - показать это сообщение")