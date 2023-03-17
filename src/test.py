def p1(fun):
    def p2(var):
        var = var + 2;
        fun(var);
    return p2

@p1
def fun(var):
    print(10*var);


fun(1)