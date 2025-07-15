def main() {
    # var input_data = [1,1,1,0,1,1,1,0];
    # print(input_data);
    # var modulated_symbols = qam_modulate(input_data);
    # print(modulated_symbols);
    var real_part = [1, 1, 1, 1];
    var img_part = [1, -1, 1, -1];
    var decoded_data = qam_demodulate(real_part, img_part);
    print(decoded_data);
}
