# author: Manuel Penz


# This program matches a given word with a regular expression
#
# It supports:
#       union           e | f
#       concatenation   ef
#       plus            (e)+
#       Kleene star     (e)*

import string

# checks if the given word and expression coincide in their alphabet by checking if not more letters are in the word
# than there are in the expression
def checkWord(w, e):
    alpha = string.ascii_lowercase

    # remove letter in alpha if this letter is in the regex
    # check if the word has any letter from the remaining alpha
    #       yes - no valid word
    #       no - valid word
    for regIndex in range(len(e)):
        if e[regIndex].isalpha():
            alpha = alpha.replace(e[regIndex], '')

    for aIndex in range(len(alpha)):
        if alpha[aIndex] in w:
            print('Word contains a letter not from the regex!')
            exit()

# check if a given single character is the Kleen Star operator
def isKleene(char):
    return char == '*'

# check if a gicen single character is the Plus operator
def isPlus(char):
    return char == '+'

# check if the given single character is an open bracket
def isOpenBrac(char):
    return char == '('

# check if zhe given single character is a closed bracket
def isCloseBrac(char):
    return char == ')'

# check if the given single character is an operator (kleene or plus)
def isOp(char):
    return isKleene(char) or isPlus(char)

# check if the given single character is a letter or a number
def isSingleChar(char):
    return char.isalpha() or char.isdigit()

# check if a substring sub of the expression is in brackets
def isInBrac(sub):
    return isOpenBrac(sub[0]) and isCloseBrac(sub[-1])

# check if a substring sub of the expression is a union (open bracket, pipe symbol and closed bracket)
def isUnion(sub):
    return isOpenBrac(sub[0]) and isCloseBrac(sub[-1])

# check if a substring is a "unit" - eiter a single literal or it is inside brackets
def isUnit(sub):
    return isSingleChar(sub[0]) or isInBrac(sub)

# return a list of characters inside the brackets
def splitBrac(sub):
    return list(sub[1:-1])

# return a list of alternatives for union inside the brackets
def splitUnion(union):
    return union[1:-1].split('|')

# split the given expression up in head, operator and tail
# if the fist character of the expression starts with a bracket then it is the tail
#      otherwise the second literal is the head
# if the literal afterwards is an operator then set it as an operator
# always set rest as the tail
def splitExp(e):
    head = None
    op = None
    tail = None
    posLastExp = None

    if isOpenBrac(e[0]):
        posLastExp = e.find(')') + 1
        head = e[:posLastExp]
    else:
        posLastExp = 1
        head = e[0]

    if posLastExp < len(e) and isOp(e[posLastExp]):
        op = e[posLastExp]
        posLastExp += 1

    tail = e[posLastExp:]

    return head, op, tail

# check if a "unit" is matching
# this can be eiter a single character or it can be a substring of the expression in brackets
def isUnitMatching(w, e):
    head, op, tail = splitExp(e)

    if len(w) == 0:
        return False
    if isSingleChar(head):
        return w[0] == e[0]
    elif isInBrac(head):
        inBrac = splitBrac(head)
        return w[0] in inBrac

    return False

# trying to match as many units as possible with the word by first finding the longest length that is possible to match
# by changing the regex itself and replacing it stepwise with multiple occurrences of what the Kleene Star/Plus operator
# initially referred to
# after finding the longest submatch, the second loop reduces the number of occurrences so that it does not mess up the
# rest of the string
# e.g:      exp: ab*b
#           str: abbbbbbbbbb <--- Last b is not part of the Kleene star, thats why there is the second loop
def matchMultiple(w, e, minMatch=None, maxMatch=None):
    head, op, tail = splitExp(e)

    if not minMatch:
        minMatch = 0

    subMatch = -1

    while not maxMatch or (subMatch < maxMatch):
        matched = match(w, (head * (subMatch + 1)))

        if matched:
            subMatch += 1
        else:
            break

    while subMatch >= minMatch:
        matched = match(w, (head * subMatch) + tail)

        if matched:
            return matched
        subMatch -= 1

    return False

# match Kleene by calling matchMultiple with no minimum and no maximum occurrence
def matchKleene(w, e):
    return matchMultiple(w, e, None, None)

# match Plus by calling matchMultiple with one minimum and no maximum occurrence
def matchPlus(w, e):
    return matchMultiple(w, e, 1, None)

# match a union by checking the possible optional characters and trying to match all of these options
def matchUnion(w,e):
    head, op, tail = splitExp(e)

    optional = splitUnion(head)
    for opt in optional:
        matched = match(w, opt + tail)

        if matched:
            return matched

    return False

# actual match function which gets called recursively for every literal in the word
def match(w,e):
    if len(e) == 0:
        return True
    elif e[0] == '$':
        if len(w)==0:
            return True
        else:
            return False

    head, op, tail = splitExp(e)

    if isKleene(op):
        return matchKleene(w, e)
    elif isPlus(op):
        return matchPlus(w, e)
    elif isUnion(head):
        return matchUnion(w,e)
    elif isUnit(head):
        if isUnitMatching (w, e):
            return match(w[1:], tail)
    else:
        print('Not supported by this regex!')

    return False

# Main function
# asks if the user wants to check a word to the given regex or if the user want to define a custom regex and enter a
# word to compare
def main():

    # choose between predefined regex or not
    print('This program matches a word against a regular expression.')
    print('It supports regex with union (a|b), concatenation (ab), multiple (a)+ and Kleene star (a)*.\n')

    print('1 ... Input a word and test it against the given regex (a+b)*a(ab)*')
    print('2 ... Input a word and test it against an input regex')
    print('Choose: ')
    choice = int(input())

    if (choice == 1):
        print('Enter a word:')
        word = input()
        testRegex = '(a|b)*a(ab)*'

        # check if the entered word is valid and if the word contains only letters from the regex
        checkWord(word, testRegex)
        # match the word with the regex
        matched = match(word, testRegex+'$')
        if matched:
            print(f'The word \'{word}\' and regex \'{testRegex}\' are matching!')
        else:
            print(f'The word \'{word}\' and regex \'{testRegex}\' are not matching!')

    elif (choice == 2):
        print('Enter a word:')
        word = input()
        print('Enter a regex')
        regex = input()

        # check if the entered word is valid and if the word contains only letters from the regex
        checkWord(word, regex)
        # match the word with the regex
        matched = match(word, regex+'$')
        if matched:
            print(f'The word \'{word}\' and regex \'{regex}\' are matching!')
        else:
            print(f'The word \'{word}\' and regex \'{regex}\' are not matching!')

    else:
        print('Wrong option - try again!')

if __name__ == '__main__':
    main()