from state import State
from transition import Transition

class NFA:
    def __init__(self):
        self.start_state = State()
        self.current_state = self.start_state
        self.current_state.set_accept()

    def concatenation(self, symbol):
        new_state = State()
        transition = Transition(self.current_state, new_state, symbol)
        
        self.current_state.add_out_transition(transition)
        new_state.add_in_transition(transition)
        
        self.current_state.non_accept()
        new_state.set_accept()
        self.current_state = new_state

    def alternation(self, branch_state):
        new_state = State()
        epsilon = Transition(branch_state, new_state, 'E')
        branch_state.add_out_transition(epsilon)
        new_state.add_in_transition(epsilon)
        self.current_state = new_state
        return new_state

    def kleene_star(self, symbol):
        sequence_start = self.current_state
        while sequence_start.in_transitions:
            sequence_start = sequence_start.in_transitions[0].prev_state

        new_start = State()
        new_end = State()

        # Create epsilon transitions
        t1 = Transition(new_start, new_end, 'E')
        new_start.add_out_transition(t1)
        new_end.add_in_transition(t1)

        t2 = Transition(new_start, sequence_start, 'E')
        new_start.add_out_transition(t2)
        sequence_start.add_in_transition(t2)

        t3 = Transition(self.current_state, sequence_start, 'E')
        self.current_state.add_out_transition(t3)
        sequence_start.add_in_transition(t3)

        t4 = Transition(self.current_state, new_end, 'E')
        self.current_state.add_out_transition(t4)
        new_end.add_in_transition(t4)

        new_end.set_accept()
        self.current_state = new_end
        self.start_state = new_start

    def __repr__(self):
        visited = set()
        queue = [self.start_state]
        state_map = {self.start_state: "q0"}
        table = []
        state_counter = 1

        while queue:
            current = queue.pop(0)
            if current in visited:
                continue
            visited.add(current)

            state_info = []
            if current == self.start_state:
                state_info.append("(Start)")
            if current.is_accept():
                state_info.append("(Accepting)")
            
            transitions = {}
            for t in sorted(current.out_transitions, key=lambda x: (x.symbol != 'E', x.symbol)):
                if t.next_state not in state_map:
                    state_map[t.next_state] = f"q{state_counter}"
                    state_counter += 1
                symbol = 'ε' if t.symbol == 'E' else t.symbol
                transitions.setdefault(symbol, []).append(state_map[t.next_state])

            trans_str = "\n".join(
                [f"  {sym} → {', '.join(states)}" 
                 for sym, states in transitions.items()]
            )
            table.append(
                f"State {state_map[current]} {' '.join(state_info)}\n{trans_str}"
            )
            queue.extend(
                t.next_state for t in current.out_transitions 
                if t.next_state not in visited
            )

        return "\n".join(table)