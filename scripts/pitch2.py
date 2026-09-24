#!/usr/bin/env python3
"""F0 via autocorrelation + harmonic product spectrum (mono 16k wav)."""
import wave, struct, sys
import numpy as np

def analyze(path, win=4096, hop=1024):
    w = wave.open(path, 'rb')
    sr = w.getframerate()
    n = w.getnframes()
    raw = w.readframes(n)
    x = np.frombuffer(raw, dtype='<i2').astype(np.float64)
    ac_f0s, hps_f0s = [], []
    for st in range(0, n - win, hop):
        seg = x[st:st+win]
        seg = seg - seg.mean()
        energy = float((seg**2).sum())
        if energy < 1e6:
            continue
        # --- autocorrelation ---
        ac = np.correlate(seg, seg, 'full')[win-1:]
        ac /= ac[0]
        lo, hi = int(sr/300), int(sr/45)   # 45..300 Hz
        peak = int(np.argmax(ac[lo:hi])) + lo
        if ac[peak] > 0.30:
            ac_f0s.append(sr / peak)
        # --- HPS ---
        spec = np.abs(np.fft.rfft(seg * np.hanning(win)))
        hps = spec.copy()
        for m in range(2, 6):
            hps[:len(spec)//m] *= spec[::m][:len(spec)//m]
        fmin, fmax = 45, 300
        kmin, kmax = int(fmin*win/sr), int(fmax*win/sr)
        k = int(np.argmax(hps[kmin:kmax])) + kmin
        hps_f0s.append(k * sr / win)
    return ac_f0s, hps_f0s

def report(path):
    ac, hp = analyze(path)
    def st(f0s):
        f0s = np.array(sorted(f0s))
        if len(f0s) == 0: return None
        return f0s[len(f0s)//2], f0s[len(f0s)//10], f0s[9*len(f0s)//10], len(f0s)
    for name, arr in (("AC", ac), ("HPS", hp)):
        s = st(arr)
        if s:
            med, lo, hi, c = s
            print(f"  {name}: median {med:.1f} Hz (10-90%: {lo:.1f}-{hi:.1f}, n={c})")
        else:
            print(f"  {name}: none")

if __name__ == '__main__':
    report(sys.argv[1])
