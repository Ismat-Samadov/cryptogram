import type { Difficulty } from '@/types/game';
import { DIFFICULTY_CONFIG } from './constants';

/**
 * Calculate the final score based on elapsed time, hints used, and wrong guesses.
 * Score is clamped to a minimum of 0.
 */
export function calculateScore(
  difficulty: Difficulty,
  elapsedSeconds: number,
  hintsUsed: number,
  wrongGuesses: number,
): number {
  const { baseScore, scoreDecayPerSecond, hintPenalty, wrongGuessPenalty } =
    DIFFICULTY_CONFIG[difficulty];

  const score =
    baseScore -
    Math.floor(elapsedSeconds * scoreDecayPerSecond) -
    hintsUsed * hintPenalty -
    wrongGuesses * wrongGuessPenalty;

  return Math.max(0, score);
}

/** Format seconds as MM:SS */
export function formatTime(seconds: number): string {
  const m = Math.floor(seconds / 60)
    .toString()
    .padStart(2, '0');
  const s = (seconds % 60).toString().padStart(2, '0');
  return `${m}:${s}`;
}
