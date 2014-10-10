# -*- coding: utf-8 -*-

#戦略を分ける


#Componentクラスに相当する

class OrganizationEntry(object):

    def __init__(self, code, name):
        self.code = code
        self.name = name


    def getCode(self):
        return self.code


    def getName(self):
        return self.name


    #組織ツリーを表示する
    #サンプルでは、デフォルトの実装を用意
    def accept(self, visitor):
        visitor.visit(self)

class Group(OrganizationEntry):

    def __init__(self, code, name):
        super(Group, self).__init__(code, name)
        self.entries = []

    #子要素を追加する
    def add(self, entry):
        self.entries.append(entry)

    #子要素を取得する
    def getChildren(self):
        return self.entries


#Leafクラスに相当する
class Employee( OrganizationEntry):

    def __init__(self, code, name):
        super(Employee, self).__init__(code, name)

    #子要素を追加する
    #Leafクラスは子要素を持たないので、例外を発生させている
    def add(self, entry):
        raise Exception, 'method not allowed'

    def getChildren(self):
        return []



class DumpVisitor(object):
    def visit(self, entry):
        if entry.__class__.__name__ == 'Group':
            h = '■'
        else:
            h = '  '

        print h + entry.getCode() + ":" + entry.getName()
        for   ent in entry.getChildren():
            ent.accept(self)

class CountVisitor(object):

    def __init__(self):
        self.group_count = 0
        self.employee_count = 0

    def visit(self, entry):
        if entry.__class__.__name__ == 'Group':
            self.group_count += 1
        else:
            self.employee_count += 1

        for ent in entry.getChildren():
            self.visit(ent)

    def getGroupCount(self):
        return self.group_count

    def getEmployeeCount(self):
        return self.employee_count

if __name__ == "__main__":

    #木構造を作成
    root_entry = Group("001", "本社")
    root_entry.add(Employee("00101", "CEO"))
    root_entry.add(Employee("00102", "CTO"))

    group1 = Group("010", "○○支店")
    group1.add(Employee("01001", "支店長"))
    group1.add(Employee("01002", "佐々木"))
    group1.add(Employee("01003", "鈴木"))
    group1.add(Employee("01003", "吉田"))

    group2 = Group("110", "△△営業所")
    group2.add(Employee("11001", "川村"))
    group1.add(group2)
    root_entry.add(group1)

    group3 = Group("020", "××支店")
    group3.add(Employee("02001", "萩原"))
    group3.add(Employee("02002", "田島"))
    group3.add(Employee("02002", "白井"))
    root_entry.add(group3)


    #木構造をダンプ
    root_entry.accept(DumpVisitor())

    #同じ木構造に対して、別のVisitorを使用する

    visitor = CountVisitor()
    root_entry.accept(visitor)
    print '組織数：' + str(visitor.getGroupCount())
    print '社員数：' + str(visitor.getEmployeeCount())