from enum import Enum
import sys


def main():
    global debug
    # Parse input file from args
    input_str, given_productions = parse_file(sys.argv[1])
    if len(sys.argv) > 2 and sys.argv[2] == "debug":
        debug = True
    else:
        debug = False

    # print(input_str)

    # print(given_productions)

    # Converts token list into tuple list
    grammar = parse_sentence(input_str)
    # print(grammar)

    # List of identity/given contractions
    # given_productions = [('v', 'p'), ('v', 'o')]
    # given_productions = [('n', 'p')]

    # Read in grammar list and evaluate the grammar
    parse_grammar(grammar, given_productions)

    # Using global variable from parse_grammar draw the underlinks to visualize pairs.
    draw_underlinks(input_str)

# Choose What SymbolSet to use


class SymbolSet(Enum):
    VERTICAL = '│'
    LEFTCORNER = '└'
    RIGHTCORNER = '┘'
    HORINZONTAL = '─'


# class SymbolSet(Enum):
#     VERTICAL = '║'
#     LEFTCORNER = '╚'
#     RIGHTCORNER = '╝'
#     HORINZONTAL = '═'


def parse_file(input):
    with open(input) as f:
        lines = f.readlines()
    sentence = lines[0].split()
    given_productions = []
    for i in range(1, len(lines)):
        line = lines[i]
        line = line.split()
        given_productions.append((line[0], line[2]))
    return sentence, given_productions


def parse_grammar(grammar, given_productions):
    global underlink_pairs
    global debug
    underlink_pairs = []
    stack = []
    index_stack = []
    for index, token in enumerate(grammar):
        if debug:
            print(f'Current Token: {str(token)}')
            print(f'Stack: {str(stack)}\n')
        # If the stack has equal/higher precedence push the token.
        if len(stack) == 0 or stack[-1][1] >= token[1]:
            stack.append(token)
            index_stack.append(index)

        # This handles higher/lower than baseline precedences
        # by simply comparing the symbols since we can not contract them.
        elif token[1] != 0 and stack[-1][1] != 0:
            if stack[-1][0] == token[0] and abs(token[1] - stack[-1][1]) == 1:
                stack.pop()
                underlink_pairs.append((index_stack.pop(), index))
            else:
                stack.append(token)
                index_stack.append(index)

        # Note this else does not handle higher/lower precedences (-1, 0), (0, 1)
        # because the internal logic can't handle it either.
        else:
            if token[1] == 0:
                if stack[-1][0] in valid_given_productions(given_productions, token[0]):
                    stack.pop()
                    underlink_pairs.append((index_stack.pop(), index))
                else:
                    stack.append(token)
                    index_stack.append(index)
            elif stack[-1][1] == 0:
                if token[0] in valid_given_productions(given_productions, stack[-1][0]):
                    stack.pop()
                    underlink_pairs.append((index_stack.pop(), index))
                else:
                    stack.append(token)
                    index_stack.append(index)

    # Check if successful parse
    if len(stack) == 0:
        print("Accept")
        # print(underlink_pairs)
    else:
        print("Reject")


"""
v   p_r   s   o_l   v   s_r
\____/    |    \____/    |
          \______________/
"""


def draw_underlinks(sentence, gap=3):
    middle_indexes = get_middle_str_indexes(sentence, gap)
    for token in sentence:
        print(token, end=' '*gap)
    print()

    cur_depth = 1
    max_depth = 1
    for pair in underlink_pairs:
        max_depth = max((pair[1]-pair[0]+1)//2, max_depth)
    while cur_depth <= max_depth:
        underlink_chars = ['' for _ in range(len(underlink_pairs)*2)]
        for pair in underlink_pairs:
            # This depth cacluation is incorrect because it forces the underlinks
            # to always print at their max depth and not the next depth.
            # Unsure how to fix.
            depth = (pair[1]-pair[0]+1)//2
            if depth == cur_depth:
                underlink_chars[pair[0]] = SymbolSet.LEFTCORNER.value
                underlink_chars[pair[1]] = SymbolSet.RIGHTCORNER.value
            elif depth > cur_depth:
                underlink_chars[pair[0]] = SymbolSet.VERTICAL.value
                underlink_chars[pair[1]] = SymbolSet.VERTICAL.value
        cur_char_index = 0
        gap_char = ' '
        cur_line = ''
        # This reads underlink_chars and draws the different symbols when
        # on a index that is in the middle of a token or not.
        for i in range(max(middle_indexes)+1):
            if i in middle_indexes:
                cur_line += underlink_chars[cur_char_index]
                if underlink_chars[cur_char_index] == SymbolSet.LEFTCORNER.value:
                    gap_char = SymbolSet.HORINZONTAL.value
                if underlink_chars[cur_char_index] == SymbolSet.RIGHTCORNER.value:
                    gap_char = ' '
                if underlink_chars[cur_char_index] == '':
                    cur_line += gap_char
                cur_char_index += 1
            else:
                cur_line += gap_char
        print(cur_line)
        cur_depth += 1

# returns list with indexs of all the middles of each str


def get_middle_str_indexes(sentence, gap=3):
    total_length = 0
    out = []
    for token in sentence:
        mid = len(token)//2
        out.append(total_length + mid)
        total_length += gap + len(token)
    return out

# returns list of all possible versions of given token


def valid_given_productions(productions, token):
    out = []
    for production in productions:
        if token == production[0]:
            out.append(production[1])
    out.append(token)
    return out

# Derives the precedence of each token and creates a tuple for each.
# Returns the list of tuples


def parse_sentence(sentence):
    out = []
    for token in sentence:
        if '_' in token:
            out.append(
                (token.split('_')[0], get_precedence(token.split('_')[1])))
        else:
            out.append((token, 0))
    return out


# Finds precedence for a given exponent
def get_precedence(exponent):
    count = 0
    for char in exponent:
        if char == 'r':
            count += 1
        elif char == 'l':
            count -= 1
    return count


main()
