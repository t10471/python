# -*- coding: utf-8 -*-
#オブジェクトを再帰的にもてるように作成したクラス
#chain of responseibilityも似ているが
#chain of responseibilityはリストに近いがこっちは、もう少し複雑な構造

class OrganizationEntry(object):


    def __init__(self, code, name):
        self.code = code
        self.name = name


    def getCode(self):
        return self.code


    def getName(self):
        return self.name

    def dump(self):
        print self.code + ":" + self.name



class Group(OrganizationEntry):
    def __init__(self, code, name):
        super(Group, self).__init__(code, name)
        self.entries = []


    def add(self, entry):
        self.entries.append(entry)

    def dump(self):
        super(Group, self).dump()
        for entry in self.entries:
            entry.dump()




class Employee(OrganizationEntry):

    def __init__(self, code, name):
        super(Employee, self).__init__(code, name)


    def add(self, entry):
        raise Exception('method not allowed')

if __name__ == "__main__":
    root_entry = Group(u"001", u"本社")
    root_entry.add(Employee(u"00101", u"CEO"))
    root_entry.add(Employee(u"00102", u"CTO"))

    group1 = Group(u"010", u"○○支店")
    group1.add(Employee(u"01001", u"支店長"))
    group1.add(Employee(u"01002", u"佐々木"))
    group1.add(Employee(u"01003", u"鈴木"))
    group1.add(Employee(u"01003", u"吉田"))

    group2 = Group(u"110", u"△△営業所")
    group2.add(Employee(u"11001", u"川村"))
    group1.add(group2)
    root_entry.add(group1)

    group3 = Group(u"020", u"××支店")
    group3.add(Employee(u"02001", u"萩原"))
    group3.add(Employee(u"02002", u"田島"))
    group3.add(Employee(u"02002", u"白井"))
    root_entry.add(group3)

    root_entry.dump()