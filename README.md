# LR(0) Parsing Table Generator

An important step in the front-end process of a compiler is the parsing stage. After turning a statement into a set of tokens, the parser will compare the tokens to a pre-defined programming language grammar to ensure it can compile without error.

This Python script can take a simple grammar, augment its topmost production, and create an LR(0) DFA and parsing table. It displays the parsing table using tabulate.

<div align="center">

**Screenshots:**

| <!-- -->                                                                                               |
|:------------------------------------------------------------------------------------------------------:|
| ![image](https://github.com/umlaufg/lr0_table_gen/blob/main/docs/images/lr0_screenshot_1.PNG?raw=true) |
| *The example grammar provided in the script; Its formal representation*                                |
| ![image](https://github.com/umlaufg/lr0_table_gen/blob/main/docs/images/lr0_screenshot_2.PNG?raw=true) |
| *The automata for this grammar; The parsing table generated from those states*                         |

</div>
