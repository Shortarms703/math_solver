from typing import Union
from decimal import Decimal


class Base:
    def __init__(self):
        self.current = -1

    def __iter__(self):
        return self

    def __next__(self):
        self.current += 1
        if self.current < len(self):
            return self[self.current]
        raise StopIteration

    def __len__(self):
        return len(self.get_items())

    def __getitem__(self, item):
        items = self.get_items()
        return items[item]


    def __eq__(self, other):
        return str(self) == str(other)

    def latex(self):
        pass

    def get_items(self):
        raise NotImplementedError

    def fully_defined(self):
        for each in self:
            if type(each) == str:
                return False
        return True


class Expression(Base):
    def __init__(self, sections):
        super().__init__()
        if type(sections) == list:
            self.sections = sections
        else:
            self.sections = [sections]

    def __len__(self):
        return len(self.sections)

    def __repr__(self):
        return str(self.sections) # TODO [str(x) for x in self.sections] right?

    def __setitem__(self, key, value):
        self.sections[key] = value

    def get_items(self):
        return self.sections

    def fully_defined(self): # TODO this needs to be recursive
        for each in self.sections:
            if type(each) == str:
                return False
        return True

    def add_section(self, section):
        self.sections.append(section)


class Addition(Base):
    def __init__(self, *sections):
        super().__init__()
        self.sections = [x for x in sections]

    def __repr__(self):
        return_string = ''
        for each in self.sections:
            if para_needed(type(self), type(each)):
                return_string += '(' + str(each) + ')' + ' + '
            else:
                return_string += str(each) + ' + '
        return return_string[:-3]

    def latex(self):
        latex = ''
        for each in self.sections:
            if issubclass(type(each), Base):
                latex += each.latex() + ' + '
            else:
                latex += str(each) + ' + '
        return latex[:-3]

    def __setitem__(self, key, value):
        self.sections[key] = value

    def get_items(self):
        return self.sections


class Subtraction(Addition): # TODO call repr and latex functions of Addition but .replace('+', '-')
    def __repr__(self):
        return_string = ''
        for each in self.sections:
            if para_needed(type(self), type(each)):
                return_string += '(' + str(each) + ')' + ' - '
            else:
                return_string += str(each) + ' - '
        return return_string[:-3]

    def latex(self):
        latex = ''
        for each in self.sections:
            if issubclass(type(each), Base):
                latex += each.latex() + ' - '
            else:
                latex += str(each) + ' - '
        return latex[:-3]


class Multiplication(Base):
    def __init__(self, *sections):
        super().__init__()
        self.sections = [x for x in sections]

    def __repr__(self):
        return_string = ''
        for each in self.sections:
            if para_needed(type(self), type(each)):
                return_string += '(' + str(each) + ')' + ' * '
            else:
                return_string += str(each) + ' * '
        return return_string[:-3]

    def __setitem__(self, key, value):
        self.sections[key] = value

    def latex(self):
        latex = ''
        for each in self.sections:
            if issubclass(type(each), Base):
                if para_needed(type(self), type(each)):
                    latex += f'({each.latex()}) * '
                else:
                    latex += f'{each.latex()} * '
            else:
                latex += str(each) + ' * '
        return latex[:-3]

    def get_items(self):
        return self.sections


class Fraction(Base):
    def __init__(self, numerator, denominator):
        super().__init__()
        self.numerator = numerator
        self.denominator = denominator

    def __repr__(self):
        num_para = para_needed(type(self), type(self.numerator))
        den_para = para_needed(type(self), type(self.denominator))
        return '(' * num_para + str(self.numerator) + ')' * num_para + '/' + '(' * den_para + str(self.denominator) + ')' * den_para

    def __setitem__(self, key, value):
        if key == 0:
            self.numerator = value
        if key == 1:
            self.denominator = value

    def latex(self):
        latex = '\\frac'
        if issubclass(type(self.numerator), Base):
            latex += '{' + self.numerator.latex() + '}'
        else:
            latex += '{' + str(self.numerator) + '}'
        if issubclass(type(self.denominator), Base):
            latex += '{' + self.denominator.latex() + '}'
        else:
            latex += '{' + str(self.denominator) + '}'
        return latex

    def get_items(self):
        return self.numerator, self.denominator


