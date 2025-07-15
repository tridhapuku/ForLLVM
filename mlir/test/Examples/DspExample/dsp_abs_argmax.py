def main() {
        # var time = [0.0, -0.25, 0.5, -0.75, 1.0];
        var time = getRangeOfVector(0, 100, 0.01);
        var antennas = 4;
        var freq = 5;
        var weights = [1, 7, 6, -7];

        var signal = beam_form(antennas, freq, time, weights);
        var abs_signal = abs(signal);
        var power_abs_signal= abs_signal * abs_signal;
        var max_power_angle_idx = argmax(signal, 0);

        print(max_power_angle_idx);
}
