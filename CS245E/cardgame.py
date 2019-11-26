from random import choice


def possible(c1, c2, c3):
    """
    Returns True if and only if c1, c2, c3 form a possible hand of cards.
    """
    cardlist = []
    for c in [c1, c2, c3]:
        cardlist.extend([c[0], c[1]])
    if cardlist.count("A") > 4 or cardlist.count("B") > 4:
        return False
    return True


def count_pairs(c1, c2):
    if c1 == "AB" and c2 == "AB":
        return 0
    elif c1 == "AB" or c2 == "AB":
        return 1
    else:
        return 2


class player:
    def __init__(self, cards, name):
        self.cards = cards
        self.name = name
        self.possible = ["AA", "AB", "BB"]
    
    def think(self, c1, c2, round, vol=0):
        """
        Tries to remove own possibilities, and returns True if solved.

        Step 1: Try to remove possibilities.
        Step 2: If the round number plus the number of pairs >= 3, solve with AB.
        """
        newpossible = []
        for c in self.possible:
            if possible(c, c1, c2):
                newpossible.append(c)
        self.possible = newpossible
        if len(self.possible) == 1:
            assert(self.possible[0] == self.cards)
            print(f"{self.name} solves with {self.possible[0]}.")
            return True
        elif round + count_pairs(c1, c2) >= 3:
            assert(self.cards == "AB")
            print(f"{self.name} solves with AB.")
            return True
        print(f"{self.name} passes.")
        return False
        

class game:
    def __init__(self, random=True, seed=0, custom=[], vol=0):
        self.turn = 0
        self.turncounter = 1
        self.vol = vol
        if random and custom == []:
            cards = ["A"] * 4 + ["B"] * 4
            deal = ["", "", ""]
            for _ in range(2):
                for i in range(len(deal)):
                    newcard = choice(cards)
                    cards.remove(newcard)
                    deal[i] += (newcard)
            deal = list(map(''.join, map(sorted, deal)))
        else:
            all = [
                ["AA", "AA", "BB"],  # 0
                ["AA", "AB", "AB"],
                ["AA", "AB", "BB"],
                ["AA", "BB", "AA"],
                ["AA", "BB", "AB"],
                ["AA", "BB", "BB"],  # 5
                ["AB", "AA", "AB"],
                ["AB", "AA", "BB"],
                ["AB", "AB", "AA"],
                ["AB", "AB", "AB"],
                ["AB", "AB", "BB"],  # 10
                ["AB", "BB", "AA"],
                ["AB", "BB", "AB"],
                ["BB", "AA", "AA"],
                ["BB", "AA", "AB"],
                ["BB", "AA", "BB"],  # 15
                ["BB", "AB", "AA"],
                ["BB", "AB", "AB"],
                ["BB", "BB", "AA"],
            ]
            deal = all[seed % len(all)]
        if custom != [] and custom in all:
            deal = custom
        self.p0 = player(deal[0], "P1")
        self.p1 = player(deal[1], "P2")
        self.p2 = player(deal[2], "P3")
        self.players = [self.p0, self.p1, self.p2]
        print(f"Players' hands: {deal}")
    
    def step(self):
        playing = self.players[self.turn]
        waiting = list(self.players)
        waiting.remove(playing)
        if self.vol >= 1:
            print(f"End of turn {self.turncounter}:")
        if playing.think(
            waiting[0].cards, waiting[1].cards,
            (self.turncounter) // 3, vol=self.vol):
            return True
        if self.vol >= 2:
            for a in range(3):
                print(
                    f"{self.players[a].name}: " + 
                    f"{self.players[a].cards} - " + 
                    f"{self.players[a].possible}"
                )
        self.turn = (self.turn + 1) % 3
        self.turncounter += 1
    
    def solve(self):
        while not self.step():
            continue
        return self.turncounter

"""
resultdict = {}
for i in range(19):
    g = game(random=False, seed=i, vol=0)
    resultdict[i] = g.solve()
print(resultdict)
"""

g = game(custom=["AB", "AB", "BB"])
g.solve()
