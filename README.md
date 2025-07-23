# Regex-to-DFA-Converter


This project provides a Streamlit web application that converts regular expressions into their corresponding Nondeterministic Finite Automata (NFA) and Deterministic Finite Automata (DFA) representations. It's a helpful tool for understanding how regular expressions are processed by finite automata.

✨ Features
- Regular Expression Parsing: Converts a given regular expression into an NFA.
- NFA to DFA Conversion: Transforms the generated NFA into an equivalent DFA using the subset construction algorithm.
- Interactive Web Interface: Built with Streamlit for an easy-to-use web interface.
- Supported Operations:
  - Lowercase letters (a-z)
  - Digits (0-9)
  - Alternation (|)
  - Kleene star (*)
  - Grouping with parentheses ()

🛠️ Installation
1. Clone the repository:
```Bash
git clone https://github.com/your-username/regex-to-automata.git
cd regex-to-automata
```
2. Create a virtual environment (recommended):
```Bash
python -m venv venv
source venv/bin/activate  # On Windows: `venv\Scripts\activate`
```
3. Install the required dependencies:
```Bash
pip install -r requirements.txt
```
(You'll need to create a requirements.txt file. See "Usage" for its content).

🚀 Usage
To run the Streamlit application, execute the following command in your terminal:
```Bash
streamlit run app.py
```
This will open the application in your web browser.

requirements.txt

Create a file named requirements.txt in the root of your project with the following content:
```bash
streamlit
```

📂 Project Structure
```bash
app.py: The main Streamlit application file that handles user input, regex parsing, and displays the NFA and DFA.
nfa.py: Contains the NFA class, responsible for constructing the NFA from a regular expression.
dfa.py: Contains the DFA class, which implements the conversion from NFA to DFA.
state.py: Defines the State class, representing a state in an automaton.
transition.py: Defines the Transition class, representing a transition between states.
```

💡 How it Works
The application follows these main steps:
- Parsing Regular Expression: The parse_regex function in app.py recursively builds an NFA based on the input regular expression. It handles concatenation, alternation, Kleene star, and grouping.
- NFA Construction: The NFA class manages the states and transitions of the Nondeterministic Finite Automaton. Operations like concatenation, alternation, and kleene_star add states and transitions to the NFA.
- NFA to DFA Conversion: The DFA class takes the constructed NFA and applies the subset construction algorithm to create an equivalent DFA. This involves:
  - Calculating epsilon closures for sets of NFA states.
  - Determining transitions for each input symbol based on these sets.
  - Identifying accepting states in the DFA based on whether their corresponding NFA state sets contain any accepting NFA states.
- Display: The NFA and DFA transition tables are displayed in a human-readable format using Streamlit's st.code component.
