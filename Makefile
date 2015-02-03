#gawk sort order
export LC_CTYPE=C

.SUFFIXES: .asm .o .gb

all: 2048.gb

2048.o: 2048.asm
	rgbasm -p 0xff -o 2048.o 2048.asm

2048.gb: 2048.o
	rgblink -p 0xff -n 2048.sym -m $*.map -o $@ $<
	rgbfix -p 0xff -jv -i XXXX -k XX -l 0x33 -m 0x03 -p 0 -r 1 -t "2048-gb        " $@

clean:
	rm -f 2048.o 2048.gb
