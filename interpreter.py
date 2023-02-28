from basic import Basic as B
from transitions import transitions as trans
from dictionary import dictionary as global_dictionary


def main():
    sentence = input('Enter a sentence: ')
    basic_list = sentence_to_basic_list(sentence)
    display_enums(basic_list)
    valid, pairs = reduce_check(basic_list)
    print(valid)
    if valid:
        print(pairs)


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
    valid, pairs = reduce_check_helper(sentence, 0, len(sentence)-1)
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
        return True, pairs
    # Work our way backwards through the sentence, checking every
    # other basic_tuple, and seeing if we have a valid pair
    for index in range(end-1, start-1, -2):
        # Check if the given pair is a valid match
        # print(index, end)
        if match(sentence[index], sentence[end]):
            # Add our new paid
            pairs.append((index, end))
            # print(pairs)
            # Recursive call for outer and inner structure
            valid, pairs = reduce_check_helper(sentence, start, index-1, pairs) \
                and reduce_check_helper(sentence, index+1, end-1, pairs)
            return valid, pairs
    # If we check every term and do not find a match, the sentence is invalid
    return False, []


main()
