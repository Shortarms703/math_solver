from math_classes import *


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
    section = list_importances[start + 1:]
    for i, j in zip(range(len(section)), list(operator_dict.keys())[start + 1:]):
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
    operator_classes = {'+': Addition, '-': Subtraction, '*': Multiplication, '/': Fraction,
                        '^': Exponent}  # TODO add logs
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
        operator_dict[loc] = operator_dict[loc] + 1 / (2 + i)

    expression_dict = {}
    locations = {}
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
            for each in expression[n + 1:]:
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
    while list in [type(x) for x in expression_dict.values()]:
        for loc in expression_dict:
            left = expression_dict[loc][0]
            right = expression_dict[loc][1]
            if str(left).isalpha():
                left = Variable(left)
            if str(right).isalpha():
                right = Variable(right)
            if issubclass(type(left), (str, Base)) and issubclass(type(right), (str, Base)):
                expression_dict[loc] = operator_classes[expression[loc]](left, right)
            if type(left) == str and type(right) == int:
                if issubclass(type(expression_dict[right]), Base):
                    expression_dict[loc] = operator_classes[expression[loc]](left, expression_dict[right])
            if type(left) == int and type(right) == str:
                if issubclass(type(expression_dict[left]), Base):
                    expression_dict[loc] = operator_classes[expression[loc]](expression_dict[left], right)
            if type(left) == int and type(right) == int:
                if issubclass(type(expression_dict[left]), Base) and issubclass(type(expression_dict[right]), Base):
                    expression_dict[loc] = operator_classes[expression[loc]](expression_dict[left],
                                                                             expression_dict[right])
    return sorted(expression_dict.values(), key=lambda x: len(str(x)))[-1]


def latex_for_visual(expression):
    latex = order_operations(expression).latex()
    return latex


def traverse_nested_list(my_nested_list):
    results = []
    for my_item in my_nested_list:
        if type(my_item) is str:
            results.append(my_item)
        elif all(isinstance(each, str) for each in my_item):
            solved = my_item.solve_self()
            results.append(solved)
        elif issubclass(type(my_item), Base):
            results.append(traverse_nested_list(my_item))
    results = type(my_nested_list)(results[0], results[1])
    return results


def steps_to_solve(expression):
    steps = []
    if not issubclass(type(expression), Base):
        my_list = order_operations(expression)
    else:
        my_list = expression

    while any(issubclass(type(each), Base) for each in my_list):
        steps.append(my_list)
        my_list = traverse_nested_list(my_list)
    steps.append(my_list)
    steps.append(my_list.solve_self())
    return steps



print(steps_to_solve('2*(x+3)'))
