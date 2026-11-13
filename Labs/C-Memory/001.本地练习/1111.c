#include <stdio.h>
int main()
{
    unsigned char s[] = {
        0x69, 0x63, 0x75, 0x67,
        0x60, 0x6F, 0x66, 0x7F
    };
    printf("GXY{do_not_");
    for (int i = 0; i < 8; i++)
    {
        if (i % 2 == 1)
            s[i] -= 2;
        else
            s[i] -= 1;

        printf("%c", s[i]);
    }
    printf("\n");
    return 0;
}