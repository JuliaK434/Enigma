import json
import sys

class Rotor:
    """
    Класс, представляющий ротор в машине Enigma.

    Атрибуты:
        wiring (list): Список, представляющий проводку ротора.

        notch (int): Позиция, на которой ротор вызывает вращение следующего ротора.

        position (int): Текущая позиция ротора.

        ring_setting (int): Настройка кольца ротора.
    """

    def __init__(self, wiring, notch):
        self.wiring = wiring
        self.notch = notch
        self.position = 0
        self.ring_setting = 0

    def forward(self, char_idx):
        """
        Прямой проход сигнала через ротор.

        Параметры:
            char_idx (int): Индекс символа.

        Возвращает:
            int: Индекс символа после прохождения через ротор.
        """
        shift = self.position - self.ring_setting
        contact = (char_idx + shift) % 33
        contact = self.wiring[contact]
        contact = (contact - shift) % 33
        return contact

    def backward(self, char_idx):
        """
        Обратный проход сигнала через ротор.

        Параметры:
            char_idx (int): Индекс символа.

        Возвращает:
            int: Индекс символа после прохождения через ротор.
        """
        shift = self.position - self.ring_setting
        contact = (char_idx + shift) % 33
        contact = self.wiring.index(contact)
        contact = (contact - shift) % 33
        return contact

    def rotate(self):
        """
        Вращает ротор на одну позицию.

        Возвращает:
            bool: True, если ротор достиг позиции зазора (notch), иначе False.
        """
        self.position = (self.position + 1) % 33
        return self.position == self.notch


class Reflector:
    """
    Класс, представляющий отражатель в машине Enigma.

    Атрибуты:
        wiring (list): Список, представляющий проводку отражателя.
    """

    def __init__(self, wiring):
        self.wiring = wiring

    def reflect(self, char_idx):
        """
        Отражает сигнал.

        Параметры:
            char_idx (int): Индекс символа.

        Возвращает:
            int: Индекс символа после отражения.
        """
        return self.wiring[char_idx]


class Enigma:
    """
    Класс, представляющий машину Enigma.

    Атрибуты:
        rotors (list): Список роторов.

        reflector (Reflector): Объект отражателя.

        plugboard (dict): Настройки коммутационной панели.

        alphabet (str): Алфавит, используемый в машине.
    """

    def __init__(self, rotors, reflector, plugboard):
        self.rotors = rotors
        self.reflector = reflector
        self.plugboard = plugboard
        self.alphabet = 'АБВГДЕЁЖЗИЙКЛМНОПРСТУФХЦЧШЩЪЫЬЭЮЯ'

    def set_rotor_positions(self, positions):
        """
        Устанавливает начальные позиции роторов.

        Параметры:
            positions (str): Строка из трех букв, представляющая начальные позиции роторов.
        """
        for rotor, pos in zip(self.rotors, positions):
            rotor.position = self.alphabet.index(pos)

    def encode_char(self, char):
        """
        Кодирует один символ.

        Параметры:
            char (str): Символ для кодирования.

        Возвращает:
            str: Закодированный символ.
        """
        if char not in self.alphabet:
            return char

        # Применяем коммутационную панель
        char_idx = self.alphabet.index(char)
        if char_idx in self.plugboard:
            char_idx = self.plugboard[char_idx]

        # Вращение роторов
        if self.rotors[1].rotate():
            self.rotors[0].rotate()
        if self.rotors[2].rotate():
            self.rotors[1].rotate()

        # Прямой проход через роторы
        for rotor in reversed(self.rotors):
            char_idx = rotor.forward(char_idx)

        # Отражатель
        char_idx = self.reflector.reflect(char_idx)

        # Обратный проход через роторы
        for rotor in self.rotors:
            char_idx = rotor.backward(char_idx)

        # Снова применяем коммутационную панель
        if char_idx in self.plugboard:
            char_idx = self.plugboard[char_idx]

        return self.alphabet[char_idx]

    def encode_text(self, text):
        """
        Кодирует текст.

        Параметры:
            text (str): Текст для кодирования.

        Возвращает:
            str: Закодированный текст.
        """
        text = text.upper()
        return ''.join(self.encode_char(c) for c in text)


def load_config(config_file):
    """
    Загружает конфигурацию из файла.

    Параметры:
        config_file (str): Путь к файлу конфигурации.

    Возвращает:
        dict: Конфигурация.

    Исключения:
        FileNotFoundError: Если файл не найден.
        json.JSONDecodeError: Если файл имеет неверный формат.
    """
    try:
        with open(config_file, 'r', encoding='utf-8') as f:
            config = json.load(f)
        return config
    except FileNotFoundError:
        print(f"Ошибка: файл конфигурации '{config_file}' не найден.")
        sys.exit(1)
    except json.JSONDecodeError:
        print("Ошибка: неверный формат файла конфигурации.")
        sys.exit(1)


def create_enigma(config, rotor_positions, plugboard_settings):
    """
    Создает объект Enigma на основе конфигурации.

    Параметры:
        config (dict): Конфигурация.

        rotor_positions (str): Начальные позиции роторов.

        plugboard_settings (list): Настройки коммутационной панели.

    Возвращает:
        Enigma: Объект Enigma.

    Исключения:
        KeyError: Если в конфигурации отсутствуют необходимые ключи.
        ValueError: Если настройки коммутационной панели или начальные позиции роторов неверны.
    """
    try:
        rotors = [Rotor(r['wiring'], r['notch']) for r in config['rotors']]
        reflector = Reflector(config['reflector']['wiring'])
    except KeyError as e:
        print(f"Ошибка отсутствует ключ {e} в конфигурации.")
        sys.exit(1)

    # Преобразуем настройки коммутационной панели
    plugboard = {}
    try:
        for pair in plugboard_settings:
            a, b = pair
            a_idx = 'АБВГДЕЁЖЗИЙКЛМНОПРСТУФХЦЧШЩЪЫЬЭЮЯ'.index(a)
            b_idx = 'АБВГДЕЁЖЗИЙКЛМНОПРСТУФХЦЧШЩЪЫЬЭЮЯ'.index(b)
            plugboard[a_idx] = b_idx
            plugboard[b_idx] = a_idx
    except ValueError as e:
        print(f"Ошибка: неверные настройки коммуникационной панели. {e}")
        sys.exit(1)

    enigma = Enigma(rotors, reflector, plugboard)
    try:
        enigma.set_rotor_positions(rotor_positions)
    except ValueError as e:
        print(f"Ошибка: неверные начальные позиции роторов. {e}")
        sys.exit(1)
    return enigma
