# Arturo Gutierrez Larios
# CptS 516 @ WSU Tri-Cities
# May 5, 2023

# Class to store an equation's coefficients and constant
class Equation:
    def __init__(self, C1, C2, C3, C):
        self.C1 = C1
        self.C2 = C2
        self.C3 = C3
        self.C = C

# Returns Cmax from C1x1 + C2x2 + C3x3 + C = 0 where constants C1, C2, C4 are 
# integers (positive, negative, zero), and constant C is nonnegative
def Cmax(equation):
    Cmax = 0;

    # for (d1, d2, d3, d4) in [0, 1]
    for d1 in range(2):
        for d2 in range(2):
            for d3 in range(2):
                for d4 in range(2):
                    result = abs(equation.C1*d1 + equation.C2*d2 + equation.C3*d3 + d4)
                    if result > Cmax:
                        Cmax = result

    # return Cmax =            max             |C1d1 + C2d2 + C3d3 + d|
    #                d1, d2, d3, d4 in [0, 1]
    return Cmax

# Returns the value K from a given constant C >= 0
# K is defined as the number of bits needed to represent C
def K(C):
    K = 0

    if C == 0:
        K = 1;
    else:
        while C != 0:
            C //= 2
            K += 1

    return K

# Returns the value b from a given constant C >= 0 and i
# b is the bit at index i of the binary representation of C
# i shall be in the range of 1 <= i <= K + 1
def b(C, i):
    while (i > 1):
        C //= 2
        i -= 1
    
    return C % 2

# Construct a finite automaton M from the description of the equation
class M:
    # Construct M from equation it is initialized with
    def __init__(self, equation):
        # If an equation is given, use it to create M
        if equation:
            # Compute Cmax and K using the previously defined functions
            self.Cmax = Cmax(equation)
            self.K = K(equation.C)

            # Save initial and accepting states
            self.initialState = (0, 1)
            self.acceptingState = (0, self.K + 1)

            # Initialize empty dictionary to store transitions of states
            self.transitions = {}

            # -Cmax <= carry <= Cmax
            for carry in range(-self.Cmax, self.Cmax + 1):
                # 1 <= i <= K + 1
                for i in range(1, self.K + 2):
                    # For all states [carry, i]
                    state = (carry, i)
                    # Initialize empty dictionary for 'state' in transitions dictionary
                    self.transitions[state] = {}
                    # For all input symbols (a1, a2, a3)
                    for a1 in [0, 1]:
                        for a2 in [0, 1]:
                            for a3 in [0, 1]:
                                # R = C1a1 + C2a2 + C3a3 + bi + carry
                                R = equation.C1 * a1 + equation.C2 * a2 + equation.C3 * a3 + b(equation.C, i) + carry
                                # If R is divisible by 2
                                if R % 2 == 0:
                                    # carry' = R / 2
                                    carry0 = R // 2
                                    # if 1 <= i <= K
                                    if 1 <= i <= self.K:
                                        # then i' = i + 1
                                        i0 = i + 1
                                    else:
                                        # then i' = i
                                        i0 = i
                                    # Create a transition from state to state' on input (a1, a2, a3)
                                    self.transitions[state][(a1, a2, a3)] = (carry0, i0)
    
    # Returns the result of a transition from state on an input symbol
    def transition(self, state, inputSymbol):
        if inputSymbol not in self.transitions[state]:
            return None
        return self.transitions[state][inputSymbol]

# Construct a finite automaton from the cartesian product of M1 and M2, which are instances of finite automaton M
class MxM:
    # Construct MX from M1 and M2
    def __init__(self, M1, M2):
        # Initialize empty dictionary to store transitions of states
        self.transitions = {}

        # For all states in M1 and M2
        for state1 in M1.transitions:
            for state2 in M2.transitions:
                # Create a combined state
                newState = (state1, state2)
                # Initialize empty dictionary for 'new_state' in transitions dictionary
                self.transitions[newState] = {}

                # For all input symbols (a1, a2, a3)
                for a1 in [0, 1]:
                    for a2 in [0, 1]:
                        for a3 in [0, 1]:
                            # Get the transition for each FA on the current input symbol
                            transition1 = M1.transition(state1, (a1, a2, a3))
                            transition2 = M2.transition(state2, (a1, a2, a3))

                            # If both FAs have a transition on the current input symbol
                            if transition1 and transition2:
                                # Add the transition for the combined state
                                self.transitions[newState][(a1, a2, a3)] = (transition1, transition2)

        # Set the initial and accepting states for the new FA
        self.initialState = (M1.initialState, M2.initialState)
        self.acceptingState = (M1.acceptingState, M2.acceptingState)

