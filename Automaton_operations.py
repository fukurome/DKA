import tkinter as tk
from tkinter import ttk

class FiniteAutomaton:
    def __init__(self, states, alphabet, transitions, initial_state, final_states):
        self.states = states
        self.alphabet = alphabet
        self.transitions = transitions
        self.initial_state = initial_state
        self.final_states = final_states

def unification(automaton1, automaton2):
    # Реализация остается прежней
    new_states = {(state1, state2) for state1 in automaton1.states for state2 in automaton2.states}
    new_transitions = {}

    for symbol in automaton1.alphabet:
        for state1 in automaton1.states:
            for state2 in automaton2.states:
                new_transitions[((state1, state2), symbol)] = (
                    automaton1.transitions.get((state1, symbol), None),
                    automaton2.transitions.get((state2, symbol), None)
                )

    new_initial_state = (automaton1.initial_state, automaton2.initial_state)
    new_final_states1 = {(state1, state2) for state1 in automaton1.final_states for state2 in automaton2.states}
    new_final_states2 = {(state1, state2) for state2 in automaton2.final_states for state1 in automaton1.states}
    new_final_states = new_final_states1 | new_final_states2

    unification_automaton = FiniteAutomaton(new_states, automaton1.alphabet, new_transitions, new_initial_state,
                                            new_final_states)
    return unification_automaton

def intersection(automaton1, automaton2):
    # Реализация остается прежней
    new_states = {(state1, state2) for state1 in automaton1.states for state2 in automaton2.states}
    new_transitions = {}

    for symbol in automaton1.alphabet:
        for state1 in automaton1.states:
            for state2 in automaton2.states:
                new_transitions[((state1, state2), symbol)] = (
                    automaton1.transitions.get((state1, symbol), None),
                    automaton2.transitions.get((state2, symbol), None)
                )

    new_initial_state = (automaton1.initial_state, automaton2.initial_state)
    new_final_states = {(state1, state2) for state1 in automaton1.final_states for state2 in automaton2.final_states}

    intersection_automaton = FiniteAutomaton(new_states, automaton1.alphabet, new_transitions, new_initial_state,
                                             new_final_states)

    return intersection_automaton

def parse_input_automat(input_string):
    # Реализация остается прежней
    parsed_data = {}

    # Разбиваем входную строку по запятой, предполагая, что каждая пара имеет формат "1.a=2"
    pairs = input_string.split(', ')

    for pair in pairs:
        # Разбиваем пару на составляющие (1.a=2 => ['1.a', '2'])
        components = pair.split('=')
        if len(components) == 2:
            key, value = components
            # Разбиваем ключ на составляющие (1.a => ['1', 'a'])
            key_components = key.split('.')
            if len(key_components) == 2:
                parsed_data[(key_components[0], key_components[1])] = value

    return parsed_data

def out_format(transitions):
    out = ''
    for k, v in transitions.items():
        out += '(' + k[0][0] + ', ' + k[0][1] + ').' + str(k[1]) + ' = (' + v[0] + ', ' + v[1] + '), '
    out = out[0:-2]
    return out


def parse_input_final(input_string):
    final_states_set = set()
    final_states_list = []
    states = input_string.split(', ')

    for state in states:
        if state not in final_states_set:
            final_states_list.append((state,))
            final_states_set.add(state)

    return final_states_list



def extract_information(parsed_data):
    states_set = set()
    alphabet_set = set()
    states_list = []
    alphabet_list = []

    for key in parsed_data:
        # Добавляем первый элемент ключа в множество states
        if key[0] not in states_set:
            states_list.append(key[0])
            states_set.add(key[0])
        # Добавляем второй элемент ключа в множество alphabet
        if key[1] not in alphabet_set:
            alphabet_list.append(key[1])
            alphabet_set.add(key[1])

    return states_list, alphabet_list

def print_initial_state(initial_state):
    return ('(' + initial_state[0] + ', ' + initial_state[1] + ')')


def flatten_tuple(t):
    if isinstance(t, tuple) and len(t) == 1:
        return flatten_tuple(t[0])
    return t

def print_final_states(final_states):
    checklist = set()
    out = ''
    for state_tuple in final_states:
        flattened_tuple = tuple(flatten_tuple(state) for state in state_tuple)
        if flattened_tuple not in checklist:
            out += f'{flattened_tuple}, '
            checklist.add(flattened_tuple)

    out = out[0:-2]

    return out



class AutomatonApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Automaton Operations")

        # Автомат 1 Поля ввода
        #ttk.Label(self.root, text="Автомат 1", font=('Helvetica', 14, 'bold')).pack(pady=(10, 5))

        self.automaton1_input = self.create_input_field("Автомат 1:", width=50)
        self.initial_state1_input = self.create_input_field("Начальное состояние для автомата 1:")
        self.final_states1_input = self.create_input_field("Заключительные значения Автомата 1:")

        # Автомат 2 Поля ввода
        #ttk.Label(self.root, text="Автомат 2", font=('Helvetica', 14, 'bold')).pack(pady=(10, 5))

        self.automaton2_input = self.create_input_field("Автомат 2:", width=50)
        self.initial_state2_input = self.create_input_field("Начальное состояние для автомата 2:")
        self.final_states2_input = self.create_input_field("Заключительные значения Автомата 2:")

        # Кнопки
        self.union_button = ttk.Button(self.root, text="Объединение", command=self.perform_union)
        self.union_button.pack(side="left", padx=5)

        self.intersection_button = ttk.Button(self.root, text="Пересечение", command=self.perform_intersection)
        self.intersection_button.pack(side="left", padx=5)

        # Поле вывода
        ttk.Label(self.root, text="Результат").pack()
        self.text_output = tk.Text(self.root, wrap="word", height=6, width=100, state="disabled")
        self.text_output.pack(padx=10, pady=10)

        ttk.Label(self.root, text="Начальное значение:").pack()
        self.initial_states_output = tk.Text(self.root, wrap="word", height=1, width=20, state="disabled")
        self.initial_states_output.pack(padx=10, pady=10)

        ttk.Label(self.root, text="Заключительные значения:").pack()
        self.final_states_output = tk.Text(self.root, wrap="word", height=1, width=70, state="disabled")
        self.final_states_output.pack(padx=10, pady=10)

    def create_input_field(self, label_text, width=20):
        ttk.Label(self.root, text=label_text).pack()
        input_field = ttk.Entry(self.root, width=width)
        input_field.pack()

        input_field.bind("<Control-v>", self.handle_paste)
        return input_field

    def handle_paste(self, event):
        def handle_paste(self, event):
            ctrl_pressed = (event.state & 0x4) != 0

            text = self.root.clipboard_get()

            event.widget.insert("insert", text)


    def get_input(self, input_field):
        return input_field.get()

    def perform_union(self):
        self.clear_output_field()

        automaton1 = self.initialization(self.automaton1_input, self.initial_state1_input, self.final_states1_input)
        automaton2 = self.initialization(self.automaton2_input, self.initial_state2_input, self.final_states2_input)
        result_automaton = unification(automaton1, automaton2)
        self.display_result(result_automaton)

    def perform_intersection(self):
        self.clear_output_field()

        automaton1 = self.initialization(self.automaton1_input, self.initial_state1_input, self.final_states1_input)
        automaton2 = self.initialization(self.automaton2_input, self.initial_state2_input, self.final_states2_input)
        result_automaton = intersection(automaton1, automaton2)
        self.display_result(result_automaton)


    def clear_output_field(self):
        self.text_output.config(state="normal")
        self.text_output.delete("1.0", "end")
        self.text_output.config(state="disabled")

        self.initial_states_output.config(state="normal")
        self.initial_states_output.delete("1.0", "end")
        self.initial_states_output.config(state="disabled")

        self.final_states_output.config(state="normal")
        self.final_states_output.delete("1.0", "end")
        self.final_states_output.config(state="disabled")

    def initialization(self, automaton_input, initial_state_input, final_states_input):
        input_data = automaton_input.get()
        parsed_data = parse_input_automat(input_data)
        transitions = parsed_data
        states, alphabet = extract_information(parsed_data)

        initial_state = self.get_input(initial_state_input)
        final_states = self.get_input(final_states_input)
        final_states = parse_input_final(final_states)

        final_states = {(state,) for state in final_states}

        automaton = FiniteAutomaton(states, alphabet, transitions, initial_state, final_states)

        return automaton

    def display_result(self, automaton):
        self.text_output.config(state="normal")
        self.text_output.delete("1.0", "end")
        self.text_output.insert("1.0", out_format(automaton.transitions))
        self.text_output.config(state="disabled")

        self.initial_states_output.config(state="normal")
        self.initial_states_output.delete("1.0", "end")
        self.initial_states_output.insert("1.0", print_initial_state(automaton.initial_state))
        self.initial_states_output.config(state="disabled")

        self.final_states_output.config(state="normal")
        self.final_states_output.delete("1.0", "end")
        final_states_text = print_final_states(automaton.final_states)
        self.final_states_output.insert("1.0", final_states_text)
        self.final_states_output.config(state="disabled")


if __name__ == "__main__":
    root = tk.Tk()
    app = AutomatonApp(root)
    root.mainloop()

# примеры автоматов: 1) ввод 01.a=10, 01.b=11, 11.a=01, 11.b=11
#                       начальное значение 01
#                       заключительные значения 11
#                    2) ввод 12.a=12, 12.b=02, 02.a=12, 02.b=22, 22.a=22, 22.b=02
#                       начальное значение 12
#                       заключительные значения 02