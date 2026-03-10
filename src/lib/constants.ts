import type { Difficulty, DifficultyConfig } from '@/types/game';

export const ALPHABET = 'ABCDEFGHIJKLMNOPQRSTUVWXYZ'.split('');

export const DIFFICULTY_CONFIG: Record<Difficulty, DifficultyConfig> = {
  easy: {
    maxHints: 5,
    baseScore: 1000,
    scoreDecayPerSecond: 3,
    hintPenalty: 80,
    wrongGuessPenalty: 5,
  },
  medium: {
    maxHints: 3,
    baseScore: 2000,
    scoreDecayPerSecond: 8,
    hintPenalty: 150,
    wrongGuessPenalty: 15,
  },
  hard: {
    maxHints: 1,
    baseScore: 4000,
    scoreDecayPerSecond: 15,
    hintPenalty: 300,
    wrongGuessPenalty: 30,
  },
};

export const DIFFICULTY_LABELS: Record<Difficulty, string> = {
  easy: 'Easy',
  medium: 'Medium',
  hard: 'Hard',
};

export const DIFFICULTY_COLORS: Record<Difficulty, string> = {
  easy: 'text-green-400 border-green-400',
  medium: 'text-yellow-400 border-yellow-400',
  hard: 'text-red-400 border-red-400',
};
