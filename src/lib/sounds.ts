/**
 * Procedural sound effects using the Web Audio API.
 * No external audio files required — all sounds are synthesised at runtime.
 */

let audioCtx: AudioContext | null = null;

function getCtx(): AudioContext | null {
  if (typeof window === 'undefined') return null;
  if (!audioCtx) {
    const Ctx =
      window.AudioContext ||
      (window as unknown as { webkitAudioContext: typeof AudioContext }).webkitAudioContext;
    audioCtx = new Ctx();
  }
  // Resume if suspended (browser autoplay policy)
  if (audioCtx.state === 'suspended') {
    audioCtx.resume();
  }
  return audioCtx;
}

/** Play a single synthesised tone */
function tone(
  freq: number,
  duration: number,
  type: OscillatorType = 'sine',
  gainPeak: number = 0.25,
  startDelay: number = 0,
): void {
  const ctx = getCtx();
  if (!ctx) return;

  const osc = ctx.createOscillator();
  const gain = ctx.createGain();
  const t = ctx.currentTime + startDelay;

  osc.connect(gain);
  gain.connect(ctx.destination);

  osc.type = type;
  osc.frequency.setValueAtTime(freq, t);

  // Quick attack, exponential decay
  gain.gain.setValueAtTime(0, t);
  gain.gain.linearRampToValueAtTime(gainPeak, t + 0.01);
  gain.gain.exponentialRampToValueAtTime(0.001, t + duration);

  osc.start(t);
  osc.stop(t + duration + 0.01);
}

// ── Public sound functions ─────────────────────────────────────────────────

export function playClick(): void {
  tone(880, 0.07, 'square', 0.08);
}

export function playSelect(): void {
  tone(660, 0.08, 'sine', 0.12);
}

export function playCorrect(): void {
  tone(523, 0.12, 'sine', 0.2);
  tone(659, 0.18, 'sine', 0.2, 0.1);
}

export function playWrong(): void {
  tone(180, 0.18, 'sawtooth', 0.15);
}

export function playHint(): void {
  tone(440, 0.08, 'sine', 0.15);
  tone(554, 0.08, 'sine', 0.15, 0.1);
  tone(659, 0.14, 'sine', 0.15, 0.2);
}

export function playWin(): void {
  [523, 659, 784, 1047, 1319].forEach((f, i) => {
    tone(f, 0.3, 'sine', 0.22, i * 0.14);
  });
}

export function playPause(): void {
  tone(440, 0.1, 'sine', 0.1);
  tone(330, 0.15, 'sine', 0.1, 0.12);
}
