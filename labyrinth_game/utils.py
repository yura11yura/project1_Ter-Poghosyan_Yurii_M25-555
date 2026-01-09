# labyrinth_game/utils.py

import math

from .constants import ALT_ANSWERS, COMMANDS, DEATH_THRESHOLD, DEFAULT_MODULO, ROOMS


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

    possible_answers = ALT_ANSWERS[str(correct_answer).lower()]

    if user_answer.lower() in possible_answers:
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

        if curr_room_name == 'trap_room':
            trigger_trap(game_state)

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

def show_help(command_list = COMMANDS):
    """
    Фукнция для вывода вспомогательной информации

    Принимает:
        command_list - список, содержит информацию о доступных командах
    """
    print("\nДоступные команды:")
    
    for command, description in COMMANDS.items():
        formatted_command = command.ljust(20)
        print(f"  {formatted_command} - {description}")

def pseudo_random(seed, modulo):
    """
    Фукнция псевдослучайный генератор
    
    Параметры:
        seed - целое число, содержит количество шагов
        modulo - целое число для определения диапазона результата
    Возвращает:
        Целое число в диапазоне [0. modulo)
    """
    x = math.sin(seed * 12.9898) * 43758.5453

    return int(math.floor((x - math.floor(x)) * modulo))

def trigger_trap(game_state):
    """
    Фукнция для срабатывания ловушки
    
    Параметры:
        game_state - словарь, содержит информацию о состоянии игрока
    """
    print("Ловушка активирована! Пол стал дрожать...")

    inventory = game_state['player_inventory']
    
    if inventory:
        random_index = pseudo_random(game_state['steps_taken'], len(inventory))
        lost_item = inventory.pop(random_index)
        print("У вас выпал предмет: ", lost_item)
    else:
        random_value = pseudo_random(game_state['steps_taken'], DEFAULT_MODULO)
        if random_value < DEATH_THRESHOLD:
            print("Ловушка оказалась смертельной! Вы проиграли.")
            game_state['game_over'] = True
        else:
            print("Вам удается увернуться от ловушки. Вы уцелели!")

def random_event(game_state):
    """
    Функция для создания случайного события
    
    Параметры:
        game_state - словарь, содержит информацию о состоянии игрока
    """
    event_chance = pseudo_random(game_state['steps_taken'], DEFAULT_MODULO)

    if event_chance == 0:
        event = pseudo_random(game_state['steps_taken'] + 1, 3)
        
        if event == 0:
            curr_room = ROOMS[game_state['current_room']]
            if 'coin' not in curr_room['items']:
                curr_room['items'].append('coin')
                print("Вы заметили что-то блестящее на полу. Это монетка!")
        
        elif event == 1:
            print("Вы слышите шорох в темноте.")
            if 'sword' in game_state['player_inventory']:
                print("Вы хватаетесь за меч, и шорох затихает. Опасность отступила.")
            else:
                print("Вы замираете, пока шорох не стихает.")
        
        elif event == 2:
            curr_room_name = game_state['current_room']
            if curr_room_name == 'trap_room' and 'torch' \
                not in game_state['player_inventory']:
                print("Опасно! Вы наступили на скрытую плиту!")
                trigger_trap(game_state)
        else:
            print("Вы чувствуете, что здесь что-то не так...")