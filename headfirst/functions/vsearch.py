def search4vowels(word):
    """Returns any vowels found in a suppplied word."""
    vowels = {'a','e','i','o','u'}
    return vowels.intersection(set(word))