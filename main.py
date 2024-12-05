import argparse
import sys
from enigma import load_config, create_enigma

def validate_rotor_positions(positions, alphabet):
    """ Проверяет корректность начальных позиций роторов.

        Параметры:
            positions (list): Список начальных позиций роторов (должен содержать три элемента).

            alphabet (str): Строка, представляющая допустимый алфавит.

        Исключения:
            ValueError: Если количество позиций не равно 3 или если какая-либо из позиций недопустима.
        """
    if len(positions) != 3:
        raise ValueError("Необходимо указать три начальные позиции роторов.")
    for pos in positions:
        if pos not in alphabet:
            raise ValueError(f"Недопустимая позиция ротора: {pos}")

def validate_plugboard_settings(plugboard_settings, alphabet):
    """ Проверяет настройки коммутационной панели.

        Параметры:
            plugboard_settings (list): Список пар символов для настройки коммутационной панели (каждая пара должна содержать ровно 2 буквы).

            alphabet (str): Строка, представляющая допустимый алфавит.

        Исключения:
            ValueError: Если пара имеет недопустимую длину, содержит недопустимые буквы, имеет одинаковые буквы или использует уже задействованные буквы.
        """
    used_letters = set()
    for pair in plugboard_settings:
        if len(pair) != 2:
            raise ValueError(f"Неверная пара в настройках коммутационной панели: {pair}")
        a, b = pair
        if a not in alphabet or b not in alphabet:
            raise ValueError(f"Недопустимые буквы в паре: {pair}")
        if a == b:
            raise ValueError(f"Буквы в паре не могут быть одинаковыми: {pair}")
        if a in used_letters or b in used_letters:
            raise ValueError(f"Буква уже используется в другой паре: {pair}")
        used_letters.update(pair)

def validate_text(text, alphabet):
    """ Проверяет корректность текста на наличие недопустимых символов.

        Параметры:
            text (str): Строка с текстом, который необходимо проверить.

            alphabet (str): Строка, представляющая допустимый алфавит.

        Исключения:
            ValueError: Если в тексте присутствуют символы, не входящие в допустимый алфавит, кроме пробелов.
        """
    for char in text:
        if char not in alphabet and char != ' ':
            raise ValueError(f"Недопустимый символ в тексте: {char}")

def main():
    """
    Основная функция для запуска программы.
    """
    parser = argparse.ArgumentParser(description='Russian Enigma Machine')
    parser.add_argument('--config', help='Path to configuration file', default='config.json')
    parser.add_argument('--positions', help='Rotor positions (3 letters)')
    parser.add_argument('--plugboard', help='Plugboard settings (pairs of letters)')
    parser.add_argument('--text', help='Text to encode/decode')

    args = parser.parse_args()

    if len(sys.argv) == 1:
        # Текстовый интерфейс
        config_file = input("Введите путь к файлу конфигурации: ")
        positions = input("Введите начальные позиции роторов (3 буквы): ").upper()
        plugboard = input("Введите настройки коммутационной панели (пары букв через пробел): ").upper().split()
        text = input("Введите текст для шифрования: ").upper()
    else:
        # Командная строка
        config_file = args.config
        positions = args.positions.upper()
        plugboard = args.plugboard.upper().split()
        text = args.text.upper()

    alphabet = 'АБВГДЕЁЖЗИЙКЛМНОПРСТУФХЦЧШЩЪЫЬЭЮЯ'

    try:
        validate_rotor_positions(positions, alphabet)
        validate_plugboard_settings(plugboard, alphabet)
        validate_text(text, alphabet)
    except ValueError as e:
        print(f"Ошибка: {e}")
        sys.exit(1)

    config = load_config(config_file)
    enigma = create_enigma(config, positions, plugboard)
    result = enigma.encode_text(text)
    print(f"Результат: {result}")


if __name__ == "__main__":
    main()
