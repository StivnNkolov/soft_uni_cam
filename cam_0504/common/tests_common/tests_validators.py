from django import test as django_tests
from django.core.exceptions import ValidationError

from common.validators import only_letters_validator, LettersNumbersWhitespacesValidator


class OnlyLettersValidatorTests(django_tests.TestCase):

    def test_value_contains_only_letters_return_None(self):
        value = 'test'

        return_value = only_letters_validator(value)

        self.assertIsNone(return_value)

    def test_value_contains_only_letters_and_number__raises_and_return_message(self):
        value = 'test2'
        return_message = 'The value must consist of only letters!'

        with self.assertRaises(ValidationError) as ex:
            only_letters_validator(value)

        self.assertEqual(return_message, ex.exception.message)

    def test_value_contains_only_letters_and_symbols__raises_and_return_message(self):
        value = 'test.'
        return_message = 'The value must consist of only letters!'

        with self.assertRaises(ValidationError) as ex:
            only_letters_validator(value)

        self.assertEqual(return_message, ex.exception.message)

    def test_value_contains_only_letters_and_white_space__raises_and_return_message(self):
        value = 'test '
        return_message = 'The value must consist of only letters!'

        with self.assertRaises(ValidationError) as ex:
            only_letters_validator(value)

        self.assertEqual(return_message, ex.exception.message)

    def test_value_is_empty_string__raises_and_return_message(self):
        value = ''
        return_message = 'The value must consist of only letters!'

        with self.assertRaises(ValidationError) as ex:
            only_letters_validator(value)

        self.assertEqual(return_message, ex.exception.message)


class LettersNumbersWhitespacesValidatorTests(django_tests.TestCase):
    REGEX_PATTERN = '(?<![\s\W\D])^([a-zA-Z0-9]+[\s]?[a-zA-Z0-9]+)+$(?![\s\W\D])'

    def test__value_contains_only_letters__return_None(self):
        value = 'test'

        validator = LettersNumbersWhitespacesValidator(self.REGEX_PATTERN)

        self.assertIsNone(validator(value))

    def test__value_contains_only_numbers__return_None(self):
        value = '222'

        validator = LettersNumbersWhitespacesValidator(self.REGEX_PATTERN)

        self.assertIsNone(validator(value))

    def test__value_contains_letters_and_numbers__return_None(self):
        value = 'test222'

        validator = LettersNumbersWhitespacesValidator(self.REGEX_PATTERN)

        self.assertIsNone(validator(value))

    def test__value_contains_letters_numbers_and_white_spaces__return_None(self):
        value = 'test 222'

        validator = LettersNumbersWhitespacesValidator(self.REGEX_PATTERN)

        self.assertIsNone(validator(value))

    def test_value_contains_only_white_space_raises(self):
        value = ' '

        validator = LettersNumbersWhitespacesValidator(self.REGEX_PATTERN)

        with self.assertRaises(ValidationError) as ex:
            validator(value)

        self.assertIsNotNone(ex.exception)

    def test_value_contains_letters_and_symbols_raises(self):
        value = 'asaaa.'

        validator = LettersNumbersWhitespacesValidator(self.REGEX_PATTERN)

        with self.assertRaises(ValidationError) as ex:
            validator(value)

        self.assertIsNotNone(ex.exception)

    def test_value_contains_numbers_and_symbols_raises(self):
        value = '222.'

        validator = LettersNumbersWhitespacesValidator(self.REGEX_PATTERN)

        with self.assertRaises(ValidationError) as ex:
            validator(value)

        self.assertIsNotNone(ex.exception)

    def test_value_contains_whitespaces_and_symbols_raises(self):
        value = ' @'

        validator = LettersNumbersWhitespacesValidator(self.REGEX_PATTERN)

        with self.assertRaises(ValidationError) as ex:
            validator(value)

        self.assertIsNotNone(ex.exception)

    def test_invalid_value_raises_and_return_the_message(self):
        value = 'asaaa.'
        ex_message = 'Name can consist of letters, whitespaces and numbers. "Tomato soup"'

        validator = LettersNumbersWhitespacesValidator(self.REGEX_PATTERN)

        with self.assertRaises(ValidationError) as ex:
            validator(value)

        self.assertEqual(ex_message, ex.exception.message)
