def search4letters(phrase:str, letters:str="aeiou") -> set:
    """Returns a set of the "letters" found in "phrase".If "letters" is not specified it returns any vowels found in a suppplied word."""
    return set(letters).intersection(set(phrase))