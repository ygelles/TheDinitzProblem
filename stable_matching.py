class Man:
    def __init__(self, id: int, ranking: list):
        self.id = id
        self.rejected = True
        self.out_of_the_game = False if ranking else True
        self.ranking = ranking
        self.index = 0
        self.woman_to_rank = {woman: rank for rank, woman in enumerate(ranking)}


class Woman:
    def __init__(self, id: int, ranking: list):
        self.id = id
        self.man = None
        self.ranking = ranking
        self.man_to_rank = {man: rank for rank, man in enumerate(ranking)}

    def preferred(self, man):
        if self.man is None:
            return True
        return self.man_to_rank[man] < self.man_to_rank[self.man]


def propose(man, woman):
    if woman.preferred(man.id):
        rejected = woman.man  # may be None
        woman.man = man.id
    else:
        rejected = man.id
    return rejected


# Gale–Shapley algorithm, time complexity: O(|men| * |women|)
def find_stable_matching(men: list, women: list):
    _men = [Man(id, ranking) for id, ranking in enumerate(men)]
    _women = [Woman(id, ranking) for id, ranking in enumerate(women)]

    change = True
    while change:
        change = False
        for man in _men:
            if (not man.rejected) or man.out_of_the_game:
                continue
            change = True  # there are still rejected men that not leave the game
            rejected_man = propose(man, _women[man.ranking[man.index]])
            man.rejected = False
            if rejected_man is not None:
                _men[rejected_man].rejected = True
            man.index += 1
            if man.index == len(man.ranking):  # leave the game
                man.out_of_the_game = True

    # validation:
    #   matching
    matches = 0
    for man in _men:
        if not man.rejected:
            assert _women[man.ranking[man.index - 1]].man == man.id
            matches += 1
    for woman in _women:
        if woman.man is not None:
            matches -= 1
    assert matches == 0
    #   stable
    for man in _men:
        for not_selected_woman in range(man.index - 1):  # is always stable if the index of not selected woman is bigger
            assert not _women[man.ranking[not_selected_woman]].preferred(man.id)
        if man.rejected and man.index:
            assert not _women[man.ranking[man.index - 1]].preferred(man.id)

    return [(woman.man, woman.id) for woman in _women if woman.man is not None]


if __name__ == '__main__':
    a = [0, 2]
    b = [2, 3, 1]
    c = [0, 3]
    d = [0]
    men = [a, b, c, d]

    A = [2, 3, 0]
    B = [1]
    C = [0, 1]
    D = [2, 1]
    women = [A, B, C, D]

    print(find_stable_matching(men, women))
