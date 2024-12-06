
<CsoundSynthesizer>
<CsOptions>
-odac
</CsOptions>
<CsInstruments>
sr = 44100
ksmps = 32
nchnls = 2
0dbfs = 1
;  GLOBAL VARIABLES

gihandle OSCinit 8002

; EO GLOBAL VARIABLES

;  INSTRUMENTS



    ; I_NAME: test_instr 
    ; INSTR_NO: 1 
    instr 1

        a1 oscili 0.5, 440
        outs 0.07*a1, 0.07*a1
        event_i "i", 2, 60, p3
        
    endin


    ; I_NAME: beep_instr 
    ; INSTR_NO: 13 
    instr 13

        a1 oscili 0.5, 4*440
        outs 0.1*a1, 0.1*a1
        
    endin


    ; I_NAME: exit_instr 
    ; INSTR_NO: 997 
    instr 997

        exitnow;
        
    endin


    ; I_NAME: OSC_METRO 
    ; INSTR_NO: 7 
    instr 7

        kf1 init 0
        kino init 0
        kfdur init 0.1

        km  OSClisten gihandle, "/metro", "if", kino, kfdur
        if (km != 0) then
            printks "QUITTING\n", 0
            event "i", kino, 0, kfdur
        endif
    
    endin


    ; I_NAME: OSC_PANIC 
    ; INSTR_NO: 9997 
    instr 9997

        kk  OSClisten gihandle, "/panic", ""
        if (kk != 0) then
            printks "QUITTING\n", 0
            event "i", 997, 0, p3
        endif
    
    endin


    ; I_NAME: HEARTBEAT 
    ; INSTR_NO: 9999 
    instr 9999

            ktime init 0
            kvalue init 0

            ; Toggle the value between 0 and 1
            if ktime > 1 then
                kvalue = 1
                ktime = 0
            else
                kvalue = 0
            endif

            OSCsend 1, "", 8012, "/heartbeat", "i", 1

            ; Increment time counter
            ktime = ktime + 0.01
        
    endin


;  EO INSTRUMENTS
</CsInstruments>
<CsScore>

  ; ################# INSTR_NO: 1 ####################
  i 1   0  7200 ;
  
  ; ################# INSTR_NO: 7 ####################
  i 7   0  7200 ;
  
  ; ################# INSTR_NO: 9997 ####################
  i 9997   0  7200 ;
  
  ; ################# INSTR_NO: 9999 ####################
  i 9999   0  7200 ;
  
</CsScore>
</CsoundSynthesizer>