from collections import deque
import statistics


# todo: optimize this so that it doesn't re-sort the list on every function call. Don't use for large values of
# max_elements :)
class StatTracker(object):
    def __init__(self, max_elements: int):
        self.max_elements = max_elements

        self.values = deque([], maxlen=max_elements)

    def track(self, element: float) -> None:
        self.values.append(element)

    def median(self, default=None) -> float:
        if not self.values and default:
            return default

        return statistics.median(self.values)

    def size(self):
        return len(self.values)

    def mean(self, default=None):
        if not self.values and default:
            return default

        return statistics.mean(self.values)

    def sorted_values(self):
        return sorted(self.values)

    def quartile(self, q: float, default=None):
        assert 0.0 <= q <= 1.0

        # todo: these two lines are copied across three functions. Refactor to get rid of duplication.
        if not self.values and default:
            return default

        idx = int(q * len(self.values))

        return self.sorted_values()[idx]

    def probability_of_being_lower(self, num) -> float:
        """
        Computes the probability that the next statistics to be tracked is less than or equal to the given number,
        computed based on the previously recorded values.
        :param num:
        :return:
        """
        return len([x for x in self.values if x <= num]) / len(self.values)
