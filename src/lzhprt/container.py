# -*- coding: UTF-8 -*-
# Public package
import os
# Private package
# Internal package


class Line:
    def __init__(self):
        self.units = []
        self.weights = []

    def add(self, unit, weight=1):
        self.units.append(unit)
        self.weights.append(weight)

    def __repr__(self):
        try:
            total = os.get_terminal_size().columns
        except BaseException:
            total = 80
        temp_iunits = []
        temp_weight = []
        for iunit, unit in enumerate(self.units):
            if (unit.is_dynamic()):
                temp_iunits.append(iunit)
                temp_weight.append(self.weights[iunit])
            else:
                total -= unit.get_length()
        total = max(total, 0)
        use_weight = [int(total * weight / sum(temp_weight)) for weight in temp_weight]
        use_weight[-1] += total - sum(use_weight)
        for iunit, weight in zip(temp_iunits, use_weight):
            self.units[iunit].filler.length = weight
        return ''.join([unit.__repr__() for unit in self.units])
