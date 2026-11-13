#include <stdio.h>
 
int main()
{
    char key[18]={
        180, 136, 137, 147, 191, 137, 147, 191, 148, 136,
        133, 191, 134, 140, 129, 135, 191, 65 };
        for(int i=0;i<18;i++)
        {
            key[i]=key[i]^0x20-64; 
            printf("%c",key[i]);
        }
    return 0;
}