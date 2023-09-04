"""
Simulate drawing lots by a tote and check the incidence of getting at least two adjacent numbers in a draw
"""

import random


def decorator(classname):
    class Wrapper:
        diffs = []
        
        def __init__(self, *args) -> None:
            self.wrapped = classname(*args)
            
        def __getattr__(self, name):
            return getattr(self.wrapped, name)
        
        def analyse(self):
            res = self.wrapped.analyse()
            self.diffs.append(self.wrapped.lowest_diff)
            return res
    
    def summary():
        total_len = len(Wrapper.diffs)
        adjacent_total = len(list(filter(lambda x: x == 1, Wrapper.diffs)))
        res = adjacent_total / total_len * 100
        print('Liczby sąsiednie wystąpiły w {0:.2f} % losowań.'.format(res))
        
    Wrapper.summary = summary

    return Wrapper

@decorator
class Tote:
    range_from = 0
    range_to = 49
    winning_set_count = 6
    lowest_diff = -1
    
    def draw_lots(self):
        self.winning_set = random.sample(range(self.range_from, self.range_to+1), k=self.winning_set_count)
        
    def analyse(self):
        lowest_diff = self.range_to
        for (i, val) in enumerate(self.winning_set):
            diffs = [abs(val - v) for (k, v) in enumerate(self.winning_set) if k != i]
            lowest_diff = min(diffs) if min(diffs) < lowest_diff else lowest_diff            
        self.lowest_diff = lowest_diff

def run_simulation():
    for _ in range(100000):
        t = Tote()
        t.draw_lots()
        t.analyse()
        
    Tote.summary()
    
if __name__ == '__main__':
    run_simulation()