# -*- coding: utf-8 -*-
import collections

class DistinctError(Exception):

    def __init__(self, key, value):
        self.key = key
        self.vale = value
    def __str__(self):        # エラーメッセージ
        return 'ERROR value duplicate key = "%s", value = "%s"' % (self.key, self.vale)

# 辞書を継承
class distinctdict(dict):

    def __setitem__(self, key, value):
        for existing_key, existing_value in self.items():
            if existing_value == value and existing_key != key:
                raise DistinctError(key, value)

        super(distinctdict, self).__setitem__(key, value)

my = distinctdict()
my['key'] = 'value'
try:
    my['other_key'] = 'value'
except DistinctError as inst:
    print(inst)  # __str__で引数を表示

my['other_key'] = 'value2'
print(my)

# リストを継承
class folder(list):

    def __init__(self, name):
        super(folder, self).__init__()
        self.name = name

    def dir(self):  # @ReservedAssignment
        print('I am the %s foler:' % self.name)
        for element in self:
            print(element)

the = folder('sercret')
the.append('pics')
the.append("videos")
the.dir()


class ListBasedSet(collections.Set):

    ''' Alternate set implementation favoring space over speed
        and not requiring the set elements to be hashable. '''
    def __init__(self, iterable):
        self.elements = lst = []
        for value in iterable:
            if value not in lst:
                lst.append(value)
    def __iter__(self):
        return iter(self.elements)
    def __contains__(self, value):
        return value in self.elements
    def __len__(self):
        return len(self.elements)

s1 = ListBasedSet('abcdef')
s2 = ListBasedSet('defghi')
print(s1)
for el in s1:
    print(el)
print(s2)
for el in s2:
    print(el)

overlap = s1 & s2  # The __and__() method is supported automatically
print(overlap)
for el in overlap:
    print(el)
