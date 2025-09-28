#
# SRI RAMACHANDRA FACULTY OF ENGINEERING AND TECHNOLOGY
# CSE23CT302- THEORY OF COMPUTATION AND COMPILER DESIGN
# Special Assignment for Fast Learners
# Name: VARSHA VENKATESAN
# Unique ID: E0223018
# Department: CSE (Cyber Security and IoT)
#
# Program to convert a Regular Expression to a DFA and validate strings.
#

import sys

# Increase recursion limit for complex regular expressions
sys.setrecursionlimit(2000)

class NFAState:
    """A state in the Nondeterministic Finite Automaton (NFA)."""
    def __init__(self, is_final=False):
        self.is_final = is_final
        # Transitions: {'symbol': {set of next_states}}
        # 'ε' is used for epsilon transitions
        self.transitions = {}

class NFA:
    """Represents an NFA."""
    def __init__(self, start_state, final_state):
        self.start_state = start_state
        self.final_state = final_state
        self.states = set()
        self._collect_states(start_state)

    def _collect_states(self, state):
        """Recursively find all reachable states to populate the states set."""
        if state in self.states:
            return
        self.states.add(state)
        for symbol in state.transitions:
            for next_state in state.transitions[symbol]:
                self._collect_states(next_state)


def re_to_postfix(regex):
    """Converts an infix regular expression to postfix using Shunting-yard algorithm."""
    # Add explicit concatenation operators '.'
    regex_concat = ""
    for i in range(len(regex)):
        regex_concat += regex[i]
        if i + 1 < len(regex):
            char1 = regex[i]
            char2 = regex[i+1]
            if char1 not in '(|' and char2 not in ')|*':
                regex_concat += '.'

    postfix = ""
    stack = []
    precedence = {'|': 1, '.': 2, '*': 3}

    for char in regex_concat:
        if char.isalnum() or char == 'ε':
            postfix += char
        elif char == '(':
            stack.append(char)
        elif char == ')':
            while stack and stack[-1] != '(':
                postfix += stack.pop()
            stack.pop() # Pop '('
        else: # Operator
            while (stack and stack[-1] != '(' and
                   precedence.get(stack[-1], 0) >= precedence.get(char, 0)):
                postfix += stack.pop()
            stack.append(char)

    while stack:
        postfix += stack.pop()

    return postfix

def postfix_to_nfa(postfix):
    """
    Converts a postfix regular expression to an NFA using Thompson's Construction.
    """
    if not postfix:
        return None

    nfa_stack = []

    for char in postfix:
        if char.isalnum():
            # Create a simple NFA for a literal character
            final_state = NFAState(is_final=True)
            start_state = NFAState()
            start_state.transitions[char] = {final_state}
            nfa_stack.append(NFA(start_state, final_state))
        elif char == '*':
            # Kleene Star operation
            nfa = nfa_stack.pop()
            new_start = NFAState()
            new_final = NFAState(is_final=True)
            new_start.transitions['ε'] = {nfa.start_state, new_final}
            nfa.final_state.is_final = False
            nfa.final_state.transitions['ε'] = {nfa.start_state, new_final}
            nfa_stack.append(NFA(new_start, new_final))
        elif char == '.':
            # Concatenation operation
            nfa2 = nfa_stack.pop()
            nfa1 = nfa_stack.pop()
            nfa1.final_state.is_final = False
            nfa1.final_state.transitions['ε'] = {nfa2.start_state}
            nfa_stack.append(NFA(nfa1.start_state, nfa2.final_state))
        elif char == '|':
            # Union operation
            nfa2 = nfa_stack.pop()
            nfa1 = nfa_stack.pop()
            new_start = NFAState()
            new_start.transitions['ε'] = {nfa1.start_state, nfa2.start_state}
            new_final = NFAState(is_final=True)
            nfa1.final_state.is_final = False
            nfa2.final_state.is_final = False
            nfa1.final_state.transitions['ε'] = {new_final}
            nfa2.final_state.transitions['ε'] = {new_final}
            nfa_stack.append(NFA(new_start, new_final))

    return nfa_stack[0]


