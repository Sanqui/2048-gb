;==============================================================
; SMS defines
;==============================================================
VDPControl EQU $bf
VDPData    EQU $be
VRAMWrite  EQU $4000
CRAMWrite  EQU $c000
VPDStatus  EQU $bf 

im: MACRO
    db $ed
if \1 == 0
    db $46
endc
if \1 == 1
    db $56
endc
if \1 == 2
    db $5e
endc
    ENDM
    
