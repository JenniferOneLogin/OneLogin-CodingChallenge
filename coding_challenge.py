#!/usr/bin/env python3

# Coding Challenge Submission
# Name: Jennifer Assaf
# Date: 07/05/2021
# Description: Command line program written in python that takes fractional math as input.

import sys
import re
import operator
import argparse

ops = {
    '+': operator.add,
    '-': operator.sub,
    '*': operator.mul,
    '/': operator.truediv,
}


def main():
    while True:
        user_input = validate_input()

        operator = get_operator(user_input)

        if re.findall('(\s*(?<![_\/])[\d*](?![_\/])\s*)', user_input):
            user_input = convert_whole_number(user_input)

        parsed_string = list(filter(None, re.split('\W', user_input)))

        check_mixed_numbers(parsed_string)

        if parsed_string[1] == '0' or parsed_string[3] == '0':
            print(f"Invalid Input")
            validate_input()

        if operator == '/':
            parsed_string[2], parsed_string[3] = parsed_string[3], parsed_string[2]
            operator = '*'

        get_common_denominator(parsed_string)

        numerator, denominator, whole_number = do_the_math(operator, parsed_string)

        factor = get_largest_factor(numerator, denominator)

        final_fraction = reduce_and_reassemble(whole_number, numerator, denominator, factor)

        print(f"= {final_fraction}")


def reduce_and_reassemble(whole, nume, denom, fact):
    """Converts fraction to correct format

   Parameters
   ----------
    whole : int
       whole number to create mixed numbers
    nume : int
       the fraction numerator
    denom : int
       the fraction denominator

   Returns
   -------
   fraction_string : str
       the converted fraction
   """
    nume = str(int(nume / fact))

    denom = str(int(denom / fact))

    if whole != 0:
        fraction_string = f"{str(int(whole))}_{nume}/{denom}"
    elif denom == '1':
        fraction_string = f"{nume}"
    else:
        fraction_string = f"{nume}/{denom}"
    return fraction_string


def get_largest_factor(a, b):
    if a == 0:
        return b
    if b == 0:
        return a
    return get_largest_factor(b, a % b)


def do_the_math(op, input_string):
    """Does the desired mathematical operation using operator library

    Parameters
    ----------
    input_string : list
      parsed string in list format
    op : str
      the desired mathematical operation (+, -, *)

    Returns
    -------
    whole : int
       whole number to create mixed numbers
    nume : int
       the fraction numerator
    denom : int
       the fraction denominator
    """

    whole = 0
    nume = ops[op](input_string[0], input_string[2])

    if op == '*':
        denom = ops[op](input_string[1], input_string[3])
    else:
        denom = input_string[1]

    while (nume > denom):
        if nume > denom:
            whole = nume % denom
            if whole != 0:
                nume -= denom
            else:
                break
    if nume < 0 and abs(nume) > denom:
        positive_nume = abs(nume)
        while (positive_nume > denom):
            if positive_nume > denom:
                whole = positive_nume % denom
                if whole != 0:
                    positive_nume -= denom
                else:
                    break
        if whole > 0:
            whole *= -1
            nume = positive_nume
        else:
            nume = positive_nume * -1

    return nume, denom, whole


def get_common_denominator(input_string):
    """Multiplies both denominators to find common denominator

    Parameters
    ----------
    input_string : list
      parsed string in list format

    """
    first_multiplier = int(input_string[3])
    second_multiplier = int(input_string[1])

    for index, val in enumerate(input_string):
        if index in {0, 1}:
            input_string[index] = int(val) * first_multiplier
        else:
            input_string[index] = int(val) * second_multiplier


def check_mixed_numbers(input_string):
    """Converts mixed numbers into improper fractions

    Parameters
    ----------
    input_string : list
      parsed string in list format

    """
    for index, second in enumerate(input_string):
        if '_' == input_string[index]:
            whole, numerator = input_string[index].split('_')
            input_string[index] \
                = (int(whole) * int(input_string[index + 1])) + int(numerator)


def convert_whole_number(input_string):
    """Checks for the existence of single whole numbers and converts to fractions.
    If a number is singular -- i.e 2, then it  will be converted to 2/1

    Parameters
    ----------
    input_string : list
      parsed string in list format

    """
    itera = re.finditer('(\s*(?<![_\/])[\d*](?![_\/])\s*)', input_string)

    for index, val in enumerate(itera):
        input_string = input_string[:val.end() + (index * 2)] + "/1" + input_string[val.end() + (index * 2):]

    return str(input_string)


def get_operator(input_string):
    return next((i for i in input_string if i in '+' '-' '*'), None) or '/'


def validate_input():
    """Validates correct user input.
    """
    input_string = input('? ')
    while not re.match("((\d+_\d+\/\d+)|(\d+\/\d+)|\d+)\s+([+\-\*\/])\s+((\d+_\d+\/\d+)|(\d+\/\d+)|\d+)$",
                       input_string):
        print("Invalid Input")
        input_string = input('? ')
    return input_string


if __name__ == "__main__":
    main()
