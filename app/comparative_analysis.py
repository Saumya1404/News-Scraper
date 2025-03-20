def compare(keyword_dict):
    keyword_sets = {key: set(value) for key, value in keyword_dict.items()}
    common_keywords = set.intersection(*keyword_sets.values())
    unique_keywords = {key: value - common_keywords for key, value in keyword_sets.items()}
    return {
        'common_keywords': list(common_keywords),
        'unique_keywords': {k:list(v) for k,v in unique_keywords.items()}
    }