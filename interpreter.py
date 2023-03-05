from basic import Basic as B
from transitions import transitions as trans
from dictionary import dictionary as global_dictionary
from enum import Enum


def main():
    sentence = input('Enter a sentence: ')
    basic_list = sentence_to_basic_list(sentence)
    display_enums(basic_list)
    valid, pairs = reduce_check(basic_list)
    print(valid)
    if valid:
        print(sentence)
        draw_underlinks(basic_list, pairs)


def display_enums(sentence):
    s = '['
    for tuple in sentence:
        s += f'({tuple[0].name}, {tuple[1]}), '
    print(s[0:-2] + ']')


def sentence_to_basic_list(sentence):
    basic_list = []
    sentence_list = sentence.split()
    # Get the basic types for each word in the sentence from the global dictionary
    for word in sentence_list:
        basic_list.extend(global_dictionary[word])
    return basic_list


def match(left_tuple, right_tuple):
    """
    Checks if the left and right tuple can be reduced to 1
    """
    # Check that the left precedence is 1 less that the right precedence
    if right_tuple[1] - left_tuple[1] != 1:
        return False
    # Check if the tuples are the same basic type, no further checks needed
    if right_tuple[0] == left_tuple[0]:
        return True
    # Transitions can only occur on 0 precedence
    # We check if the left or right tuple is the one with 0 precedence
    # Then by comparing the basic type to all possible transitions of the other
    # We can verify if the match can be made
    if left_tuple[1] == 0:
        return right_tuple[0] in trans[left_tuple[0]]
    return left_tuple[0] in trans[right_tuple[0]]


def reduce_check(sentence):
    # Sentences cannot have an odd number of basic types
    if len(sentence) % 2 == 1:
        return False, []
    valid, pairs, depth = reduce_check_helper(sentence, 0, len(sentence)-1)
    return valid, pairs


def reduce_check_helper(sentence, start, end, pairs=[]):
    """
    Recursive method to reduce an entire sentence. Will return True if 
    the sentence can be reduced all the way to 1, as well as a list of all
    the pairs made in the reduction. If the reduction is invalid, the pairs
    will be returned as an empty list

    @param sentence: List of basic tuples
    @param start: Starting index of sublist
    @param end: End index of sublist
    @param pairs: List of all the pairs that reduce with each other

    @return boolean, list
    """
    # print(f'S: {start}, E: {end}')
    # Base case: Empty sentence is valid
    if end-start <= 0:
        return True, pairs, 0
    # Work our way backwards through the sentence, checking every
    # other basic_tuple, and seeing if we have a valid pair
    for index in range(end-1, start-1, -2):
        # Check if the given pair is a valid match
        # print(index, end)
        if match(sentence[index], sentence[end]):
            # Recursive call for outer
            valid_outer, pairs, depth_outer = reduce_check_helper(
                sentence, start, index-1, pairs)
            # Recursive call for inner
            valid_inner, pairs, depth_inner = reduce_check_helper(
                sentence, index+1, end-1, pairs)
            # Calculate depth of current tuple
            depth = depth_inner + 1
            # Add our new pair
            pairs.append((index, end, depth))
            # print(pairs)
            # Recursive call for outer and inner structure
            return valid_outer and valid_inner, pairs, depth
    # If we check every term and do not find a match, the sentence is invalid
    return False, []


# class SymbolSet(Enum):
#     VERTICAL = '│'
#     LEFTCORNER = '└'
#     RIGHTCORNER = '┘'
#     HORINZONTAL = '─'


class SymbolSet(Enum):
    VERTICAL = '║'
    LEFTCORNER = '╚'
    RIGHTCORNER = '╝'
    HORINZONTAL = '═'


def draw_underlinks(tuple_sentence, pairs, gap=3):
    formatted_sentence = []
    for tuple in tuple_sentence:
        if tuple[1] < 0:
            formatted_sentence.append(f'{tuple[0].name}_{"l"*-tuple[1]}')
        elif tuple[1] > 0:
            formatted_sentence.append(f'{tuple[0].name}_{"r"*tuple[1]}')
        else:
            formatted_sentence.append(f'{tuple[0].name}')

    middle_indexes = get_middle_str_indexes(formatted_sentence, gap)
    print((' '*gap).join(formatted_sentence))

    cur_depth = 1
    max_depth = max(list(map(lambda tuple: tuple[2], pairs)))

    while cur_depth <= max_depth:
        underlink_chars = ['' for _ in range(len(pairs)*2)]
        for pair in pairs:
            depth = pair[2]
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

# returns list with indexes of all the middles of each str


def get_middle_str_indexes(sentence, gap=3):
    total_length = 0
    out = []
    for token in sentence:
        mid = len(token)//2
        out.append(total_length + mid)
        total_length += gap + len(token)
    return out


main()
