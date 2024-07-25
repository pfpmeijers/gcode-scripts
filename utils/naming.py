from re import findall, sub


def snake_to_label_case(s):
    s = f'{s[0].upper()}{s[1:].replace("_", " ")}'
    return s


def camel_to_label_case(sc):
    sl = ''
    for words, separators in findall(r'(\w+)(\W*)', sc):
        words = findall(r'[A-Z][a-z0-9]*', words)
        words = ' '.join([word if i == 0 else word.lower() for i, word in enumerate(words)])
        sl = f'{sl}{words}{separators}'
    return sl


def camel_to_snake_case(s):
    s = sub(r'(?<!^)(?=[A-Z])', '_', s).lower()
    return s