# Find a path from the initial state to the accepting state given a FA m using a DFS
def findPath(m):
    # List of states that have already been searched to avoid going in loops
    states = []
    # Helper function performs the depth-first search
    def dfs(state, path):
        states.append(state)
        # If the current state is the final state, return the path
        if state == m.acceptingState:
            return path
        # Otherwise, iterate over all possible input symbols
        for a1 in [0, 1]:
            for a2 in [0, 1]:
                for a3 in [0, 1]:
                    # Get the next state for the current input symbol
                    inputSymbol = (a1, a2, a3)
                    if state in m.transitions and inputSymbol in m.transitions[state]:
                        nextState = m.transitions[state][inputSymbol]
                    else:
                        nextState = None
                    # If there is a transition on the current input symbol, recursively search for a path from the next state
                    if nextState is not None and nextState not in states:
                        result = dfs(nextState, path + [inputSymbol])
                        # If a path was found, return it
                        if result is not None:
                            return result
        # If no path was found from the current state, return None
        return None
    
    # Start the search from the initial state
    return dfs(m.initialState, [])

# Calculate the solutions x1, x2, and x3 from a given path
def solutionFromPath(path):
    # Create empty strings to store the binary values
    x1str = ""
    x2str = ""
    x3str = ""

    # Iterate over the list of tuples and store the binary values in the corresponding x
    for tup in path:
        x1str += str(tup[0])
        x2str += str(tup[1])
        x3str += str(tup[2])

    # Reverse the strings
    x1str = x1str[::-1]
    x2str = x2str[::-1]
    x3str = x3str[::-1]

    # Convert the reversed strings to decimal
    x1 = int(x1str, 2)
    x2 = int(x2str, 2)
    x3 = int(x3str, 2)

    # Return the decimal values as a tuple
    return (x1, x2, x3)

# Program starts here
def main():
    # Print an explanation of the program for the user
    print("\nThis program solves a system of two equations in three variables. "
          "Therefore the system of equations is given as:\n\n"
          "   Equation 1: C11x1 + C12x2 + C13x3 + C1 = 0\n"
          "   Equation 2: C21x1 + C22x2 + C23x3 + C2 = 0\n"
          "\nWhere all the xj's are nonnegative integer variables (called unknowns) "
          "and the following are all the parameters:\n\n"
          "   - all the coefficients Cij's, which are integers (positive, negative, zero), and\n"
          "   - all the numbers Ci's, which are nonnegative integers\n")

    # Get Equation 1 from user
    print("Enter the parameters for Equation 1 in order (C11, C12, C13, C1): ", end="")
    eq1 = Equation(*map(int, input().split()))

    # Get Equation 2 from user
    print("Enter the parameters for Equation 2 in order (C21, C22, C23, C2): ", end="")
    eq2 = Equation(*map(int, input().split()))

    # Print Equations 1 and 2 from user's inputs
    print("\nYou provided the following LD-instance Q:\n\n"
          f"   Equation 1: {eq1.C1}x1 + {eq1.C2}x2 + {eq1.C3}x3 + {eq1.C} = 0\n"
          f"   Equation 2: {eq2.C1}x1 + {eq2.C2}x2 + {eq2.C3}x3 + {eq2.C} = 0\n")

    # Create finite automaton M1 from equation 1
    M1 = M(eq1)
    # Create finite automaton M2 from equation 2
    M2 = M(eq2)
    # Create finite automaton MX from M1 x M2
    MX = MxM(M1, M2)
    # Find a path in MX from the initial state to the accepting state
    path = findPath(MX)

    # Check if a path was found
    if path is not None:
        # Calculate and print the solution from the path
        solution = solutionFromPath(path)
        print(f"Solution found: x1 = {solution[0]}, x2 = {solution[1]}, x3 = {solution[2]}\n")
    else:
        # Inform the user there is no solution
        print("No solution found.\n")

# Run main() if file is directly executed
# Does not run main() if file is imported as a module
if __name__ == '__main__':
    main()