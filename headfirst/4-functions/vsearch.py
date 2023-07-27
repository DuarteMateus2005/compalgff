def search4vowels(phrase:str) -> set:
    """Returns any vowels found in a suppplied word."""
    vowels = {'a','e','i','o','u'}
    return vowels.intersection(set(phrase))


def search4letters(phrase:str, letters:str) -> set:
    """Returns a set of the "letters" found in "phrase"."""
    return set(letters).intersection(set(phrase))