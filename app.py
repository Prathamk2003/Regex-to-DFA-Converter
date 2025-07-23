import streamlit as st # type: ignore
from nfa import NFA
from dfa import DFA
from transition import Transition

def parse_regex(regex):
    nfa = NFA()
    current_branch = nfa.start_state
    i = 0

    while i < len(regex):
        c = regex[i]

        if c == '(':
            group = []
            depth = 1
            i += 1
            while i < len(regex) and depth > 0:
                if regex[i] == '(':
                    depth += 1
                elif regex[i] == ')':
                    depth -= 1
                if depth > 0:
                    group.append(regex[i])
                i += 1

            group_nfa = parse_regex(''.join(group))

            if i < len(regex) and regex[i] == '*':
                group_nfa.kleene_star('G')
                i += 1

            # Connect with epsilon transition
            epsilon = Transition(nfa.current_state, group_nfa.start_state, 'E')
            nfa.current_state.add_out_transition(epsilon)
            group_nfa.start_state.add_in_transition(epsilon)
            
            nfa.current_state = group_nfa.current_state

        elif c.islower() or c.isdigit():
            nfa.concatenation(c)
            i += 1

        elif c == '*':
            nfa.kleene_star(regex[i-1])
            i += 1

        elif c == '|':
            new_branch = nfa.alternation(current_branch)
            current_branch = new_branch
            i += 1

        else:
            i += 1

    return nfa

def main():
    st.title("Regular Expression to Finite Automata Converter")
    st.markdown("""
    Supported operations:
    - Lowercase letters (a-z)
    - Digits (0-9)
    - Alternation (|)
    - Kleene star (*)
    - Grouping with parentheses ()
    """)

    # Empty input field with placeholder example
    regex = st.text_input("Enter regular expression:", 
                         placeholder="e.g., (a|b)*ab")

    if st.button("Convert"):
        try:
            if not regex:
                st.warning("Please enter a regular expression")
                return

            allowed_chars = set("abcdefghijklmnopqrstuvwxyz0123456789()*|")
            if not set(regex).issubset(allowed_chars):
                raise ValueError("Only a-z, 0-9, (), *, | allowed")

            with st.spinner("Processing..."):
                nfa = parse_regex(regex)
                dfa = DFA(nfa)

                st.subheader("NFA Transition Table")
                st.code(str(nfa))

                st.subheader("DFA Transition Table")
                st.code(str(dfa))

        except Exception as e:
            st.error(f"Error: {str(e)}")

if __name__ == "__main__":
    main()