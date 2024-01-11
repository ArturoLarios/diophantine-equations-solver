# diophantine-equations-solver

## Background

This script solves a system of two linear Diophantine equations in three variables. The system of equations is given as follows:

- **Equation 1:** \(C_{11}x_1 + C_{12}x_2 + C_{13}x_3 + C_1 = 0\)
- **Equation 2:** \(C_{21}x_1 + C_{22}x_2 + C_{23}x_3 + C_2 = 0\)

Taking the user's input for the coefficients and constants of both equations, it constructs finite automata (labeled graphs) M~1~ ​ and M~2~ ​ from the equations, and then constructs a finite automaton M~x~M from the Cartesian product. Then, a depth-first search (DFS) algorithm is applied to find a path from the initial state to the accepting state in M~x~M, representing a solution to the system of equations. If such a solution exists, the script will output it in the form  x~1~ = a, x~2~ = b , x~3~ = c where a, b, c are non-negative integers.

## Dependencies

Python 3.x

## Credits

The algorithm for solving Linear Diophantine equations using graph theory is based on the brilliant ideas discussed in CPT_S 516 by Zhe Dang at WSU.

## License

This project is licensed under the MIT License - see the LICENSE file for details.