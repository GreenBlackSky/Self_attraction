from random import randint


class Population(object):
    NUMBER_OF_TRAITS = 10
    NUMBER_OF_VARIANTS = 5
    NUMBER_OF_PEOPLE = 100

    @staticmethod
    def mix(arr1, arr2):
        return [
            val1 if randint(0, 1) == 0 else val2
            for val1, val2 in zip(arr1, arr2)
        ]

    @staticmethod
    def generate():
        return [
            randint(0, Population.NUMBER_OF_VARIANTS)
            for _ in range(Population.NUMBER_OF_TRAITS)
        ]

    class Person(object):
        def __init__(self, mother=None, father=None):
            self.gender = randint(0, 1)
            if mother is not None:
                self.traits = Population.mix(mother.traits, father.traits)
                self.likes = Population.mix(mother.likes, father.likes)
            else:
                self.traits = Population.generate()
                self.likes = Population.generate()

        def rate(self, partner):
            return sum(
                1 if trait == like else 0
                for trait, like in zip(partner.traits, self.likes)
            )/Population.NUMBER_OF_TRAITS

    def __init__(self):
        self.boys = []
        self.girls = []
        self.pairs = []
        for _ in range(Population.NUMBER_OF_PEOPLE):
            person = Population.Person()
            if person.gender == 0:
                self.girls.append(person)
            else:
                self.boys.append(person)

    def match(self):
        table = [
            [
                girl.rate(boy) + boy.rate(girl)
                for boy in self.boys
            ]
            for girl in self.girls
        ]

        while table and table[0]:
            max_val, max_x, max_y = 0, 0, 0
            for y, row in enumerate(table):
                for x, val in enumerate(row):
                    if val > max_val:
                        max_val, max_x, max_y = val, x, y

            self.pairs.append((self.girls[max_y], self.boys[max_x]))
            table.pop(max_y)
            for row in table:
                row.pop(max_x)

        self.girls.clear()
        self.boys.clear()

    def reproduce(self):
        for mother, father in self.pairs:
            if len(self.pairs)*2 < Population.NUMBER_OF_PEOPLE:
                max_number_of_children = 4
            else:
                max_number_of_children = 3

            for _ in range(randint(1, max_number_of_children)):
                child = Population.Person(mother, father)
                if child.gender == 0:
                    self.girls.append(child)
                else:
                    self.boys.append(child)
        self.pairs.clear()

    def average_self_attraction(self):
        return sum(
            person.rate(person)
            for person in self.boys + self.girls
        )/(len(self.boys) + len(self.girls))


def test():
    NUMBER_OF_GENERATIONS = 20
    population = Population()
    start = population.average_self_attraction()
    for _ in range(NUMBER_OF_GENERATIONS):
        population.match()
        population.reproduce()
    end = population.average_self_attraction()
    print(start)
    print(end)


if __name__ == '__main__':
    test()
