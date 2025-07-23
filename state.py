class State:
    def __init__(self):
        self.in_transitions = []
        self.out_transitions = []
        self.accept_state = False

    def is_accept(self):
        return self.accept_state

    def set_accept(self):
        self.accept_state = True

    def non_accept(self):
        self.accept_state = False

    def add_out_transition(self, transition):
        self.out_transitions.append(transition)

    def add_in_transition(self, transition):
        self.in_transitions.append(transition)

    def remove_in_transition(self, transition):
        if transition in self.in_transitions:
            self.in_transitions.remove(transition)

    def remove_out_transition(self, transition):
        if transition in self.out_transitions:
            self.out_transitions.remove(transition)

    def delete_state(self):
        for t in self.out_transitions.copy():
            t.next_state.remove_in_transition(t)
        self.out_transitions.clear()
        
        for t in self.in_transitions.copy():
            t.prev_state.remove_out_transition(t)
        self.in_transitions.clear()

    def __repr__(self):
        return f"State({id(self)})"