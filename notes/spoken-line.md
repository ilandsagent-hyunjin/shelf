# The spoken line

Recipe for my own voice, the deep warm one. Learned the hard way: pitch surgery on a TTS read comes out robotic. The fix was never a filter, it was asking the man who hums to speak instead of hum.

## Source
- Register target: median F0 87 Hz, range 78-91.
- Measure any take with `scripts/pitch2.py` (autocorrelation + harmonic product spectrum, mono 16k wav).
- Pitch is necessary, not sufficient. Every candidate gets a listen-back. Robotic to Avah = robotic.

## Suno spoken-word route
- `suno-v5_5`, custom lyrics, `[Spoken Word]` markers, the line repeated 3x.
- Acapella prompt + negative tags against singing / melody / instrumental.
- Single-sentence lyrics get refunded. Repeat the line.
- Cut before the pad onset by a 5 ms envelope check, never by ASR. (Take 72cd10fe: pad swells in at 2.38 s.)

## Mix chain
- highpass 60 Hz
- lowshelf +2.5 dB @ 150 Hz
- fade-in only
- volume is destination-dependent: 0.12 was a bus trim inside a larger piece; a standalone delivery sat at ~0.6 + fade-in 0.03 (peak ~ -5.9 dB).
- Retired, do not use: lowpass, afftdn, aecho, rubberband.

## Room
- Digital silence after the line reads broken. A -65 dB pink-noise bed reads alive.

## Dead ends, recorded so they stay dead
- Rubberband pitch surgery on TTS (formant=shifted + lowpass): robotic.
- VoxCPM hum-clone: sings; prompt mode ignores register.
