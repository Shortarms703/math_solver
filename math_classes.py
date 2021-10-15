from typing import Union


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

    def __setitem__(self, key, value):
        self.sections[key] = value

    def get_items(self):
        return self.sections


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


class SingleVariable(Base): # TODO dont think this is needed ||| it is for .fully_defined()
    def __init__(self, variable):
        super().__init__()
        self.variable = variable

    def __repr__(self):
        return self.variable

    def get_items(self):
        return [self.variable]


def para_needed(first, second):
    class_list = [[Addition], [Fraction, Multiplication, SingleVariable], [Exponent, Logarithm]]

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


def order_operations(expression): # TODO add logs
    operator_classes = {'+': Addition, '-': Addition, '*': Multiplication, '/': Fraction, '^': Exponent} # TODO add logs
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

    # -- TESTING --
    accum = ''
    for x, y in sorted(operator_dict.items(), key=lambda x: x[0]):
        accum += ' ' * (x - len(accum)) + str(y)
    print('-' * len(expression))
    print(expression)
    print(accum)
    print('-' * len(expression))


    final = None
    previous = ''
    for n, importance in sorted(operator_dict.items(), key=lambda x: -x[1]):
        section = expression[:n]
        bits = []
        if any(x in section for x in all_operators):
            section = section[::-1]
            for i, ch in enumerate(section):
                if ch in all_operators:
                    bits.append(section[:i])
                    break
        else:
            bits.append(section)
        section = expression[n+1:]
        if any(x in section for x in all_operators):
            for i, ch in enumerate(section):
                if ch in all_operators:
                    bits.append(section[:i])
                    break
        else:
            bits.append(section)
        if final:
            # if expression[n] == '/':
            #     final = operator_classes[expression[n]](final, bits[-1])
            # else:
            #     final = operator_classes[expression[n]](final, bits[-1])
            if n > previous:
                final = operator_classes[expression[n]](final, bits[-1])
            if n < previous:
                final = operator_classes[expression[n]](bits[0], final)
            pass
        else:
            final = operator_classes[expression[n]](*bits)
        previous = n
    return final
    # accum = []
    # expression = expression.replace(' ', '')
    # looping = expression
    # statements = [expression]
    # for n, ch in enumerate(looping):
    #     if '(' not in looping:
    #         break
    #     if ch == '(':
    #         loc = bracket_span(looping[n:], brackets='()')
    #         looping = looping[n:n + loc]
    #         statements.append(looping[1:])
    # # return statements
    # x = statements.copy()
    # for n, each in enumerate(statements[:0:-1]):
    #     a = statements[::-1][n+1].index(each)
    #     x[-(n + 2)] = [x[-(n + 2)][:a], x[-(n + 1)], x[-(n + 2)][a + len(each):]]
    # return x[0]
    #     # print(statements[::-1][n+1][a:a + len(each)])
    #
    # return statements



expression = '(1+2^2)/3+4*4'
print(str(order_operations(expression)).replace(' ', ''))
# print(order_operations(expression))


tests = False
if tests:
    assert str(order_operations('(1+2^2)/3+4')) == '(1 + 2^2)/3 + 4'

