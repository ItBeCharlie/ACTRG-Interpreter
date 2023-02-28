from basic import Basic as B
from transitions import transitions as trans
from dictionary import dictionary as global_dictionary


def main():
    sentence = input('Enter a sentence: ')
    basic_list = sentence_to_basic_list(sentence)
    print(basic_list)


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


def reduce_check(sentence, start, end, pairs=[]):
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
    # Base case: Empty sentence is valid
    if end-start <= 0:
        return True, pairs
    # Sentences cannot have an odd number of basic types
    # NOTE: This can be extracted to a different method, as it does
    # not need to be checked during every recursive call, but only
    # needs to be done once at the start of the check
    if len(sentence) % 2 == 1:
        return False, []
    # Work our way backwards through the sentence, checking every
    # other basic_tuple, and seeing if we have a valid pair
    for index in range(end-1, start, -2):
        # Check if the given pair is a valid match
        if match(sentence[index], sentence[end]):
            # Add our new paid
            pairs.append((index, end))
            # Recursive call for outer and inner structure
            return reduce_check(sentence, start, index-1, pairs) \
                and reduce_check(sentence, index+1, end-1, pairs)
    # If we check every term and do not find a match, the sentence is invalid
    return False, []


main()
