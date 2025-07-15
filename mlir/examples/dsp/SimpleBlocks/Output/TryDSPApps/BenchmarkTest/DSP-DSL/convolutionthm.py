def main() {
    var a = getRangeOfVector(0, 100, 1);
    var b = getRangeOfVector(0, 100, 2);
    # var a = [1,2,3,4];
    # var b = [2,3,4,5];

    # print(a);

    var ra = padding(a, 0, 99);
    var rb = padding(b, 0, 99);
    
    # print(ra);

    var x1 = fft1dreal(ra);
    var y1 = fft1dimg(ra);
    var x2 = fft1dreal(rb);
    var y2 = fft1dimg(rb);

    # # print(x1);
    # # print(y1);
    # # print(x2);
    # # print(y2);

    var tempreal = x1 * x2;
    var negreal = y1 * y2;
    var imag = x1 * y2 + x2 * y1; # the order matters!
    var real = sub(tempreal, negreal);

    # print(real);
    # print(imag);

    var result = ifft1d(real, imag);
    print(result);

    # var t = FIRFilterResponse(b, a);
    # print(t);
}