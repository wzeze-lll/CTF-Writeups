#include <stdio.h>

int main() {
    char key[] = "Qsw3sj_lz4_Ujw@l";

    for (int i = 0; key[i] != '\0'; i++) {
        int x = key[i];

        if (x >= 'A' && x <= 'Z')
            x = (x - 65 - 14 + 26) % 26 + 65;
        else if (x >= 'a' && x <= 'z')
            x = (x - 97 - 18 + 26) % 26 + 97;

        printf("%c", x);
    }

    return 0;
}