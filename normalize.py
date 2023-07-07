import re

CYRILLIC_SYMBOLS = "абвгдеёжзийклмнопрстуфхцчшщъыьэюяєіїґ"
TRANSLATION = ("a", "b", "v", "g", "d", "e", "e", "j", "z", "i", "j", "k", "l", \
               "m", "n", "o", "p", "r", "s", "t", "u", "f", "h", "ts", "ch", \
               "sh", "sch", "", "y", "", "e", "yu", "u", "ja", "je", "ji", "g")
TRANS = {}

for cyr_symb, letter in zip(CYRILLIC_SYMBOLS, TRANSLATION):
    TRANS[ord(cyr_symb)] = letter
    TRANS[ord(cyr_symb.upper())] = letter.upper()


def normalize(name: str) -> str:
    transl_name = name.translate(TRANS)
    transl_name = re.sub(r'\W', '_', transl_name)
    return transl_name