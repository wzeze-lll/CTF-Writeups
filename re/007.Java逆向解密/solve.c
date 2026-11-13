#include <stdio.h>

int main(void)
{
    const unsigned int key[] = {
        180, 136, 137, 147, 191, 137, 147, 191, 148,
        136, 133, 191, 134, 140, 129, 135, 191, 65
    };
    for (size_t i = 0; i < sizeof(key) / sizeof(key[0]); ++i) {
        putchar((int)((key[i] ^ 0x20U) - 64U));
    }
    putchar('\n');
    return 0;
}
