'use client';

import { useState, useEffect, useCallback } from 'react';
import type { Difficulty, HighScore } from '@/types/game';

const STORAGE_KEY = 'cryptogram-high-scores-v1';

type ScoreState = Record<Difficulty, HighScore | null>;

const DEFAULT_STATE: ScoreState = { easy: null, medium: null, hard: null };

/**
 * Persist and retrieve best scores per difficulty using localStorage.
 * Gracefully handles environments where localStorage is unavailable.
 */
export function useHighScore() {
  const [highScores, setHighScores] = useState<ScoreState>(DEFAULT_STATE);

  // Hydrate from localStorage on mount (client only)
  useEffect(() => {
    try {
      const raw = localStorage.getItem(STORAGE_KEY);
      if (raw) setHighScores(JSON.parse(raw));
    } catch {
      /* localStorage unavailable — no-op */
    }
  }, []);

  /**
   * Conditionally update the stored high score if the new score is better.
   * Returns true if a new high score was recorded.
   */
  const saveScore = useCallback(
    (score: number, timeSeconds: number, difficulty: Difficulty): boolean => {
      let isNew = false;
      setHighScores((prev) => {
        const existing = prev[difficulty];
        if (existing && score <= existing.score) return prev;

        isNew = true;
        const next: ScoreState = {
          ...prev,
          [difficulty]: {
            score,
            timeSeconds,
            difficulty,
            date: new Date().toLocaleDateString(),
          },
        };
        try {
          localStorage.setItem(STORAGE_KEY, JSON.stringify(next));
        } catch {
          /* ignore */
        }
        return next;
      });
      return isNew;
    },
    [],
  );

  return { highScores, saveScore };
}
