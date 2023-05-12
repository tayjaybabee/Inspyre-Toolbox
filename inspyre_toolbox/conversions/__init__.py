

def format_bytes(size, round_to=2, auto_round=True):
    power = 2**10
    n = 0
    power_labels = {
        0: '',
        1: 'kilo',
        2: 'mega',
        3: 'giga',
        4: 'tera',
        5: 'peta',
        6: 'exa',
        7: 'zetta',
        8: 'yotta'
    }

    while size > power:
        size /= power
        n += 1

    if auto_round:
        size = round(size, round_to)

    return f"{size} {power_labels[n]}bytes"



