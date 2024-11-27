import argparse
import sys
from enigma import load_config, create_enigma

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
    if len(positions) != 3:
        print("Ошибка: необходимо указать три начальные позиции роторов.")
        sys.exit(1)

    config = load_config(config_file)
    enigma = create_enigma(config, positions, plugboard)
    result = enigma.encode_text(text)
    print(f"Результат: {result}")


if __name__ == "__main__":
    main()
