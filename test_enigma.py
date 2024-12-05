import pytest
from enigma import Enigma, Rotor, Reflector, load_config
from unittest.mock import mock_open, patch

@pytest.fixture
def sample_config():
    """ Фикстура для предоставления примерной конфигурации машины Энигма.
    Возвращает словарь с настройками роторов и рефлектора. """
    return {
        "rotors": [
            {"wiring": [4, 10, 12, 5, 11, 6, 3, 16, 21, 25, 13, 19, 14, 22, 24, 7, 23, 20, 18, 15, 0, 8, 1, 17, 2, 9,
                        26, 27, 28, 29, 30, 31, 32], "notch": 5},
            {"wiring": [0, 9, 3, 10, 18, 8, 17, 20, 23, 1, 11, 7, 22, 19, 12, 2, 16, 6, 25, 13, 15, 24, 5, 21, 14, 4,
                        26, 27, 28, 29, 30, 31, 32], "notch": 10},
            {"wiring": [1, 3, 5, 7, 9, 11, 2, 15, 17, 19, 23, 21, 25, 13, 24, 4, 8, 22, 6, 0, 10, 12, 20, 18, 16, 14,
                        26, 27, 28, 29, 30, 31, 32], "notch": 15}
        ],
        "reflector": {
            "wiring": [24, 17, 20, 7, 16, 18, 11, 3, 15, 23, 13, 6, 14, 10, 12, 8, 4, 1, 5, 25, 2, 22, 21, 9, 0, 19, 26,
                       27, 28, 29, 30, 31, 32]
        }
    }


@pytest.fixture
def basic_enigma(sample_config):
    """Фикстура для создания базовой машины Энигма с примерной конфигурацией.
    Возвращает объект Enigma с установленными роторами и рефлектором. """
    rotors = [Rotor(r['wiring'], r['notch']) for r in sample_config['rotors']]
    reflector = Reflector(sample_config['reflector']['wiring'])
    return Enigma(rotors, reflector, {})


def test_rotor_position_setting(basic_enigma):
    """ Тестирует установку начальных позиций роторов.
    Проверяет, что позиции роторов соответствуют заданным символам. """
    positions = "АБВ"
    basic_enigma.set_rotor_positions(positions)
    assert [r.position for r in basic_enigma.rotors] == [0, 1, 2]

@pytest.mark.parametrize("text,positions", [
    ("ПРИВЕТ", "АБВ"),
    ("ТЕСТСООБЩЕНИЕ", "ЖЗИ"),
    ("PYTHON", "ЮЯА")
])

def test_encryption_decryption(basic_enigma, text, positions):
    """ Тестирует шифрование и дешифрование текста с разными начальными позициями роторов.
        Проверяет, что текст после шифрования и последующего дешифрования совпадает с исходным. """
    basic_enigma.set_rotor_positions(positions)
    encrypted = basic_enigma.encode_text(text)

    # Сброс позиций для дешифрования
    basic_enigma.set_rotor_positions(positions)
    decrypted = basic_enigma.encode_text(encrypted)

    assert decrypted == text


def test_different_positions_fail(basic_enigma):
    """Проверяет, что шифрование и дешифрование с разными начальными позициями роторов приводит к различным результатам. """
    text = "ТЕСТОВОЕСООБЩЕНИЕ"

    # Шифруем с первой позицией
    basic_enigma.set_rotor_positions("АБВ")
    encrypted = basic_enigma.encode_text(text)

    # Пытаемся расшифровать с другой позицией
    basic_enigma.set_rotor_positions("ГДЕ")
    decrypted = basic_enigma.encode_text(encrypted)

    assert decrypted != text

    # Дополнительная проверка - расшифровка с правильной позицией должна работать
    basic_enigma.set_rotor_positions("АБВ")
    correct_decrypted = basic_enigma.encode_text(encrypted)
    assert correct_decrypted == text


@pytest.mark.parametrize("plugboard_pairs", [
    [("А", "Б"), ("В", "Г")],
    [("Е", "Ж"), ("З", "И"), ("К", "Л")],
    []
])

def test_plugboard_settings(sample_config, plugboard_pairs):
    """ Тестирует работу машины Энигма с различными настройками коммутационной панели.
        Проверяет, что текст после шифрования и последующего дешифрования совпадает с исходным. """
    plugboard = {}
    for a, b in plugboard_pairs:
        a_idx = 'АБВГДЕЁЖЗИЙКЛМНОПРСТУФХЦЧШЩЪЫЬЭЮЯ'.index(a)
        b_idx = 'АБВГДЕЁЖЗИЙКЛМНОПРСТУФХЦЧШЩЪЫЬЭЮЯ'.index(b)
        plugboard[a_idx] = b_idx
        plugboard[b_idx] = a_idx

    rotors = [Rotor(r['wiring'], r['notch']) for r in sample_config['rotors']]
    reflector = Reflector(sample_config['reflector']['wiring'])
    enigma = Enigma(rotors, reflector, plugboard)

    text = "ТЕСТ"
    enigma.set_rotor_positions("АБВ")
    encrypted = enigma.encode_text(text)

    enigma.set_rotor_positions("АБВ")
    decrypted = enigma.encode_text(encrypted)

    assert decrypted == text


