### LR(0) Parsing Table Generation ###

from tabulate import tabulate

## Grammar goes here ##
# How should we write our LR(0) grammar?:
# Below is a BNF grammar, followed by the representation for this parser:
#
# A ::= 'a' <A> | 'b'
# 'A' : (('a', 'A'), ('b',))

GRAMMAR = {
    'S' : (('A', 'A'),),
    'A' : (('a', 'A'), ('b',))
    }

class LR0_Parser:

    def __init__(self) -> None:
        self.grammar      = {}   # Our grammar
        self.states       = []   # We'll store all the grammar states here
        self.item_prods   = []   # Store the productions for get_closure here

        self.rules        = []   # Numbered rules to refer to when reducing
        self.goto_table   = []   # A representation of the parse table

        self.parse_table  = [['',],]

        self.debug_counter = 0

    ## Prettyprint the state's info ##
    def print_state(self, state, n=None):

        if n == None:
            n = len(self.states)

        print(f"State I{n}:")

        for item in state:
            lhs = item[0]

            rhs = []
            for prod in item[1]:
                prodf = list(prod)
                prodf.insert(item[2], '•')
                rhs.append(''.join(prodf))
                
            rhsf = '/'.join(rhs)
            
            print("    " + f"{lhs} -> {rhsf}")
            
        print()

    ## Fetch all the productions of a nonterminal recursively ##
    def get_closure(self, lhs: str) -> list:
        # Is this item a terminal or nonterminal?
        # If it's a nonterminal, it will have a right-hand side:
        rhs = self.grammar.get(lhs)

        # If it's a nonterminal:
        if rhs != None:
            # Add this to all the productions of our starting item:
            self.item_prods.append((lhs, rhs, 0))

            # Check to see if the first item in this nonterminal's
            # production(s) is a terminal or nonterminal:
            for item in rhs:
                self.get_closure(item[0])

        # We're done;
        # Return all the productions of the item we started with:
        return self.item_prods

    ## For a closure, find all gotos ##
    def get_gotos(self, state: list) -> None:
        for item in state:
            # Get the info of the item
            lhs = item[0]
            rhs = item[1]
            dot = item[2] + 1

            for r in rhs:
                # Create a possible state that could be goto-ed:
                new_state = [(lhs, (r,), dot)]

                # If the dot isn't at the end of the production:
                if dot < len(r):
                    # Get the closure of the new state and add it:
                    self.item_prods.clear()
                    closure = self.get_closure(r[dot])
                    new_state.extend(closure)

                    # If the new state hasn't been seen before:
                    if new_state not in self.states:
                        # Add it to the list of states we've seen:                    
                        self.states.append(new_state)
                        
                        # Continue the loop and get the gotos of all items
                        # in the closure:
                        self.get_gotos(new_state)

                    # Add this action to our parsing table:
                    goto = self.states.index(new_state)

                    # If we're moving on a terminal, prepend 's':
                    if self.grammar.get(r[dot-1]) == None:
                        goto = f"s{goto}"
                        
                    self.goto_table.append(
                        (self.states.index(state), r[dot-1], goto)
                        )
                        
                else:
                    # If the new state hasn't been seen before:
                    if new_state not in self.states:
                        # Add it to the list of states we've seen:
                        self.states.append(new_state)

                        # If this is the end of the first rule,
                        # we'll accept instead of shift to another state:
                        if rhs[0] in self.rules:
                            reduce = f"r{self.rules.index(r) + 1}"
                            to = "all"
                        else:
                            reduce = "accept"
                            to = '$'
                            
                        self.goto_table.append(
                            (self.states.index(new_state), to, reduce)
                            )

                    # Add this action to our parsing table:
                    goto = self.states.index(new_state)
                    
                    # If we're moving on a terminal, prepend 's':
                    if self.grammar.get(r[dot-1]) == None:
                        goto = f"s{goto}"
                        
                    self.goto_table.append(
                        (self.states.index(state), r[dot-1], goto)
                        )
                        
                    continue


    ## Create an automaton for our grammar ##
    def build_dfa(self, grammar: dict) -> None:
        # Set parser grammar:
        self.grammar = grammar

        # Set list of rules using grammar:
        for prod in grammar:
            for rhs in grammar[prod]:
                self.rules.append(rhs)

        # Augment the first production:
        augmented = {"S'" : (('S',),)}
        self.grammar.update(augmented)

        # Set the first item of state I0:
        lhs = list(augmented.keys())[0]
        rhs = self.grammar.get(lhs)
        state = [(lhs, rhs, 0)]

        # Get the closure of state I0:
        self.item_prods.clear()
        closure = self.get_closure(list(augmented.keys())[0])[1:]

        # Add the closure items to state I0:
        state.extend(closure)
            
        self.states.append(state)

        # Get gotos of state I0 and their states:
        self.get_gotos(state)

        # Print each of the states:
        for s in range(len(self.states)):
            self.print_state(self.states[s], n=s)

    def build_table(self) -> None:

        # TODO: Make a separate goto and action table
        nonterminals = []
        for goto in self.goto_table:
            if self.grammar.get(goto[1]) == None and goto[1] != "all" and \
               goto[1] not in self.parse_table[0]:
                self.parse_table[0].append(goto[1])
                nonterminals.append(self.parse_table[0].index(goto[1]))
        
        for goto in self.goto_table:
            row = 0
            col = []

            while goto[0] + 2 > len(self.parse_table):
                self.parse_table.append([len(self.parse_table) - 1])

            while goto[1] not in self.parse_table[0] and goto[1] != "all":
                self.parse_table[0].append(goto[1])

            if goto[1] == "all":
                col = nonterminals
            else:
                col.append(self.parse_table[0].index(goto[1]))
                
            row = self.parse_table[goto[0] + 1]

            while len(self.parse_table[0]) > len(row):
                row.append('')

            for nterm in col:
                row[nterm] = goto[2]

        print()
        print("Parsing Table:")
        print(
            tabulate(
                self.parse_table[1:],
                headers=self.parse_table[0],
                tablefmt="grid"
                )
            )


parser = LR0_Parser()
parser.build_dfa(GRAMMAR)
parser.build_table()
