
class MarkovProb:
    def __init__(self):
        self.Next = {}
    def add_transition(self, state, next_state):
        if state not in self.Next:
            self.Next[state] = {}
        if next_state not in self.Next[state]:
            self.Next[state][next_state] = 0
        self.Next[state][next_state] += 1

if __name__ == "__main__":

