class T(object):
    a = 0


class A(T):
    pass

class B(T):
    a = 2


class C(B, A):
    def __init__(self):
        super(C, self).__init__()
    pass

c = C()
print c.a
print super(C, c).a