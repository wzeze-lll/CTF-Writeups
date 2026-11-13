CC ?= gcc
CFLAGS ?= -static -s -O2 -Wall -Wextra
TARGET = exploit

all: $(TARGET)

$(TARGET): exploit.c
	$(CC) $(CFLAGS) -o $(TARGET) exploit.c

musl: exploit.c
	x86_64-gentoo-linux-musl-gcc -static -s -Os -o $(TARGET) exploit.c

clean:
	rm -f $(TARGET)

.PHONY: all clean musl
