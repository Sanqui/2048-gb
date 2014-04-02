#gawk sort order
export LC_CTYPE=C

.SUFFIXES: .asm .o .sms

all: 2048.sms

2048.o: 2048.asm
	cat 2048.asm | python gbtoz80.py > 2048.tx
	rgbasm -o 2048.o 2048.tx

2048.sms: 2048.o
	rgblink -n 2048.sym -m $*.map -o $@ $<
	rgbfix -jv -i XXXX -k XX -l 0x33 -m 0x01 -p 0 -r 0 -t 2048 $@

clean:
	rm -f 2048.o 2048.sms
