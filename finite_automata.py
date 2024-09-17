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
               f"transitions: {self.transitions}\n" + \
               f"start: {self.start}\n" + \
               f"finals: {self.finals}\n"


    def run(self, input) -> None:
        print(f"Running input: {input}")
        current_state = self.start
        for symbol in input:
            print(f"{current_state} --{symbol}--> {self.transitions.get((current_state, symbol), self.blank)}")
            current_state = self.transitions.get((current_state, symbol), self.blank)
        if current_state in self.finals:
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
                    all_subsets.add(i[0])
                else:
                    all_subsets.add(i)
        return all_subsets
                


    def __str__(self):
        return f"states: {self.states}\n" + \
               f"alphabet: {self.alphabet}\n" + \
               f"transitions: {self.transitions}\n" + \
               f"start: {self.start}\n" + \
               f"finals: {self.finals}\n"

    
    def run(self, input) -> None:
        print(f"Running input: {input}")
        current_states =[s for s in self.start.split(",")]
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
        d.alphabet = self.alphabet
        # Atribui o estado inicial do dfa como o conjunto de estados iniciais do ndfa
        if len(self.start) == 1:
            d.start = self.start
        else:
            for state in d.states:
                if set(self.start) == set(state):
                    d.start = state
                    break
        # Atribui os estados finais do dfa como os conjuntos que 
        # contém pelo menos um estado final do ndfa
        for state in d.states:
            if any (s in self.finals for s in state):
                d.finals.add(state)
        pass
        

if __name__ == "__main__":
    fa = ndfa.fromfile("nfd.auto")
    print(fa.state_subset())
    fa.determinize()
    input = "010000100"
    
    