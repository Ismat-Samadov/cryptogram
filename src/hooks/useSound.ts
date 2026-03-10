'use client';

import { useState, useCallback, useEffect } from 'react';
import {
  playClick,
  playSelect,
  playCorrect,
  playWrong,
  playHint,
  playWin,
  playPause,
} from '@/lib/sounds';

const STORAGE_KEY = 'cryptogram-sound-enabled';

/**
 * Manages sound-on/off state (persisted to localStorage) and exposes
 * typed sound-effect helpers that respect the current toggle.
 */
export function useSound() {
  const [soundEnabled, setSoundEnabled] = useState(true);

  // Hydrate preference on mount
  useEffect(() => {
    try {
      const stored = localStorage.getItem(STORAGE_KEY);
      if (stored !== null) setSoundEnabled(JSON.parse(stored));
    } catch {
      /* ignore */
    }
  }, []);

  const toggleSound = useCallback(() => {
    setSoundEnabled((prev) => {
      const next = !prev;
      try {
        localStorage.setItem(STORAGE_KEY, JSON.stringify(next));
      } catch {
        /* ignore */
      }
      return next;
    });
  }, []);

  const sfx = {
    click: () => soundEnabled && playClick(),
    select: () => soundEnabled && playSelect(),
    correct: () => soundEnabled && playCorrect(),
    wrong: () => soundEnabled && playWrong(),
    hint: () => soundEnabled && playHint(),
    win: () => soundEnabled && playWin(),
    pause: () => soundEnabled && playPause(),
  };

  return { soundEnabled, toggleSound, sfx };
}
