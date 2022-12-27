ACTRG Interpreter

Simple overview of use/purpose.

## Description

An in-depth paragraph about your project and overview of use.

### Installing

-   Use git to download main file

```shell
git clone https://github.com/ItBeCharlie/ACTRG-Interpreter
```

### Executing program

-   How to run the program
-   Step-by-step bullets
-   For textfile, enter the file that specifies the grammar you want to test
-   Debug is an optional argument you can add to see the stack trace

```

py interpreter.py \[textfile] (debug)

```

-   The textfile should be specified as follows:
-   (Note anything in parenthesis should NOT be added)

```
(To specify given productions, write them in the following format)
v > pi
v > o
(To specify the dictionary for the given language: )
John : v
Marie : v
adores : pi_r s o_l
```

Example of what the file looks like without the comments above:

```
v > pi
v > o
John : v
Marie : v
adores : pi_r s o_l
```

## Authors

Contributors names and contact info

Charlie DeGennaro
Andrew McDonald

## Other Notes

Precedence is the main system used to know when to push or pop items
from the stack. To achieve this, we converted each superscript "r" to 1,
and each "l" to -1. To get the precedence, we then add up all these values
to get a numerical representation of precedence. Smaller values are always
less precedence, for example:

```
pi pi_r

converts to

('pi', 0) ('pi', 1)
```

## Example Output

Without debug

```
PS D:\Code\ResearchGroup> py interpreter.py test2.txt
Accept
v   pi_r   s   o_l   v   s_r
└─────┘    │    └────┘    │
           └──────────────┘
```

With debug

```
PS D:\Code\ResearchGroup> py interpreter.py test2.txt debug
Token: ('v', 0)
Stack: []

Token: ('pi', 1)
Stack: [('v', 0)]

Token: ('s', 0)
Stack: []

Token: ('o', -1)
Stack: [('s', 0)]

Token: ('v', 0)
Stack: [('s', 0), ('o', -1)]

Token: ('s', 1)
Stack: [('s', 0)]

Accept
v   pi_r   s   o_l   v   s_r
└─────┘    │    └────┘    │
           └──────────────┘
```

## Version History

1.0 Initial Functionality
1.1 Added ability to define dictionary
