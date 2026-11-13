#include <stdio.h>
#include <unistd.h>
int main() {
    char buf[100] = {0};
    read(0, buf, 99);
    printf(buf);
    return 0;
}