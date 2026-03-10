// Core game type definitions

export type Difficulty = 'easy' | 'medium' | 'hard';

export type GameStatus = 'idle' | 'playing' | 'paused' | 'won';

/** A single puzzle entry — plaintext phrase with metadata */
export interface Puzzle {
  id: string;
  text: string;
  author?: string;
  category: string;
  difficulty: Difficulty;
}

/** Per-difficulty tuning values */
export interface DifficultyConfig {
  maxHints: number;
  baseScore: number;
  scoreDecayPerSecond: number;
  hintPenalty: number;
  wrongGuessPenalty: number;
}

/**
 * Maps cipher letter → player's guessed original letter.
 * e.g. { 'Q': 'T', 'E': 'H', ... }
 */
export interface GuessMap {
  [cipherLetter: string]: string;
}

/** Persisted best-score per difficulty */
export interface HighScore {
  score: number;
  timeSeconds: number;
  difficulty: Difficulty;
  date: string;
}
