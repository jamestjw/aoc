from collections import Counter


inp_lines = open("input.txt", "r", encoding="utf-8").read().split("\n")
hands = [tuple(l.split()) for l in inp_lines]


def tiebreaks(hand, strengths):
    indices = tuple([strengths[::-1].index(card) for card in hand])

    return int("".join([hex(i)[-1] for i in indices]), 16) / 0xFFFFF


def hand_strength_pt2(hand):
    tb = tiebreaks(hand, strengths="AKQT98765432J")
    counter = Counter(hand)
    counterWithoutJ = Counter([card for card in hand if card != "J"])
    jokerCount = counter["J"]

    if 5 in counter.values():
        return 40 + tb
    elif 4 in counterWithoutJ.values():
        match jokerCount:
            case 1:
                return 40 + tb  # 5 kind
            case _:
                return 30 + tb
    elif 2 in counter.values() and 3 in counter.values():
        if jokerCount in (3, 2):
            return 40 + tb  # 5 kind
        else:
            return 25 + tb
    elif 3 in counterWithoutJ.values():
        match jokerCount:
            case 1:
                return 30 + tb  # 4 kind
            case 2:
                return 40 + tb  # 5 kind
            case _:
                return 20 + tb
    elif 2 == len([v for v in counterWithoutJ.values() if v == 2]):
        match jokerCount:
            case 1:
                return 25 + tb  # Fullhouse
            case _:
                return 15 + tb
    elif 1 == len([v for v in counterWithoutJ.values() if v == 2]):
        match jokerCount:
            case 1:
                return 20 + tb  # 3 kind
            case 2:
                return 30 + tb  # 4 kind
            case 3:
                return 40 + tb  # 5 kind
            case _:
                return 10 + tb

    else:
        match jokerCount:
            case 1:
                return 10 + tb  # 1 pair
            case 2:
                return 20 + tb  # 3 kind
            case 3:
                return 30 + tb  # 4 kind
            case 4 | 5:
                return 40 + tb  # 5 kind
            case _:
                return tb  # High card


def hand_strength_pt1(hand):
    tb = tiebreaks(hand, strengths="AKQT98765432J")
    counter = Counter(hand)
    maxCount = max(counter.values())

    match maxCount:
        case 5:
            return 50 + tb
        case 4:
            return 40 + tb
        case 3:
            if 2 in counter.values():  # Fullhouse
                return 35 + tb
            else:
                return 30 + tb  # Three kind
        case 2:  # At least a pair
            numpairs = len([v for v in counter.values() if v == 2])
            if numpairs == 2:
                return 25 + tb
            else:
                return 20 + tb
        case _:
            # High card
            return tb


sortedHands = sorted(hands, key=lambda x: hand_strength_pt1(x[0]))
sortedHands2 = sorted(hands, key=lambda x: hand_strength_pt2(x[0]))

# 248179786 247885995
print(sum((i + 1) * int(v) for i, (_, v) in enumerate(sortedHands)))
print(sum((i + 1) * int(v) for i, (_, v) in enumerate(sortedHands2)))
