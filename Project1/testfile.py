class A:
    a = 0;

    def __init__(self, input):
        A.a = input;



def main():
    B = A(123);
    C = A(234);
    print(A.a, B.a, C.a);



main();
