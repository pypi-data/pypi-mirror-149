LATIN_TO_CYRILLIC = {
    'a': 'а', 'A': 'А',
    'b': 'б', 'B': 'Б',
    'd': 'д', 'D': 'Д',
    'e': 'е', 'E': 'Е',
    'f': 'ф', 'F': 'Ф',
    'g': 'г', 'G': 'Г',
    'h': 'ҳ', 'H': 'Ҳ',
    'i': 'и', 'I': 'И',
    'j': 'ж', 'J': 'Ж',
    'k': 'к', 'K': 'К',
    'l': 'л', 'L': 'Л',
    'm': 'м', 'M': 'М',
    'n': 'н', 'N': 'Н',
    'o': 'о', 'O': 'О',
    'p': 'п', 'P': 'П',
    'q': 'қ', 'Q': 'Қ',
    'r': 'р', 'R': 'Р',
    's': 'с', 'S': 'С',
    't': 'т', 'T': 'Т',
    'u': 'у', 'U': 'У',
    'v': 'в', 'V': 'В',
    'x': 'х', 'X': 'Х',
    'y': 'й', 'Y': 'Й',
    'z': 'з', 'Z': 'З',
}


COMPOUNDS_FIRST_THREE_LETTERS = {
    "yo'": "йў", "Yo'": 'Йў', "YO'": "ЙЎ",
    "yo‘": "йў", "Yo‘": "Йў", "YO‘": "ЙЎ",
    "yoʻ": "йў", "Yoʻ": "Йў", "YOʻ": "ЙЎ",
}

COMPOUNDS_SECOND_DOUBLE_LETTERS = {
    'ch': 'ч', 'Ch': 'Ч', 'CH': 'Ч',
    'sh': 'ш', 'Sh': 'Ш', 'SH': 'Ш',
    'yo': 'ё', 'Yo': 'Ё', 'YO': 'Ё',
    'yu': 'ю', 'Yu': 'Ю', 'YU': 'Ю',
    'ya': 'я', 'Ya': 'Я', 'YA': 'Я',
    'ye': 'е', 'Ye': 'Е', 'YE': 'Е',
}

COMPOUNDS_THREE_WITH_APOSTROPHES = {
    "o'": "ў", "O'": "Ў",
    "o‘": "ў", "O‘": "Ў",
    "oʻ": "ў", "Oʻ": "Ў",

    "a'": "aъ", "A'": "Aъ",
    "a‘": "aъ", "A‘": "Aъ",
    "aʻ": "aъ", "Aʻ": "Aъ",

    "g'": "ғ", "G'": "Ғ",
    "g‘": "ғ", "G‘": "Ғ",
    "gʻ": "ғ", "Gʻ": "Ғ",
}

LATIN_APOSTROPHES = ["'", "‘", "ʻ"]

HARD_SIGN = "ъ"
SOFT_SIGN = "ь"

E_EXCEPTION = {'e': 'э', 'E': 'Э'}


def get_cyrillic_or_same_char(current_c, is_previous_space):
    if (current_c == 'e' or current_c == 'E') and is_previous_space:
        return 1, E_EXCEPTION[current_c]
    if current_c in LATIN_TO_CYRILLIC:
        return 1, LATIN_TO_CYRILLIC[current_c]
    return 1, current_c


def get_space_or_value_from_two_letters_down(current_c, next_c, is_previous_space):
    double_char = current_c + next_c
    if double_char in COMPOUNDS_SECOND_DOUBLE_LETTERS:
        return 2, COMPOUNDS_SECOND_DOUBLE_LETTERS[double_char]
    if double_char in COMPOUNDS_THREE_WITH_APOSTROPHES:
        return 2, COMPOUNDS_THREE_WITH_APOSTROPHES[double_char]
    return get_cyrillic_or_same_char(current_c, is_previous_space)


def get_space_or_value_from_three_letters_down(current_c, next_c, next_next_c, is_previous_space):
    triple_char = (current_c + next_c + next_next_c)
    if triple_char in COMPOUNDS_FIRST_THREE_LETTERS:
        return 3, COMPOUNDS_FIRST_THREE_LETTERS[triple_char]
    return get_space_or_value_from_two_letters_down(current_c, next_c, is_previous_space)


def latin_to_cyrillic(cyrillic_txt: str):
    original_length = len(cyrillic_txt)
    latin_txt = ""
    i = 0
    while i < original_length:
        current_c = cyrillic_txt[i]

        if current_c.isspace():
            latin_txt += current_c
            i += 1
            continue

        next_c = ' '
        next_next_c = ' '
        prev_c = ' '
        next_index = i + 1
        next_next_index = i + 2
        prev_index = i - 1

        if prev_index > 0:
            prev_c = cyrillic_txt[prev_index]
        is_prev_space = prev_c.isspace()

        if next_index < original_length:
            next_c = cyrillic_txt[next_index]

        if next_c.isspace():
            progress, char_ = get_cyrillic_or_same_char(current_c, is_prev_space)
            latin_txt += char_
            i += 1
            continue

        if next_next_index < original_length:
            next_next_c = cyrillic_txt[next_next_index]

        if next_next_c.isspace():
            progress, char_ = get_space_or_value_from_two_letters_down(current_c, next_c, is_prev_space)
            latin_txt += char_
            i += progress
            continue

        (progress, char_) = get_space_or_value_from_three_letters_down(current_c, next_c, next_next_c, is_prev_space)
        latin_txt += char_
        i += progress
    return latin_txt
