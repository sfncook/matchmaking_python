from fuzzywuzzy import fuzz
from fuzzywuzzy import process

def find_most_similar_strings(target, string_list, max_results):
    # Preprocess the target string
    target_clean = ''.join(e for e in target if e.isalnum()).lower()

    # Preprocess the list strings and keep a mapping to original strings
    string_list_clean = [''.join(e for e in s if e.isalnum()).lower() for s in string_list]

    # Use fuzzy matching to find the top N most similar strings
    matches = process.extract(target_clean, string_list_clean, scorer=fuzz.ratio, limit=max_results)

    # Extract the original strings corresponding to the best matches
    best_matches = [string_list[string_list_clean.index(match[0])] for match in matches]

    return best_matches

if __name__ == '__main__':
    # Example usage
    target_string = "example string"
    list_of_strings = ["Example string!", "Sample text", "examlpe strng", "Completely different string", "Ex@mple Str!ng"]
    max_results = 2

    similar_strings = find_most_similar_strings(target_string, list_of_strings, max_results)
    print(similar_strings)
