import os
import random
import time
from puzzles import RIDDLES, MATH_PUZZLES, SCRAMBLES, SEQUENCES, MEMORY_ITEMS


def clear_screen():
    os.system('cls' if os.name == 'nt' else 'clear')


def ask_riddle():
    r = random.choice(RIDDLES)
    print('\nRiddle:')
    print(r['q'])
    ans = input('Your answer: ').strip().lower()
    correct = r['a'].lower()
    if correct in ans or ans in correct:
        print('Correct!')
        return 1
    else:
        print(f'Wrong. Answer: {r["a"]}')
        return 0


def ask_math():
    p = random.choice(MATH_PUZZLES)
    print('\nMath Puzzle:')
    print(p['q'])
    try:
        ans = input('Your answer: ').strip()
        if float(ans) == float(p['a']):
            print('Correct!')
            return 1
    except Exception:
        pass
    print(f'Wrong. Answer: {p["a"]}')
    return 0


def ask_scramble():
    word = random.choice(SCRAMBLES)
    scrambled = ''.join(random.sample(word, len(word)))
    while scrambled == word:
        scrambled = ''.join(random.sample(word, len(word)))
    print('\nUnscramble the word:')
    print(scrambled)
    ans = input('Your answer: ').strip().lower()
    if ans == word.lower():
        print('Correct!')
        return 1
    else:
        print(f'Wrong. Answer: {word}')
        return 0


def ask_sequence():
    s = random.choice(SEQUENCES)
    seq = s['seq']
    print('\nSequence:')
    print(', '.join(str(x) for x in seq))
    ans = input('Next number: ').strip()
    try:
        if int(ans) == int(s['next']):
            print('Correct!')
            return 1
    except Exception:
        pass
    print(f'Wrong. Answer: {s["next"]}')
    return 0


def memory_test():
    item = random.choice(MEMORY_ITEMS)
    print('\nMemory test: Memorize the item shown (you have 4 seconds)')
    print('\n>>>', item, '\n')
    time.sleep(4)
    clear_screen()
    ans = input('Type the item you saw: ').strip().lower()
    if ans == str(item).lower():
        print('Correct!')
        return 1
    else:
        print(f'Wrong. Item was: {item}')
        return 0
def menu(auto_submit=False, submit_host='127.0.0.1', submit_port=5000, submit_source='brain-tease'):
    score = 0
    played = 0
    handlers = [
        ('Riddles', ask_riddle),
        ('Math puzzles', ask_math),
        ('Word scramble', ask_scramble),
        ('Sequence/Pattern', ask_sequence),
        ('Memory test', memory_test),
    ]

    while True:
        print('\n=== Brain Tease & Mindset ===')
        print(f'Score: {score}  Played: {played}')
        for i, (name, _) in enumerate(handlers, start=1):
            print(f'{i}. {name}')
        print('6. Timed round')
        print('7. Random mix')
        print('8. Quit')
        try:
            choice = input('Choose a category: ').strip()
        except EOFError:
            print('\nInput ended. Exiting.')
            return score

        if choice == '8':
            print('\nThanks for playing! Final score:', score)
            return score
        try:
            num = int(choice)
        except Exception:
            print('Invalid choice')
            continue
        if num == 6:
            played += 1
            score += timed_round()
            continue
        if num == 7:
            func = random.choice([h for _, h in handlers])
        elif 1 <= num <= len(handlers):
            func = handlers[num - 1][1]
        else:
            print('Invalid choice')
            continue

        played += 1
        try:
            score += func()
        except EOFError:
            print('\nInput ended. Exiting.')
            return score


def timed_round():
    try:
        qn = int(input('How many questions for the timed round (default 5)? ').strip() or 5)
    except Exception:
        qn = 5
    try:
        limit = float(input('Seconds allowed per question (default 10): ').strip() or 10.0)
    except Exception:
        limit = 10.0

    print(f"\nStarting timed round: {qn} questions, {limit}s each")
    score = 0
    for i in range(qn):
        print(f"\nQuestion {i+1}/{qn}")
        handler = random.choice([ask_riddle, ask_math, ask_scramble, ask_sequence, memory_test])
        start = time.time()
        try:
            result = handler()
        except EOFError:
            print('\nInput ended. Exiting timed round.')
            return score
        elapsed = time.time() - start
        if elapsed > limit:
            print(f'Timeout ({elapsed:.1f}s > {limit}s). No point awarded.')
        else:
            score += result
            print(f'Answered in {elapsed:.1f}s.')
    print(f'\nTimed round finished. Score: {score}/{qn}')
    return score


if __name__ == '__main__':
    import argparse
    from submit_score import submit as submit_score

    p = argparse.ArgumentParser()
    p.add_argument('--auto-submit', action='store_true', help='Auto-submit final score to leaderboard')
    p.add_argument('--submit-host', default='127.0.0.1', help='Leaderboard host')
    p.add_argument('--submit-port', default=5000, type=int, help='Leaderboard port')
    p.add_argument('--submit-source', default='brain-tease', help='Source identifier for leaderboard')
    args = p.parse_args()

    try:
        final = menu(auto_submit=args.auto_submit,
                     submit_host=args.submit_host,
                     submit_port=args.submit_port,
                     submit_source=args.submit_source)
    except KeyboardInterrupt:
        print('\nGoodbye!')
        final = None

    # If we have a final score, ask to submit or auto-submit
    try:
        if final and final > 0:
            name = None
            if args.auto_submit:
                name = os.environ.get('USER') or input('Enter name to submit score: ').strip()
            else:
                ans = input('Submit this score to leaderboard? (y/N): ').strip().lower()
                if ans == 'y':
                    name = input('Enter name to submit score: ').strip()

            if name:
                try:
                    # fetch current leaderboard top entries and check if we should submit
                    import urllib.request
                    import json

                    def get_best_for(name, host, port, source):
                        try:
                            url = f'http://{host}:{port}/api/leaderboard'
                            with urllib.request.urlopen(url, timeout=3) as r:
                                data = json.load(r)
                        except Exception:
                            return None
                        for e in data.get('leaderboard', []):
                            if e.get('name') == name and e.get('source', source) == source:
                                try:
                                    return int(e.get('score', 0))
                                except Exception:
                                    return None
                        return None

                    best = get_best_for(name, args.submit_host, args.submit_port, args.submit_source)
                    if best is None or final > best:
                        submit_score(name, final, host=args.submit_host, port=args.submit_port, source=args.submit_source)
                        print('Score submitted.')
                    else:
                        print(f'Not submitted — current best for {name} is {best} >= {final}.')
                except Exception as e:
                    print('Failed to submit score check/submit:', e)
    except EOFError:
        pass
