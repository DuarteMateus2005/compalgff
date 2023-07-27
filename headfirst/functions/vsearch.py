def search4vowels(word):
    """Returns a boolean based on any vowels found."""
    vowels = {'a','e','i','o','u'}
    found = vowels.intersection(set(word))
    return bool(found)