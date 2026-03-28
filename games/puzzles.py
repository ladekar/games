import random

# Riddles: list of dicts with 'q' and 'a'
RIDDLES = [
    {"q": "I speak without a mouth and hear without ears. I have nobody, but I come alive with wind. What am I?",
     "a": "Echo"},
    {"q": "What has keys but can't open locks?", "a": "Piano"},
    {"q": "What runs all around a backyard, yet never moves?", "a": "Fence"},
]

# Simple math puzzles
MATH_PUZZLES = [
    {"q": "If 5 workers take 5 hours to make 5 widgets, how long for 1 worker to make 1 widget?", "a": 5},
    {"q": "What is 15% of 200?", "a": 30},
    {"q": "Solve: (8 * 3) + 12 / 4", "a": 26},
]

# Words for scramble
SCRAMBLES = [
    "python",
    "brain",
    "puzzle",
    "memory",
    "logic",
]

# Sequences: give a short sequence, ask next
SEQUENCES = [
    {"seq": [2, 4, 6], "next": 8},
    {"seq": [1, 1, 2, 3, 5], "next": 8},
    {"seq": [3, 9, 27], "next": 81},
]

# Items for short memory tests
MEMORY_ITEMS = [
    "48",
    "red apple",
    "7-2-9",
    "omega",
]


def sample_all():
    return {
        'riddle': random.choice(RIDDLES),
        'math': random.choice(MATH_PUZZLES),
        'scramble': random.choice(SCRAMBLES),
        'sequence': random.choice(SEQUENCES),
        'memory': random.choice(MEMORY_ITEMS),
    }
