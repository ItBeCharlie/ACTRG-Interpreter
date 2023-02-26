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


def is_valid_basic_list(basic_list):
    for tuple in basic_list:
        pass


main()
