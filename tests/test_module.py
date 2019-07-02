from unittest import TestCase

from common.function2commandline import edit_parser_by_func, fun_to_cml


def simple_sum(a, b):
    return a + b


def sum_with_default(a, b=4):
    return a + b


def sum_with_documantation(a, b=4):
    """
    summarize a & b
    :param a: is a
    :param b: is b
    :return:
    """
    return a + b


def multi_with_documantation(a, b=4):
    """
    multiply a & b
    :param a: is a
    :param b: is b
    :return:
    """
    return a * b


class TestF2cml(TestCase):
    def test_f2cml(self):
        parser = edit_parser_by_func(simple_sum)
        args = parser.parse_args(['4', '5'])
        self.assertEqual(args.a, '4', 'should be 4')
        self.assertEqual(args.b, '5', 'should be 5')
        parser = edit_parser_by_func(sum_with_default)
        args = parser.parse_args(['4', '--b', '5'])
        self.assertEqual(args.a, '4', 'should be 4')
        self.assertEqual(args.b, '5', 'should be 5')
        args = parser.parse_args(['3'])
        self.assertEqual(args.a, '3', 'should be 3')
        self.assertEqual(args.b, 4, 'should be 4')


class TestFun_to_cml(TestCase):
    def test_func_to_cml(self):
        self.assertEqual(fun_to_cml(simple_sum, ['4', '5']), 9)


if __name__ == '__main__':
    import sys
    sys.path.append(r'C:\Users\chaimb\PycharmProjects\function2commandline')
    from common.function2commandline import fun_to_cml
    print fun_to_cml(sum_with_documantation)