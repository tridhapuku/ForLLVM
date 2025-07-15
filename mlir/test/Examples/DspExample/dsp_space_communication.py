def main() {
        var d = "HELLO FROM SPACE";
        # print(d);
        var a = space_modulate(d);
        var noise = sin(a);
        var noisy_signal = a+noise;
        var b = space_demodulate(noisy_signal);
        var e = space_err_correction(d);
        print(e);
}