class Exponent(Base):
    def __init__(self, base, power):
        super().__init__()
        self.base = base
        if type(power) == int:
            self.power = int(power)
        else:
            self.power = power

    def __repr__(self):
        if type(self.power) == Exponent:
            base_para = para_needed(type(self), type(self.base))
            power_para = True
            return '(' * base_para + str(self.base) + ')' * base_para + '^' + '(' * power_para + str(
                self.power) + ')' * power_para
        else:
            base_para = para_needed(type(self), type(self.base))
            power_para = para_needed(type(self), type(self.power))
            return '(' * base_para + str(self.base) + ')' * base_para + '^' + '(' * power_para + str(self.power) + ')' * power_para

    def __setitem__(self, key, value):
        if key == 0:
            self.base = value
        if key == 1:
            self.power = value

    def latex(self):
        latex = ''
        if issubclass(type(self.base), Base):
            if para_needed(type(self), type(self.base)):
                latex += f'({self.base.latex()}) ^'
            else:
                latex += f'{self.base.latex()} ^'
        else:
            latex += str(self.base) + '^'
        if issubclass(type(self.power), Base):
            latex += '{' + self.power.latex() + '}'
        else:
            latex += '{' + str(self.power) + '}'
        return latex

    def get_items(self):
        return self.base, self.power


class Logarithm(Base):
    def __init__(self, base, log_of):
        super().__init__()
        self.base = base
        self.log_of = log_of

    def __repr__(self):
        if self.base == 'e':
            return 'ln' + '(' + self.log_of + ')'
        if str(self.base) == '10':
            return 'log' + '(' + self.log_of + ')'
        else:
            base_para = para_needed(type(self), type(self.base))
            base = '(' * base_para + str(self.base) + ')' * base_para
            return 'log_' + base + '(' + self.log_of + ')'

    def __setitem__(self, key, value):
        if key == 0:
            self.base = value
        if key == 1:
            self.log_of = value

    def get_items(self):
        return [self.base, self.log_of]


class SingleVariable(Base): # TODO still not used yet
    def __init__(self, variable):
        super().__init__()
        self.variable = variable

    def __repr__(self):
        return self.variable

    def get_items(self):
        return [self.variable]


def para_needed(first, second):
    class_list = [[Addition, Subtraction], [Fraction, Multiplication, SingleVariable], [Exponent, Logarithm]]

    for operator_subset in class_list:
        if first in operator_subset and second in operator_subset:
            return False
        elif first in operator_subset:
            return False
        elif second in operator_subset:
            return True


def bracket_span(section, brackets='{}'):
    OPEN = brackets[0]
    CLOSE = brackets[1]
    total_open = 0
    for location, ch in enumerate(section):
        if ch == OPEN:
            total_open += 1
        if ch == CLOSE:
            total_open -= 1
        if total_open == 0:
            return location


def string_to_expression_obj(expression):
    final = Expression(expression)
    print(final)
    operator_chars = ['(', ')', '+', '-', '*', '/', '^'] # TODO add logs
    operator_chars = {'(': '', ')': '', '+': Addition, '-': Addition, '*': Multiplication, '/': Fraction, '^': Exponent} # TODO add logs
    section_final = final
    # while not final.fully_defined():


def stops_increasing(operator_dict, start):
    values_left = []
    list_importances = list(operator_dict.values())
    section = list_importances[:start][::-1]
    for i, j in zip(range(len(section)), list(operator_dict.keys())[:start][::-1]):
        if section[i] > list_importances[start]:
            values_left.append(j)
        else:
            break
    values_right = []
    section = list_importances[start+1:]
    for i, j in zip(range(len(section)), list(operator_dict.keys())[start+1:]):
        if section[i] > list_importances[start]:
            values_right.append(j)
        else:
            break
    if values_left and values_right:
        return min(values_left, key=lambda x: operator_dict[x]), min(values_right, key=lambda x: operator_dict[x])
    elif values_left:
        return min(values_left, key=lambda x: operator_dict[x]), None
    elif values_right:
        return None, min(values_right, key=lambda x: operator_dict[x])
    else:
        return None, None


