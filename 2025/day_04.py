from utils import read, print_answers

raw = read(2025, 4).split("\n")

coords = {i + 1j * j: x for i, line in enumerate(raw) for j, x in enumerate(line)}
papers = {k for k, v in coords.items() if v == "@"}


def is_accessible(p, papers):
    s = 0
    for i in (-1, 0, 1):
        for j in (-1, 0, 1):
            if i == j == 0:
                continue
            n = p + i + 1j * j
            if n in papers:
                s += 1
            if s >= 4:
                return False
    return True


def remove_and_count(papers, max_rounds):
    papers = papers.copy()
    tally = set()
    for _ in range(max_rounds):
        removed = {p for p in papers if is_accessible(p, papers)}
        if not removed:
            break
        tally |= removed
        papers -= removed
    return len(tally)


a1 = remove_and_count(papers, 1)
a2 = remove_and_count(papers, 1000)

print_answers(a1, a2, day=4)
