from itertools import combinations

class dfa:
    def __init__(self) -> None:
        self.states = set()
        self.alphabet = set()
        self.transitions = {}
        self.start = None
        self.finals = set()
    
    @property
    def blank(self):
        return "__"
    
    @classmethod
    def fromfile(cls, filename):
        fa = cls()
        with open(filename) as f:
            lines = f.readlines()
            fa.start = lines.pop(0).strip()
            fa.finals = set(lines.pop(0).strip().split(","))
            for line in lines:
                state, symbol, next_state = line.strip().split(",")
                fa.transitions[(state,symbol)] = next_state
                fa.states.add(state)
                fa.states.add(next_state)
                fa.alphabet.add(symbol)

        return fa
    
    @classmethod
    def fromlist(cls, list):
        fa = cls()
        fa.start = list.pop(0)
        fa.finals = set(list.pop(0).split(","))
        for line in list:
            state, symbol, next_state = line.strip().split(",")
            fa.transitions[(state,symbol)] = next_state
            fa.states.add(state)
            fa.states.add(next_state)
            fa.alphabet.add(symbol)
            

    def __str__(self):
        return f"states: {self.states}\n" + \
               f"alphabet: {self.alphabet}\n" + \
               f"transitions: {self.print_transition_dfa()}\n" + \
               f"start: {self.start}\n" + \
               f"finals: {self.finals}\n"

    def print_transition_dfa(self):
        return "\n".join(f"{key[0]} --{key[1]}--> {value}" for key, value in self.transitions.items())
                                                          
    def run(self, input) -> None:
        print(f"Running input: {input}")
        current_state = self.start
        for symbol in input:
            current_state = tuple(sorted(current_state))
            print(f"{current_state} --{symbol}--> {self.transitions.get((current_state, symbol), self.blank)}")
            current_state = self.transitions.get((current_state, symbol), self.blank)
        for s in self.finals:
            accept = False
            x = set(s)
            y = set(current_state)
            if x == y:
                accept = True
                break
        if accept:
            print("Accept")
        else:
            print("Reject")
                

class ndfa:
    def __init__(self) -> None:
        self.states = set()
        self.alphabet = set()
        self.transitions = []
        self.start = set()
        self.finals = set()
    
    @property
    def blank(self):
        return "__"
    
    @classmethod
    def fromfile(cls, filename):
        fa = cls()
        with open(filename) as f:
            lines = f.readlines()
            fa.start = set(lines.pop(0).strip().split(","))
            fa.finals = set(lines.pop(0).strip().split(","))
            for line in lines:
                state, symbol, next_state = line.strip().split(",")
                fa.transitions.append((state, symbol, next_state))
                fa.states.add(state)
                fa.states.add(next_state)
                fa.alphabet.add(symbol)

        return fa
    
    @classmethod
    def fromlist(cls, list):
        fa = cls()
        fa.start = list.pop(0)
        fa.finals = set(list.pop(0).split(","))
        for line in list:
            state, symbol, next_state = line.strip().split(",")
            fa.transitions.append((state, symbol, next_state))
            fa.states.add(state)
            fa.states.add(next_state)
            fa.alphabet.add(symbol)

    def state_subset(self) -> set:
        s = list(self.states)
        all_subsets = set()
        states = [set(combinations(s, r)) for r in range(len(s)+1)]
        for state in states:
            for i in state:
                if len(i) == 1:
                    x = set()
                    x.add(i[0])
                    x = tuple(x)
                    all_subsets.add(x)
                else:
                    i = sorted(i)
                    i = tuple(i)
                    all_subsets.add(i)
        return all_subsets
                


    def __str__(self):
        return f"states: {self.states}\n" + \
               f"alphabet: {self.alphabet}\n" + \
               f"transitions: {self.print_transition()}\n" + \
               f"start: {self.start}\n" + \
               f"finals: {self.finals}\n"

    def print_transition(self):
        transitions = ""
        for transition in self.transitions:
            transitions += (f"{transition[0]} --{transition[1]}--> {transition[2]}")
        return transitions
    
    def run(self, input) -> None:
        print(f"Running input: {input}")
        current_states = [s for s in self.start]
        for symbol in input:
            next_states = set()
            for state in current_states:
                for transition in self.transitions:
                    if (transition[0] == state and transition[1] == symbol) or (transition[0]==state and transition[1] == " "):
                        next_states.add(transition[2])
                        print(f"{state} --{symbol}--> {transition[2]}")
            current_states = next_states

        if any (state in self.finals for state in current_states):
            print("Accept")
        else:
            print("Reject")

    def determinize(self) -> dfa:
        d = dfa()
        d.states = self.state_subset()
        d.alphabet = set([symbol for symbol in self.alphabet if symbol != " "])
        # Atribui o estado inicial do dfa como o conjunto de estados iniciais do ndfa
        st = set()  # Usa set() para garantir que não haja elementos repetidos
        if len(self.start) == 1:
            st.add(next(iter(self.start)))  # Pega o único estado inicial
        else:
            for state in d.states:
                if set(self.start) == set(state):
                    for s in state:
                        st.add(s)  # Adiciona ao conjunto sem duplicatas
                break

        for transition in self.transitions:
            if transition[0] in self.start and transition[1] == " ":
                st.add(transition[2])  # Adiciona o próximo estado ao conjunto

        # Agora converte o conjunto em tupla, para ser usado como chave ou estado inicial
        d.start = tuple(sorted(tuple(st)))
        
        # Atribui os estados finais do dfa como os conjuntos que 
        # contém pelo menos um estado final do ndfa
        for state in d.states:
            if (any (s in self.finals for s in state)):
                d.finals.add(state)
        #transições dfa
        for state in d.states:
            for symbol in d.alphabet:
                next_state = set()
                for s in state if isinstance(state, tuple) else (state,):
                    for transition in self.transitions:
                        if transition[0] == s and transition[1] == symbol:
                            next_state.add(transition[2])
                if next_state:
                    if len(next_state) > 1:
                        next_state = tuple(next_state)
                    else:
                        ns = next_state.pop()
                        next_state = (ns,)
                    d.transitions[(state, symbol)] = next_state
                    print(f"{state} --{symbol}--> {next_state}")
                else:
                    d.transitions[(state, symbol)] = self.blank
                    print(f"{state} --{symbol}--> {self.blank}")
        
            
        return d

if __name__ == "__main__":
    fa = ndfa.fromfile("nfd.auto")
    print(fa.state_subset())
    d = fa.determinize()
    input = "baa"
    d.run(input)
    
    
