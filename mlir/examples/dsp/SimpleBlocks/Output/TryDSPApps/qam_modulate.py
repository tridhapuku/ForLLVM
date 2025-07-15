def main() {
    var input_data = [0,1,1,0,1,1,1,0];
    # print(input_data);
    var real = qam_modulate_real(input_data);
    var imagine = qam_modulate_imagine(input_data);
    print(real);
    print(imagine);
    # var real_part = [1, 1, 1, 1];
    # var img_part = [1, -1, 1, -1];
    # var decoded_data = qam_demodulate(real_part, img_part);
    # print(decoded_data);
}
