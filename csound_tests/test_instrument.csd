<CsoundSynthesizer>
<CsOptions>
; Use appropriate audio output options for your setup
-odac
</CsOptions>

<CsInstruments>

; Initialize the Csound orchestra
sr = 44100
ksmps = 32
nchnls = 2
0dbfs = 1

gihandle OSCinit 8002

    instr 1
        a1 oscili 0.5, 440
        outs 0.02*a1, 0.02*a1
        event_i "i", 2, 60, p3
    endin

    instr 2
        exitnow  ; 
    endin

    instr   1199
        kf1 init 0
        kk  OSClisten gihandle, "/panic", ""
        if (kk != 0) then
            printks "QUITTING\n", 0
            event "i", 2, 0, p3
        endif
    endin

    instr   2099
        kf1 init 0
        kf2 init 0
        kk  OSClisten gihandle, "/panic", "ff", kf1, kf2
        if (kk != 0) then
            printks "QUITTING\n", 0
            event "i", 2, 0, p3
        endif
    endin

</CsInstruments>
<CsScore>
f 2 0 16384 10 1
; i99077  0.01   7200  1        ; UDP OSC LISTENER
i 1 0 20
i 1199    0 20
</CsScore>
</CsoundSynthesizer>
