 Программа принимает на вход положение 3 роторов, настройки соединительной панели и текст. В результате программа выводит получившийся текст. Программа работает как через текстовый интерфейс так и через командную строку. Конфигурация роторов и рефлектора задается через файл конфигурации машины (текстовый файл с конфигурацией роторов и рефлектора) 

Через командную строку:

```python enigma.py --config <файл конфигурации(по одной букве на ротор)> --positions <позиции роторов> --plugboard <настройки коммутационной панели (пары букв, которые соединяются)> --text <текст который нужно зашифровать>```

Через текстовый интерфейс (запуск без параметров):

```python enigma.py```

Файл config.json - это конфигурационный файл, который содержит настройки роторов и рефлектора машины Enigma. Он написан в формате JSON и определяет, как именно будут осуществляться замены букв в каждом роторе и рефлекторе.
Пример как создать свой config.json
```json
# Создаем конфигурацию для русского алфавита (33 буквы)

config = {
    "rotors": [
        {
            # Первый ротор - случайная перестановка индексов
            "wiring": [4, 10, 12, 5, 11, 6, 3, 16, 21, 25, 13, 19, 14, 22, 24, 
                      7, 23, 20, 18, 15, 0, 8, 1, 17, 2, 9, 26, 27, 28, 29, 30, 31, 32],
            "notch": 16
        },
        {
            # Второй ротор - другая случайная перестановка
            "wiring": [0, 9, 3, 10, 18, 8, 17, 20, 23, 1, 11, 7, 22, 19, 12, 
                      2, 16, 6, 25, 13, 15, 24, 5, 21, 14, 4, 26, 27, 28, 29, 30, 31, 32],
            "notch": 4
        },
        {
            # Третий ротор - еще одна случайная перестановка
            "wiring": [1, 3, 5, 7, 9, 11, 2, 15, 17, 19, 23, 21, 25, 13, 24, 
                      4, 8, 22, 6, 0, 10, 12, 20, 18, 16, 14, 26, 27, 28, 29, 30, 31, 32],
            "notch": 21
        }
    ],
    "reflector": {
        # Рефлектор - симметричная перестановка
        "wiring": [24, 17, 20, 7, 16, 18, 11, 3, 15, 23, 13, 6, 14, 10, 12, 
                  8, 4, 1, 5, 25, 2, 22, 21, 9, 0, 19, 26, 27, 28, 29, 30, 31, 32]
    }
}
```
Важные замечания:
1) Числа в wiring должны быть в диапазоне от 0 до 32 (для русского алфавита)
2) Каждое число должно использоваться только один раз в пределах одного ротора
3) В рефлекторе соединения должны быть парными (если A соединено с B, то B должно быть соединено с A)
4) Значение notch должно быть в диапазоне от 0 до 32
5) Индексы соответствуют буквам русского алфавита в порядке: 'АБВГДЕЁЖЗИЙКЛМНОПРСТУФХЦЧШЩЪЫЬЭЮЯ'

