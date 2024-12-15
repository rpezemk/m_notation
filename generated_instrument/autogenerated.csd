
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

gihandle OSCinit 8015; global def

gSpath init "" ; ; global def

; EO GLOBAL VARIABLES

;  INSTRUMENTS



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
            ktrig metro 5
            kprevTrig init 0
            if ktrig == 1 && kprevTrig == 0 then
                kvalue = 1 - kvalue
            endif
            OSCsend kvalue, "", 8012, "/heartbeat", "i", kvalue
            kprevTrig = ktrig
        
    endin


    ; I_NAME: TAPE_NOISE 
    ; INSTR_NO: 12 
    instr 12

            aNoise rand -1, 1           
            aOut = aNoise * 0.002
            outs aOut, aOut             
        
    endin


    ; I_NAME: FILE_PLAYER 
    ; INSTR_NO: 39 
    instr 39

        Spath strcpy gSpath
        a_L, a_R diskin2 Spath, 1
        outs a_L, a_R    
        
    endin


    ; I_NAME: FIRE_FILE_PLAY 
    ; INSTR_NO: 15 
    instr 15

        kf1 init 0
        kino init 0
        kfdur init 0.1
        koffset init 0
        Spath init ""
        km  OSClisten gihandle, "/playfile", "iffs", kino, kfdur, koffset, Spath
        if (km != 0) then
            printks "Spath: %s\n", 0, Spath
            gSpath strcpyk Spath
            printks "gSpath: %s\n", 0, gSpath
            event "i", kino, 0, kfdur, koffset
        endif
    
    endin


;  EO INSTRUMENTS
</CsInstruments>
<CsScore>

  ; ################# INSTR_NO: 7 ####################
  i 7   0  7200 ;
  
  ; ################# INSTR_NO: 9997 ####################
  i 9997   0  7200 ;
  
  ; ################# INSTR_NO: 9999 ####################
  i 9999   0  7200 ;
  
  ; ################# INSTR_NO: 12 ####################
  i 12   0  7200 ;
  
  ; ################# INSTR_NO: 15 ####################
  i 15   0  7200 ;
  
</CsScore>
</CsoundSynthesizer>