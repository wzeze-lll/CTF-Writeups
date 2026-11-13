 #include <stdio.h>
 int main() {
    char x[] = "dd2940c04462b4dd7c450528835cca15";
    x[2] = (char) ((x[2] + x[3]) - 50);
    x[4] = (char) ((x[2] + x[5]) - 48);
    x[30] = (char) ((x[31] + x[9]) - 48);
    x[14] = (char) ((x[27] + x[28]) - 97);
    for (int i = 0; i < 16; i++) {
                        char a = x[31 - i];
                        x[31 - i] = x[i];
                        x[i] = a;
                    }
    printf("%s\n", x);
    return 0;
}