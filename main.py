import random, re
from collections import defaultdict, Counter
from typing import List, Tuple, Dict
import sys

def tokenize_words(text: str) -> List[str]:
    text = re.sub(r"\s+", " ", text.strip())
    text = re.sub(r"([.,!?;:()\[\]\"'])", r" \1 ", text)
    return [t for t in text.split(" ") if t]

def build_markov(tokens: List[str], order: int) -> Dict[Tuple[str, ...], Counter]:
    model: Dict[Tuple[str, ...], Counter] = defaultdict(Counter)
    for i in range(len(tokens) - order):
        state = tuple(tokens[i:i+order])
        nxt = tokens[i+order]
        model[state][nxt] += 1
    return model

def weighted_choice(counter: Counter) -> str:
    total = sum(counter.values())
    r = random.randint(1, total)
    cum = 0
    for token, cnt in counter.items():
        cum += cnt
        if r <= cum:
            return token
    return random.choice(list(counter.keys()))

def generate(model, seed: Tuple[str,...], length: int) -> List[str]:
    state = seed
    out = list(state)
    for _ in range(length):
        if state not in model or not model[state]:
            state = random.choice(list(model.keys()))
        nxt = weighted_choice(model[state])
        out.append(nxt)
        state = tuple(out[-len(state):])
    return out

def detokenize_words(tokens: List[str]) -> str:
    out = []
    for i, t in enumerate(tokens):
        if i > 0 and t in ".,!?;:)]'\"" :
            out[-1] = out[-1].rstrip()
            out.append(t)
        elif t in "([\"'":
            out.append(t)
        else:
            out.append(" " + t)
    return "".join(out).strip()

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("usage: python main.py data.txt")
        sys.exit(1)

    with open(sys.argv[1], "r", encoding="utf-8") as f:
        text = f.read()

    tokens = tokenize_words(text)
    order = 2
    model = build_markov(tokens, order)

    print("GbMCM is started.")
    while True:
        user_inp = input("you: ").strip()
        if user_inp.lower() in ["exit", "quit", "q"]:
            break
        seed = tuple(user_inp.split()[:order])
        if len(seed) < order or seed not in model:
            seed = random.choice(list(model.keys()))
        reply_tokens = generate(model, seed, 30)
        print("LM:", detokenize_words(reply_tokens))
