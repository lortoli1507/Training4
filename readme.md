vector_sequence_28.py     Outputs a simple square wave on Sig #1.  Duty cycle is always 50%, and period is (2 x tbvalue); tbvalue defaults to 0.125 (sec), but may be adjusted by using New Timebase fill-in field and CH TB pushbutton.  Sig's 2 and 3 are controlled by a set of vectors contained in a 2D array, vectors[], which is -- for the time being -- hardcoded.  The "wait" (or "hold") time for each vector is (multiplier x stddelay), with stddelay being set to 0.200 (sec) in code.  The signal on which each vector causes a transition is specified by sig#.
   vectors = [ [multiplier, sig#],
               [multiplier, sig#],
               [multiplier, sig#],
               [multiplier, sig#] ]
If the code is run as-is, the vectors will be applied continuously in an infinite loop; they may be appplied once ("single-shot mode") by removing the while statement at Line 125.  Note that removing the while statement requires that one level of indent be removed from Lines 126 - 130.  Signal 1 can be turned ON/OFF using the pushbuttons labeled CH1 ON and CH1 OFF; Sig's 2 and 3 are controlled (independently from Sig #1) using CH2 ON and CH2 OFF.
