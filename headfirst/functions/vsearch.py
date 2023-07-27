def search4vowels(word):
    """Returns any vowels found in a suppplied word."""
    vowels = {'a','e','i','o','u'}
    found = vowels.intersection(set(word))
    return found