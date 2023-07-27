def search4vowels(word):
    """Displays any found vowels in an asked-for word."""
    vowels = {'a','e','i','o','u'}
    found = vowels.intersection(set(word))
    for vowel in found:
        print(vowel)