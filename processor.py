import re


def similar_words_to_numbers():
    return {'for': 'four',
            'to': 'two',
            'at': 'eight',
            'or': 'all',
            'not': 'zero'}


def adjust_similar_words(x: str, words):
    elements = x.split(' ')

    for i in range(len(elements)):
        try:
            elements[i] = words[elements[i]]
        except KeyError:
            pass

    return ' '.join(elements)


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
    def __init__(self, similar_words=None):
        self.penalty_pattern = re.compile(
            r".*(time \w+|stop go \w+|go away|run) (number [zero|one|two|three|four|five|six|seven|eight|nine ]+)")

        self.clear_all_pattern = re.compile('.*people you can go')
        self.clear_time_pattern = re.compile(
            '.*you can go time ([zero|one|two|three|four|five|six|seven|eight|nine ]+)')
        self.clear_pattern = re.compile(
            '.*you can go ([zero|one|two|three|four|five|six|seven|eight|nine ]+)')

        self.restart_pattern = re.compile(r".*people go again")
        self.next_pattern = re.compile(r".*people go next")
        self.enter_pattern = re.compile(r"open open")
        self.escape_pattern = re.compile(r".*escape escape")
        self.similar_words = similar_words

    def get(self, x):
        if self.similar_words is not None:
            x = adjust_similar_words(x, self.similar_words)

        penalty_match = self.penalty_pattern.match(x)

        if penalty_match is not None:
            penalty = penalty_match.group(1)
            car_number = penalty_match.group(2)
            return self._process_penalty(penalty, car_number)

        clear_time_match = self.clear_time_pattern.match(x)

        if clear_time_match is not None:
            command = clear_time_match.group(1)
            return self._clear_time(command)

        clear_match = self.clear_pattern.match(x)

        if clear_match is not None:
            command = clear_match.group(1)
            return self._clear(command)

        if self.clear_all_pattern.match(x):
            return self._clear_all()

        if self.restart_pattern.match(x) is not None:
            return self._restart_command()

        if self.next_pattern.match(x) is not None:
            return self._next_command()

        if self.enter_pattern.match(x) is not None:
            return self._hit_enter()

        if self.escape_pattern.match(x) is not None:
            return self._hit_escape()

        return None

    @staticmethod
    def _clear_all():
        return '/clear_all'

    @staticmethod
    def _clear_time(x):
        numbers = list(map(text_to_number, x.split(' ')))
        if -1 in numbers:
            raise InvalidAdminCommand
        car = numbers_to_text(numbers)

        return '/cleartp {}'.format(numbers_to_text(car))

    @staticmethod
    def _clear(x):
        numbers = list(map(text_to_number, x.split(' ')))
        if -1 in numbers:
            raise InvalidAdminCommand
        car = numbers_to_text(numbers)

        return '/clear {}'.format(numbers_to_text(car))

    @staticmethod
    def _next_command():
        return '/next'

    @staticmethod
    def _restart_command():
        return '/restart'

    @staticmethod
    def _hit_enter():
        return '\n'

    @staticmethod
    def _hit_escape():
        return chr(27)

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
