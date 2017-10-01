import json


class TranslationCosts(object):
    def __init__(self, money=0, time=0):
        self.time = time
        self.money = money

    def to_json(self):
        return json.dumps({
            'time': self.time,
            'money': self.money
        })