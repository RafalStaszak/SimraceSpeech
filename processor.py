import re
import os


def text_to_number(x):
    numbers = {'zero': 0, 'one': 1, 'two': 2, 'three': 3, 'four': 4, 'five': 5, 'six': 6, 'seven': 7, 'eight': 8,
               'nine': 9, 'ten': 10, 'fifteen': 15,
               'thirty': 30}
    try:
        return numbers[x]
    except KeyError:
        return -1


def numbers_to_text(x):
    text = ''
    for v in x:
        text += str(v)

    return text


class InvalidAdminCommand(Exception):
    pass


class AdminProcessor:
    def __init__(self):
        self.penalty_pattern = re.compile(
            r".*(time \w+|stop go \w+|go away|run) (number [one|two|three|four|five|six|seven|eight|nine ]+)")
        self.clear_pattern = re.compile(
            r".*command clear (all|time [one|two|three|four|five|six|seven|eight|nine ]+|number [one|two|three|four|five|six|seven|eight|nine ]+)")

        self.restart_pattern = re.compile(r".*command restart")
        self.next_pattern = re.compile(r".*command next")
        self.enter_pattern = re.compile(r".*do it do it")
        self.escape_pattern = re.compile(r".*escape escape")

    def get(self, x):
        penalty_match = self.penalty_pattern.match(x)

        if penalty_match is not None:
            penalty = penalty_match.group(1)
            car_number = penalty_match.group(2)
            return self._process_penalty(penalty, car_number)

        clear_match = self.clear_pattern.match(x)

        if clear_match is not None:
            command = clear_match.group(1)
            return self._process_clear(command)

        if self.restart_pattern.match(x) is not None:
            return self._restart_command()

        if self.next_pattern.match(x) is not None:
            return self._next_command()

        if self.enter_pattern.match(x) is not None:
            return self._hit_enter()

        if self.escape_pattern.match(x) is not None:
            return self._hit_enter()

        return None

    @staticmethod
    def _next_command():
        return '/next'

    @staticmethod
    def _restart_command():
        return '/restart'

    @staticmethod
    def _hit_enter():
        return os.linesep

    @staticmethod
    def _process_penalty(penalty, car_number):
        elements = penalty.split(' ')
        numbers = car_number.split(' ')[1:]
        numbers = list(map(text_to_number, numbers))
        time = text_to_number(elements[-1])

        if -1 in numbers:
            raise InvalidAdminCommand

        car = numbers_to_text(numbers)

        if penalty.startswith('run'):
            return '/dt {}'.format(car)
        elif penalty.startswith('go away'):
            return '/dq {}'.format(car)

        if time == -1:
            raise InvalidAdminCommand

        if penalty.startswith('time'):
            return '/tp{} {}'.format(time, car)
        elif penalty.startswith('stop go'):
            return '/sg{} {}'.format(time, car)

        return None

    @staticmethod
    def _process_clear(command):
        elements = command.split(' ')
        if command.startswith('all'):
            return '/clear_all'

        numbers = elements[1:]
        numbers = list(map(text_to_number, numbers))
        if -1 in numbers:
            raise InvalidAdminCommand

        car = numbers_to_text(numbers)

        if command.startswith('time'):
            return '/clear_tp {}'.format(car)
        elif command.startswith('number'):
            return '/clear {}'.format(car)

        return None
