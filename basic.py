from enum import Enum


class Basic:
    PI = 0  # subject
    PI1 = 1  # first person singular subject
    PI2 = 2  # second person singular and any plural personal subject
    PI3 = 3  # third person singular subject
    PIHAT3 = 4  # pseudo-subject
    S = 5  # declarative sentence, aka statement
    S1 = 6  # statement in present tense
    S2 = 7  # statement in past tense
    QBAR = 8  # question
    Q = 9  # yes-or-no question
    Q1 = 10  # yes-or-no question in present tense
    Q2 = 11  # yes-or-no question in past tense
    SBAR = 12  # indirect statement
    T = 13  # indirect question
    SIGMA = 14  # direct or indirect sentence
    I = 15  # infinitive of intransitive verb
    J = 16  # infinitive of complete verb phrase
    JBAR = 17  # complete infinitive with *to*
    PHI = 18  # quasi-sentence with infinitive
    PSI = 19  # quasi-sentence with participle
    O = 20  # direct object
    OPRIME = 21  # indirect object
    OHAT = 22  # pseudo-object
    N = 23  # name
    N0 = 24  # mass noun
    N1 = 25  # count noun
    N2 = 26  # plural noun
    NBAR = 27  # complete noun phrase
    NBAR0 = 28  # complete noun phrase first person
    NBAR1 = 29  # complete noun phrase second person
    NBAR2 = 30  # complete noun phrase third person
    A = 31  # predictive adjective
    ABAR = 32  # predicative adjectival phrase
    P1 = 33  # present participle
    P2 = 34  # past participle
    IPRIME = 35
    JPRIME = 36
