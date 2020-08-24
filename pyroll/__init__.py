import re
import random
import argparse


NOTATION_OPERATOR_ADD = ['+']
NOTATION_OPERATOR_SUBTRACT = ['-']
NOTATION_OPERATOR_MULTIPLY = ['*', 'x']
NOTATION_OPERATOR_DIVIDE = ['/', '%']
NOTATION_OPERATORS = [
    NOTATION_OPERATOR_ADD,
    NOTATION_OPERATOR_SUBTRACT,
    NOTATION_OPERATOR_MULTIPLY,
    NOTATION_OPERATOR_DIVIDE,
]

OPERATOR_PRECEDENCE = ['*', '/', '-', '+']
NOTATION_OPERATORS_STR_ESCAPED = '(' + '|'.join(['\\' + operator for operator in OPERATOR_PRECEDENCE]) + ')'
RE_PATTERN_DICE = re.compile(r'(\d*)d(\d+)')


def normalize_symbols(notation):
    normalized = notation.replace(' ', '')

    for operator in NOTATION_OPERATORS:
        if len(operator) > 1:
            normal = operator[0]
            targets = operator[1:]

            for target in targets:
                normalized = normalized.replace(target, normal)

    return normalized


def split_on_operators(notation):
    return re.split(NOTATION_OPERATORS_STR_ESCAPED, notation)


def is_operator(item):
    return item and (item in OPERATOR_PRECEDENCE)


def calculate_dice(notation):
    match = re.match(RE_PATTERN_DICE, notation)

    count = int(match.group(1) or 1)
    sides = int(match.group(2))

    sum = 0

    for i in range(0, count):
        sum += random.randint(1, sides)

    return sum


def calculate_dices(parts):
    for index, part in enumerate(parts):
        if 'd' in part:
            parts[index] = calculate_dice(part)

    return parts


def apply_operator(a, b, operator_str):
    if operator_str == '+':
        return a + b
    elif operator_str == '-':
        return a - b
    elif operator_str == '*':
        return a * b
    elif operator_str == '/':
        return a / b


def apply_operators(parts):
    for operator in OPERATOR_PRECEDENCE:
        for index, part in enumerate(parts):
            if is_operator(part):
                if part == operator:
                    if len(parts) == 1:
                        return parts

                    a = int(parts[index - 1])
                    b = int(parts[index + 1])

                    parts = apply_operators(parts[:index - 1] + [apply_operator(a, b, operator)] + parts[index + 2:])

    return parts


def roll(notation):
    clean_notation = normalize_symbols(notation).lower()
    parts = split_on_operators(clean_notation)
    parts = calculate_dices(parts)
    total = apply_operators(parts)[0]

    return total


def create_parser():
    parser = argparse.ArgumentParser(
        prog='pyroll',
        description='Dice notation parsing and rolling',
    )

    parser.add_argument('-v, --verbose', dest='verbose', action='store_true', help='Include dice notation in output')
    parser.add_argument('dice', metavar='DICE', type=str, nargs='+')

    return parser


def main():
    args_parser = create_parser()
    args = args_parser.parse_args()

    for dice in args.dice:
        print(f'{(dice + " = ") if args.verbose else ""}{roll(dice)}')


if __name__ == '__main__':
    main()
