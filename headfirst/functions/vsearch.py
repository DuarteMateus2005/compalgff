def search4vowels(word:str): # -> set:
    """Returns any vowels found in a suppplied word."""
    vowels = {'a','e','i','o','u'}
    return vowels.intersection(set(word))