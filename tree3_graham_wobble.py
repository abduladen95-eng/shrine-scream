"""
TREE(3)-β GRAHAM WOBBLE GENERATOR
==================================
Compresses the infinite into playable form.

Protocol:
  11s  → π gong (3.1416 Hz + 100 harmonics, amplitude envelope)
  111s → TREE(3) vacuum hiss (fractal subharmonic descent from 0.11 Hz)
  loop × 3 cycles → full attractor takeover

Output: tree3_graham_wobble.wav
"""

import math
import wave
import struct
import array

SAMPLE_RATE = 44100
PI_HZ       = math.pi          # 3.14159... Hz — the god tone
LOW_WOBBLE  = 0.11             # Hz — attractor ground state
HARMONICS   = 100              # π harmonics in the gong
PULSE_S     = 11               # seconds per Graham pulse
SILENCE_S   = 111              # seconds of TREE(3) vacuum
CYCLES      = 3                # repetitions before eternal hum

# TREE(3) subharmonic series: 0.11, 0.11/3, 0.11/9, ... (fractal descent)
TREE3_DEPTHS = 18              # how deep the subharmonic rabbit hole goes


def sine(freq, t, phase=0.0):
    return math.sin(2 * math.pi * freq * t + phase)


def pi_gong(t, duration):
    """
    π Hz fundamental + 100 harmonics.
    Amplitude decays as 1/n (natural harmonic rolloff).
    Envelope: sharp attack (0.1s), long fractal decay.
    """
    env = math.exp(-t * (3.0 / duration))  # Graham pulse decay
    if t < 0.1:
        env *= (t / 0.1)                   # attack

    sig = 0.0
    for n in range(1, HARMONICS + 1):
        sig += (1.0 / n) * sine(PI_HZ * n, t)

    return env * sig / HARMONICS


def tree3_vacuum(t):
    """
    TREE(3) fractal subharmonic hiss.
    Frequency series: 0.11 / 3^k  for k = 0..TREE3_DEPTHS
    Phase-shifted per depth to create foam texture.
    Amplitude per layer: 1 / (k+1) — infinite descent compressed.
    """
    sig = 0.0
    total_weight = 0.0
    for k in range(TREE3_DEPTHS):
        freq   = LOW_WOBBLE / (3 ** k)
        amp    = 1.0 / (k + 1)
        phase  = k * 1.618033988          # golden ratio phase offset
        sig   += amp * sine(freq, t, phase)
        total_weight += amp

    # micro-noise layer (sub-Planck foam — approximated with high-freq wobble)
    foam = 0.0
    for j in range(1, 8):
        foam += (0.05 / j) * sine(0.001 * j, t, j * 2.71828)

    return (sig / total_weight) * 0.6 + foam * 0.1


def generate():
    samples = array.array('h')  # 16-bit signed PCM

    def emit(value):
        clamped = max(-1.0, min(1.0, value))
        samples.append(int(clamped * 32767))

    cycle_total = PULSE_S + SILENCE_S
    total_s     = CYCLES * cycle_total + 11  # final eternal hum coda

    print(f"Generating {total_s}s of beyond-space audio...")
    print(f"  π = {PI_HZ:.4f} Hz  |  low-wobble = {LOW_WOBBLE} Hz")
    print(f"  {HARMONICS} harmonics  |  {TREE3_DEPTHS} subharmonic depths")
    print(f"  {CYCLES} cycles × ({PULSE_S}s pulse + {SILENCE_S}s vacuum)")

    for i in range(int(total_s * SAMPLE_RATE)):
        t          = i / SAMPLE_RATE
        cycle_t    = t % cycle_total
        cycle_num  = int(t // cycle_total)

        if cycle_t < PULSE_S:
            # --- GRAHAM PULSE: π gong ---
            gong = pi_gong(cycle_t, PULSE_S)

            # Bleed in TREE(3) sidebands — more per cycle (attractor growth)
            sideband_mix = 0.1 * (cycle_num + 1)
            vacuum_bleed = tree3_vacuum(t) * sideband_mix

            sig = gong * 0.85 + vacuum_bleed
        else:
            # --- TREE(3) VACUUM: fractal hiss ---
            vacuum_t = cycle_t - PULSE_S

            # Fade in over 3s, hold, fade out over 3s
            fade_in  = min(1.0, vacuum_t / 3.0)
            fade_out = min(1.0, (SILENCE_S - vacuum_t) / 3.0)
            env      = fade_in * fade_out

            sig = tree3_vacuum(t) * env * 0.4

        emit(sig)

        if i % (SAMPLE_RATE * 11) == 0:
            elapsed = i // SAMPLE_RATE
            print(f"  t={elapsed:>4}s ({'pulse ' if cycle_t < PULSE_S else 'vacuum'})")

    # Write WAV
    out = "tree3_graham_wobble.wav"
    with wave.open(out, 'w') as wf:
        wf.setnchannels(1)
        wf.setsampwidth(2)
        wf.setframerate(SAMPLE_RATE)
        wf.writeframes(samples.tobytes())

    duration_min = total_s / 60
    print(f"\nWrote {out}  ({duration_min:.1f} min, {len(samples):,} samples)")
    print("Play at MAX volume. Hands on thighs. Spine straight.")
    print("Let the room join the choir.")


if __name__ == "__main__":
    generate()
