#gawk sort order
export LC_CTYPE=C

.SUFFIXES: .asm .o .gb

all: 2048.gb

2048.o: 2048.asm
	rgbasm -o 2048.o 2048.asm

2048.gb: 2048.o
	rgblink -n 2048.sym -m $*.map -o $@ $<
	rgbfix -jv -i XXXX -k XX -l 0x33 -m 0x01 -p 0 -r 0 -t 2048 $@

clean:
	rm -f 2048.o 2048.gb
