from state import State
from transition import Transition

class DFA:
    def __init__(self, nfa):
        self.start_state = State()
        self.states = {}
        self.alphabet = set()

        self._build_alphabet(nfa)
        self._convert(nfa)

    def _build_alphabet(self, nfa):
        visited = set()
        stack = [nfa.start_state]
        
        while stack:
            state = stack.pop()
            if state in visited:
                continue
            visited.add(state)
            
            for t in state.out_transitions:
                if t.symbol != 'E':
                    self.alphabet.add(t.symbol)
                stack.append(t.next_state)

    def _epsilon_closure(self, states):
        closure = set(states)
        stack = list(states)
        
        while stack:
            state = stack.pop()
            for t in state.out_transitions:
                if t.symbol == 'E' and t.next_state not in closure:
                    closure.add(t.next_state)
                    stack.append(t.next_state)
        return closure

    def _convert(self, nfa):
        initial = self._epsilon_closure({nfa.start_state})
        self.states[frozenset(initial)] = self.start_state
        queue = [initial]

        while queue:
            current = queue.pop(0)
            dfa_state = self.states[frozenset(current)]

            for symbol in self.alphabet:
                next_states = set()
                for state in current:
                    next_states.update(
                        t.next_state for t in state.out_transitions 
                        if t.symbol == symbol
                    )
                closure = self._epsilon_closure(next_states)
                
                if not closure:
                    continue
                
                key = frozenset(closure)
                if key not in self.states:
                    new_state = State()
                    self.states[key] = new_state
                    queue.append(closure)
                
                trans = Transition(dfa_state, self.states[key], symbol)
                dfa_state.add_out_transition(trans)
                self.states[key].add_in_transition(trans)

            if any(s.is_accept() for s in current):
                dfa_state.set_accept()

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
            for t in current.out_transitions:
                if t.next_state not in state_map:
                    state_map[t.next_state] = f"q{state_counter}"
                    state_counter += 1
                symbol = t.symbol
                transitions.setdefault(symbol, []).append(state_map[t.next_state])

            trans_str = "\n".join(
                [f"  {sym} → {', '.join(states)}" 
                 for sym, states in transitions.items()]
            )
            table.append(
                f"State {state_map[current]} {' '.join(state_info)}\n{trans_str}"
            )
            queue.extend(t.next_state for t in current.out_transitions)

        return "\n".join(table)