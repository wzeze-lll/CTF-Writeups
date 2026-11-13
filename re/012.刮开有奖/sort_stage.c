#include <stdio.h>

int sub_4010F0(int *a1, int a2, int a3)
{
    int result;
    int i;
    int v5;
    int v6;

    result = a3;

    for (i = a2; i <= a3; a2 = i)
    {
        v5 = i;              // 原来是 4 * i
        v6 = a1[i];          // 原来是 *(_DWORD *)(4*i+a1)

        if (a2 < result && i < result)
        {
            do
            {
                if (v6 > a1[result])
                {
                    if (i >= result)
                        break;

                    ++i;

                    a1[v5] = a1[result];

                    if (i >= result)
                        break;

                    while (a1[i] <= v6)
                    {
                        if (++i >= result)
                            goto LABEL_13;
                    }

                    if (i >= result)
                        break;

                    v5 = i;

                    a1[result] = a1[i];
                }

                --result;

            } while (i < result);
        }

    LABEL_13:

        a1[result] = v6;
        sub_4010F0(a1, a2, i - 1);
        result = a3;
        ++i;
    }
    return result;
}
int main(void)
{
    int a[] = {
        90, 74, 83, 69, 67,
        97, 78, 72, 51, 110, 103
    };
    sub_4010F0(a, 0, 10);
    for (int i = 0; i < 11; i++)
    {
        printf("%c", a[i]);
    }
    printf("\n");
    return 0;
}