def nfa_to_dfa(nfa, alphabet):
    """
    Converts an NFA to a DFA using the Subset Construction algorithm.
    """
    def epsilon_closure(states):
        """Computes the epsilon closure for a set of NFA states."""
        closure = set(states)
        stack = list(states)
        while stack:
            state = stack.pop()
            for next_state in state.transitions.get('ε', set()):
                if next_state not in closure:
                    closure.add(next_state)
                    stack.append(next_state)
        return frozenset(closure)

    def move(states, symbol):
        """Computes the set of states reachable on a given symbol."""
        reachable = set()
        for state in states:
            reachable.update(state.transitions.get(symbol, set()))
        return frozenset(reachable)

    dfa_states = {} # {frozenset(nfa_states): dfa_state_id}
    dfa_transitions = {} # {dfa_state_id: {symbol: dfa_state_id}}
    dfa_final_states = set()

    # Initial state of DFA is the epsilon closure of NFA's start state
    start_closure = epsilon_closure({nfa.start_state})
    unprocessed_states = [start_closure]
    dfa_states[start_closure] = 0
    dfa_transitions[0] = {}
    
    if nfa.final_state in start_closure:
        dfa_final_states.add(0)

    state_id_counter = 1
    
    while unprocessed_states:
        current_nfa_states_set = unprocessed_states.pop(0)
        current_dfa_state_id = dfa_states[current_nfa_states_set]

        for symbol in alphabet:
            next_nfa_states = move(current_nfa_states_set, symbol)
            next_closure = epsilon_closure(next_nfa_states)

            if not next_closure:
                continue

            if next_closure not in dfa_states:
                dfa_states[next_closure] = state_id_counter
                dfa_transitions[state_id_counter] = {}
                unprocessed_states.append(next_closure)
                
                # Check if this new DFA state is a final state
                if any(s.is_final for s in next_closure):
                    dfa_final_states.add(state_id_counter)
                
                state_id_counter += 1
            
            dfa_transitions[current_dfa_state_id][symbol] = dfa_states[next_closure]

    return {
        "transitions": dfa_transitions,
        "start_state": 0,
        "final_states": dfa_final_states
    }

def print_dfa_table(dfa, alphabet):
    """Prints the DFA transition table in a readable format."""
    print("\n--- DFA Transition Table ---")
    
    # Header
    header = f"{'State':<12}"
    for symbol in sorted(list(alphabet)):
        header += f"|   {symbol}   "
    print(header)
    print("-" * len(header))

    # Rows
    for state, transitions in sorted(dfa['transitions'].items()):
        # Mark start and final states
        state_marker = ""
        if state == dfa['start_state']:
            state_marker += "-> "
        if state in dfa['final_states']:
            state_marker += "*"
        
        row = f"{state_marker:<2} q{state:<8}"
        for symbol in sorted(list(alphabet)):
            next_state = transitions.get(symbol, '—')
            row += f"|   q{next_state if next_state != '—' else '—'}   "
        print(row)
    print("\n(-> indicates start state, * indicates final state)\n")


def simulate_dfa(dfa, input_string, alphabet):
    """Simulates the DFA on an input string to check for acceptance."""
    for char in input_string:
        if char not in alphabet:
            return False # Character not in alphabet

    current_state = dfa['start_state']
    for char in input_string:
        current_state = dfa['transitions'][current_state].get(char)
        if current_state is None:
            # No transition for this character, reject
            return False
            
    return current_state in dfa['final_states']

# --- Main Program Logic ---

def solve_question_1():
    print("--- Solving Question 1 ---")
    regex = "(a|b)*abb" # Using '|' for union as is standard
    alphabet = {'a', 'b'}
    print(f"Input Regular Expression: {regex}")

    # 1. Convert RE to Postfix
    postfix_re = re_to_postfix(regex)
    
    # 2. Convert Postfix to NFA
    nfa = postfix_to_nfa(postfix_re)
    
    # 3. Convert NFA to DFA
    dfa = nfa_to_dfa(nfa, alphabet)
    
    # 4. Print the output transition table
    print_dfa_table(dfa, alphabet)

def solve_question_2():
    print("--- Solving Question 2 ---")
    regex = "(0|1)*01"
    alphabet = {'0', '1'}
    strings_to_test = ["1101", "111", "0001"]
    print(f"Input Regular Expression: {regex}")
    print(f"Strings to test: {', '.join(strings_to_test)}")
    
    # 1. Convert RE to Postfix
    postfix_re = re_to_postfix(regex)
    
    # 2. Convert Postfix to NFA
    nfa = postfix_to_nfa(postfix_re)
    
    # 3. Convert NFA to DFA
    dfa = nfa_to_dfa(nfa, alphabet)
    
    # Optional: Print the DFA table for verification
    print_dfa_table(dfa, alphabet)
    
    # 4. Validate strings
    print("--- Validation Results ---")
    for s in strings_to_test:
        is_accepted = simulate_dfa(dfa, s, alphabet)
        result = "Accepted" if is_accepted else "Rejected"
        print(f"String '{s}': {result}")
    print("\n")


if __name__ == "__main__":
    # [cite_start]Question 1 from the assignment [cite: 7, 8, 9]
    # Input: (a/b)*abb, Output: DFA transition table.
    # Note: '/' is commonly represented as '|' for union in RE notation.
    solve_question_1()
    
    print("="*50)

    # [cite_start]Question 2 from the assignment [cite: 10, 11, 12, 13]
    # Input: RE=(0|1)*01, Strings: 1101, 111, 0001, Output: Accepted/Rejected
    solve_question_2()