import random
import statistics
import time
class Strategy:
    def next_guess(self):
        return 

    def response(self, card):
        return

    def solved(self):
        """
        this should tell when your deck is solved perfectly for the rest of it
        return is a bool if it is true then it is solved false for needs to keep running
        """
        return 


class Say_what_you_see(Strategy):
    last_card = 0

    def next_guess(self):
        return self.last_card

    def response(self, card):
        self.last_card = card
        return

    def solved(self):
        return False


class Random_guess(Strategy):
    cards = set(range(13))

    def next_guess(self):
        return random.choice(tuple(self.cards))

    def response(self, card):
        return

    def solved(self):
        return False

    @staticmethod
    def solve(state=(13, 0, 0, 0, 0)):
        n = sum([x * (4 - i) for x, i in zip(state, range(len(state)))])
        return (12. / 13.) ** n


class Memories(Strategy):

    def __init__(self):
        self.seen = [set(range(13)), set(), set(), set(), set()]
        self.seenidx = 0

    def next_guess(self):
        self.seenidx += bool(self.seen[self.seenidx + 1])
        return random.choice(tuple(self.seen[self.seenidx]))

    def response(self, card):
        if not isinstance(card, (int, str)):
            raise TypeError("U R SO DUMB")

        for ndx in range(self.seenidx + 1):
            if card in self.seen[ndx]:
                self.seen[ndx].remove(card)
                self.seen[ndx + 1].add(card)
                return

    def solved(self):
        return bool(self.seen[4])

    @staticmethod
    def solve(state=(13, 0, 0, 0, 0)):
        wins = 0.
        n = sum([x * (4 - i) for x, i in zip(state, range(len(state)))])
        fringe = {n: {state: 1.}, }
        while fringe[n]:
            lwins = wins
            fringe[n - 1] = {}
            for state in fringe[n]:
                prop = fringe[n][state]
                if state[4]:
                    wins += prop
                    continue
                poss = 12
                for ndx in range(len(state)):
                    tpos = min(poss, state[ndx])
                    if not tpos:
                        continue
                    nprop = prop * tpos * (4 - ndx) / n
                    nstate = tuple([x - (i == ndx) + (i == ndx+1) for x, i in zip(state, range(len(state)))])
                    if nstate not in fringe[n - 1]:
                        fringe[n - 1][nstate] = 0.
                    fringe[n - 1][nstate] += nprop
                    poss -= tpos
            #print(n, wins - lwins, "\t",  len(fringe[n]))
            del fringe[n]
            n -= 1
        for state in fringe[n]:
            wins += fringe[n][state]
        return wins


def monte_carlo(strategy, tries):
    count = 0
    for _ in range(tries):
        deck = list(range(13)) * 4
        random.shuffle(deck)
        strat = strategy()
        while deck:
            if strat.solved():
                count += 1
                break
            next_card = deck.pop()
            ng = strat.next_guess()
            if ng == next_card:
                break
            strat.response(next_card)
        else:
            count += 1
    return count/tries
def sim(strat, tries, batches):
    print()
    print(batches, "batches of:", tries, "attempts using strategy", strat)
    now = time.time()
    r = []
    for _ in range(batches):
        print("{:3.3f}% done".format(_ / batches * 100), end="\r")
        r.append(monte_carlo(strat, tries))
    print("Total time: {:6.3f}s".format(time.time() - now))
    stdv = statistics.stdev(r)
    ci95 = 1.96 * stdv / (batches ** 0.5)
    mean = statistics.mean(r)
    print("there is a 95% chance that the mean is between {:3.6f}% and {:3.6f}%".format(
        (mean - ci95) * 100, (mean + ci95) * 100))


def main():

    tries = 10000
    batches = 4000
    for strat in [Memories, Random_guess, Say_what_you_see]:
        #sim(strat, tries, batches)
        if strat == Say_what_you_see:
            continue
        now = time.time()
        print("Exact answer calculated to be: {:3.6f}%".format(strat.solve() * 100))
        print("Total time: {:6.3f}s".format(time.time()-now))


if __name__ == '__main__':
    main()
