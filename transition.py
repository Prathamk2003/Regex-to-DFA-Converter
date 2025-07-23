class Transition:
    def __init__(self, prev_state, next_state, symbol):
        self.prev_state = prev_state
        self.next_state = next_state
        self.symbol = symbol

    def __repr__(self):
        symbol = 'ε' if self.symbol == 'E' else self.symbol
        return f"{self.prev_state} --{symbol}--> {self.next_state}"