def test_invalid_input_file():
    """ Тестирует обработку ошибок при загрузке конфигурации из файла.
        Проверяет, что выбрасываются соответствующие исключения для несуществующего файла, некорректного JSON и некорректной структуры конфигурации. """
    # Тест на несуществующий файл
    with pytest.raises(FileNotFoundError):
        load_config("nonexistent.json")

    # Тест на некорректный JSON
    invalid_json = '{"rotors": [invalid json]}'
    with patch('builtins.open', mock_open(read_data=invalid_json)):
        # Используя patch, функция open заменяется на mock_open, которая будет возвращать строку invalid_json, когда программа попытается открыть файл config.json.
        # Это позволяет тестировать поведение функции load_config без необходимости создания реального файла.
        with pytest.raises(ValueError):
            load_config("config.json")

    # Тест на некорректную структуру конфигурации
    invalid_config = '{"wrong_key": []}'
    with patch('builtins.open', mock_open(read_data=invalid_config)):
        with pytest.raises(KeyError):
            load_config("config.json")


def test_special_characters(basic_enigma):
    """ Проверяет обработку специальных символов в тексте.
       Убеждается, что длина результата шифрования совпадает с длиной исходного текста. """
    text = "ТЕСТ 123 .,!"
    basic_enigma.set_rotor_positions("АБВ")
    result = basic_enigma.encode_text(text)
    assert len(result) == len(text)


def test_empty_input(basic_enigma):
    """ Проверяет обработку пустого ввода.
        Убеждается, что шифрование пустой строки возвращает пустую строку. """
    basic_enigma.set_rotor_positions("АБВ")
    assert basic_enigma.encode_text("") == ""


def test_different_rotor_configuration():
    """ Тестирует работу двух машин Энигма с разными конфигурациями роторов.
        Проверяет, что результаты шифрования различаются, и каждая машина корректно шифрует и дешифрует текст. """
    # Создаем две разные конфигурации роторов
    config1 = {
        "rotors": [
            {"wiring": [4, 10, 12, 5, 11, 6, 3, 16, 21, 25, 13, 19, 14, 22, 24, 7, 23, 20, 18, 15, 0, 8, 1, 17, 2, 9,
                        26, 27, 28, 29, 30, 31, 32], "notch": 5},
            {"wiring": [0, 9, 3, 10, 18, 8, 17, 20, 23, 1, 11, 7, 22, 19, 12, 2, 16, 6, 25, 13, 15, 24, 5, 21, 14, 4,
                        26, 27, 28, 29, 30, 31, 32], "notch": 10},
            {"wiring": [1, 3, 5, 7, 9, 11, 2, 15, 17, 19, 23, 21, 25, 13, 24, 4, 8, 22, 6, 0, 10, 12, 20, 18, 16, 14,
                        26, 27, 28, 29, 30, 31, 32], "notch": 15}
        ],
        "reflector": {
            "wiring": [24, 17, 20, 7, 16, 18, 11, 3, 15, 23, 13, 6, 14, 10, 12, 8, 4, 1, 5, 25, 2, 22, 21, 9, 0, 19, 26,
                       27, 28, 29, 30, 31, 32]
        }
    }

    config2 = {
        "rotors": [
            {"wiring": [24, 17, 20, 7, 16, 18, 11, 3, 15, 23, 13, 6, 14, 10, 12, 8, 4, 1, 5, 25, 2, 22, 21, 9, 0, 19,
                        26, 27, 28, 29, 30, 31, 32], "notch": 5},  # Другая проводка первого ротора
            {"wiring": [0, 9, 3, 10, 18, 8, 17, 20, 23, 1, 11, 7, 22, 19, 12, 2, 16, 6, 25, 13, 15, 24, 5, 21, 14, 4,
                        26, 27, 28, 29, 30, 31, 32], "notch": 10},
            {"wiring": [1, 3, 5, 7, 9, 11, 2, 15, 17, 19, 23, 21, 25, 13, 24, 4, 8, 22, 6, 0, 10, 12, 20, 18, 16, 14,
                        26, 27, 28, 29, 30, 31, 32], "notch": 15}
        ],
        "reflector": {
            "wiring": [24, 17, 20, 7, 16, 18, 11, 3, 15, 23, 13, 6, 14, 10, 12, 8, 4, 1, 5, 25, 2, 22, 21, 9, 0, 19, 26,
                       27, 28, 29, 30, 31, 32]
        }
    }

    # Создаем две машины Энигма с разными конфигурациями
    enigma1 = Enigma(
        [Rotor(r['wiring'], r['notch']) for r in config1['rotors']],
        Reflector(config1['reflector']['wiring']),
        {}
    )

    enigma2 = Enigma(
        [Rotor(r['wiring'], r['notch']) for r in config2['rotors']],
        Reflector(config2['reflector']['wiring']),
        {}
    )

    # Устанавливаем одинаковые начальные позиции
    test_text = "ТЕСТОВОЕСООБЩЕНИЕ"
    start_position = "АБВ"

    enigma1.set_rotor_positions(start_position)
    enigma2.set_rotor_positions(start_position)

    # Проверяем, что результаты шифрования различаются
    result1 = enigma1.encode_text(test_text)
    result2 = enigma2.encode_text(test_text)

    assert result1 != result2

    # Дополнительная проверка - каждая машина должна корректно шифровать/дешифровать
    enigma1.set_rotor_positions(start_position)
    decrypted1 = enigma1.encode_text(result1)
    assert decrypted1 == test_text

    enigma2.set_rotor_positions(start_position)
    decrypted2 = enigma2.encode_text(result2)
    assert decrypted2 == test_text
