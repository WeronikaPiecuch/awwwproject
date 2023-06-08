#include <8052.h>
 

 
/* This is a simple delay based on a busy loop 
 with a 22.1184 MHz crystal, the delay lasts 
 for approximately 1 ms times the number passed 
 Of course, it will take longer if there are 
 interrupts occuring... */

void delay_ms(unsigned char ms)
{
        ms;
        __asm
        mov     r0, dpl
00001$: mov     r1, #230
00002$: nop
        nop
        nop
        nop
        nop
        nop
        djnz    r1, 00002$
        djnz    r0, 00001$
        ret
        __endasm;
}

void main(void)
{
    while(1)
    {
        P1 = 0xFF; // Turn ON all LED's connected to Port1
        delay_ms(10);
        P1 = 0x00; // Turn OFF all LED's connected to Port1
        delay_ms(10);
    }
}