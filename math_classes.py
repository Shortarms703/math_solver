class Base:
    def __init__(self):
        self._current = -1

    def __iter__(self):
        self._current = -1
        return self

    def __next__(self):
        self._current += 1
        if self._current >= len(self):
            raise StopIteration
        else:
            return self[self._current]

    def __len__(self):
        return len(self.get_items())

    def __getitem__(self, item):
        items = self.get_items()
        return items[item]

    def __setitem__(self, key, value):
        self.get_items()[key] = value

    def __eq__(self, other):
        return str(self) == str(other)

    def latex(self):
        raise NotImplementedError

    def is_solvable(self):  # meaning there is are no other operations inside it
        return all(issubclass(type(each), str) for each in self)

    def solve_self(self):
        raise NotImplementedError

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
        return str(self.sections)  # TODO [str(x) for x in self.sections] right?

    def __setitem__(self, key, value):
        self.sections[key] = value

    def get_items(self):
        return self.sections

    def fully_defined(self):  # TODO this needs to be recursive
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

    def solve_self(self):
        if all(float(each).is_integer() for each in self):
            return str(sum(int(x) for x in self))
        else:
            return str(sum(float(x) for x in self))

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


class Subtraction(Addition):  # TODO call repr and latex functions of Addition but .replace('+', '-')
    def __repr__(self):
        return_string = ''
        for each in self.sections:
            if para_needed(type(self), type(each)):
                return_string += '(' + str(each) + ')' + ' - '
            else:
                return_string += str(each) + ' - '
        return return_string[:-3]

    def solve_self(self):  # FIXME if Base objects can have more than one item coming out of order_operations()
        if all(float(each).is_integer() for each in self):
            return str(int(float(self[0]) - float(self[1])))
        else:
            return str(float(self[0]) - float(self[1]))

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

    def solve_self(self):
        total = 1
        for each in self:
            total *= int(each)
        return str(total)

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
        return '(' * num_para + str(self.numerator) + ')' * num_para + '/' + '(' * den_para + str(
            self.denominator) + ')' * den_para

    def __setitem__(self, key, value):
        if key == 0:
            self.numerator = value
        if key == 1:
            self.denominator = value

    def solve_self(self):
        if (float(self.numerator) / float(self.denominator)).is_integer():
            return str(int(float(self.numerator) / float(self.denominator)))
        else:
            return str(float(self.numerator) / float(self.denominator))

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
            return '(' * base_para + str(self.base) + ')' * base_para + '^' + '(' * power_para + str(
                self.power) + ')' * power_para

    def __setitem__(self, key, value):
        if key == 0:
            self.base = value
        if key == 1:
            self.power = value

    def solve_self(self):
        return str(int(self.base) ** int(self.power))

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


class Variable(Base):  # TODO still not used yet
    def __init__(self, variable):
        super().__init__()
        self.variable = variable

    def __repr__(self):
        return self.variable

    def latex(self):
        return self.variable

    def get_items(self):
        return [self.variable]


def para_needed(first, second):
    class_list = [[Addition, Subtraction], [Fraction, Multiplication], [Exponent, Logarithm], [Variable]]

    for operator_subset in class_list:
        if first in operator_subset and second in operator_subset:
            return False
        elif first in operator_subset:
            return False
        elif second in operator_subset:
            return True