def order_operations(expression):
    operator_classes = {'+': Addition, '-': Subtraction, '*': Multiplication, '/': Fraction, '^': Exponent} # TODO add logs
    operator_chars = {'+': 1, '-': 1, '*': 2, '/': 2, '^': 3}
    all_operators = ['+', '-', '*', '/', '^', '(', ')']
    para = 0
    operator_dict = {}
    for n, ch in enumerate(expression):
        if ch == ')':
            para -= 4
        if ch in operator_chars:
            operator_dict[n] = operator_chars[ch] + para
        if ch == '(':
            para += 4

    # TESTING ----------------------------
    # accum = ''
    # for x, y in sorted(operator_dict.items(), key=lambda x: x[0]):
    #     accum += ' ' * (x - len(accum)) + str(y)
    # print('-' * len(expression))
    # print(expression)
    # print(accum)
    # print('-' * len(expression))
    # print(operator_dict)

    # gives more priority to operators from left to right
    for i, loc in enumerate(operator_dict):
        operator_dict[loc] = operator_dict[loc] + 1 / (2+i)

    expression_dict = {}
    locations = {} # a dict with KEYS being operator locations that have been reference and VALUES being operator locations that reference to those keys
    for n1, n in enumerate(operator_dict.keys()):
        left, right = stops_increasing(operator_dict, n1)
        if left is None:
            left = ''
            for each in expression[:n][::-1]:
                if each not in all_operators:
                    left = each + left
                else:
                    break
        else:
            if left in locations:
                left = locations[left]
            else:
                locations[left] = n
        if right is None:
            right = ''
            for each in expression[n+1:]:
                if each not in all_operators:
                    right = right + each
                else:
                    break
        else:
            if right in locations:
                right = locations[right]
            else:
                locations[right] = n
        expression_dict[n] = [left, right]
    "{1: ['3', 4], 4: ['2', '1'], 7: [1, '3'], 9: [7, 11], 11: ['2', 14], 14: ['4', '1'], 17: [9, '6']}"
    # print('expression_dict before solving', expression_dict)
    while list in [type(x) for x in expression_dict.values()]:
        for loc in expression_dict:
            # if not issubclass(type(expression_dict[loc]), Base) and issubclass(type(expression_dict[right]), Base):
            left = expression_dict[loc][0]
            right = expression_dict[loc][1]
            if type(left) == str and type(right) == str:
                expression_dict[loc] = operator_classes[expression[loc]](left, right)
            if type(left) == str and type(right) == int:
                if issubclass(type(expression_dict[right]), Base):
                    expression_dict[loc] = operator_classes[expression[loc]](left, expression_dict[right])
            if type(left) == int and type(right) == str:
                if issubclass(type(expression_dict[left]), Base):
                    expression_dict[loc] = operator_classes[expression[loc]](expression_dict[left], right)
            if type(left) == int and type(right) == int:
                if issubclass(type(expression_dict[left]), Base) and issubclass(type(expression_dict[right]), Base):
                    expression_dict[loc] = operator_classes[expression[loc]](expression_dict[left], expression_dict[right])

    # print('expression_dict solved', expression_dict)
    return sorted(expression_dict.values(), key=lambda x: len(str(x)))[-1]
    # return str(sorted(expression_dict.values(), key=lambda x: len(str(x)))[-1]).replace(' ', '')


def latex_for_visual():
    expression = '((2+5)^(2+1)*(3+1)+2)/(4+1)-6'
    latex = order_operations(expression).latex()
    return latex


expression = '((2+5)^(2+1)*(3+1)+2)/(x-1)-6'
print(order_operations(expression))

# expression = input('enter math: ')
# print(order_operations(expression))
# print(latex)



tests = False
if tests:
    assert str(order_operations('(1+2^2)/3+4')) == '(1 + 2^2)/3 + 4'

