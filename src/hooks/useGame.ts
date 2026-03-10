'use client';

import { useState, useCallback } from 'react';
import type { Difficulty, GameStatus, GuessMap, Puzzle } from '@/types/game';
import { generateCipher, encryptText, invertCipher, getUniqueLetters } from '@/lib/cipher';
import { getRandomPuzzle } from '@/lib/puzzles';
import { DIFFICULTY_CONFIG } from '@/lib/constants';

// ── State shape ──────────────────────────────────────────────────────────────

interface GameState {
  puzzle: Puzzle | null;
  encryptedText: string;
  /** original letter → cipher letter */
  cipherMap: Record<string, string>;
  /** cipher letter → original letter */
  reverseCipherMap: Record<string, string>;
  /** cipher letter → player's guess */
  guessMap: GuessMap;
  /** currently selected cipher letter */
  selectedCipher: string | null;
  status: GameStatus;
  difficulty: Difficulty;
  hintsUsed: number;
  maxHints: number;
  wrongGuesses: number;
  /** cipher letters that were revealed by hints — cannot be cleared */
  revealedLetters: Set<string>;
  /** every cipher letter present in the puzzle, sorted */
  uniqueCipherLetters: string[];
}

const INITIAL: GameState = {
  puzzle: null,
  encryptedText: '',
  cipherMap: {},
  reverseCipherMap: {},
  guessMap: {},
  selectedCipher: null,
  status: 'idle',
  difficulty: 'medium',
  hintsUsed: 0,
  maxHints: 3,
  wrongGuesses: 0,
  revealedLetters: new Set(),
  uniqueCipherLetters: [],
};

// ── Helper ───────────────────────────────────────────────────────────────────

/**
 * Find the next cipher letter after `current` that has not yet been
 * correctly guessed, wrapping around if needed.
 */
function nextUnguessed(
  letters: string[],
  current: string,
  guessMap: GuessMap,
  reverseMap: Record<string, string>,
): string | null {
  const idx = letters.indexOf(current);
  for (let i = 1; i <= letters.length; i++) {
    const candidate = letters[(idx + i) % letters.length];
    if (guessMap[candidate] !== reverseMap[candidate]) return candidate;
  }
  return null; // all solved
}

// ── Hook ──────────────────────────────────────────────────────────────────────

export function useGame() {
  const [state, setState] = useState<GameState>(INITIAL);

  /** Initialise a brand-new game for the given difficulty */
  const startGame = useCallback((difficulty: Difficulty) => {
    const puzzle = getRandomPuzzle(difficulty);
    const cipherMap = generateCipher();
    const reverseCipherMap = invertCipher(cipherMap);
    const encryptedText = encryptText(puzzle.text, cipherMap);
    const uniqueCipherLetters = getUniqueLetters(encryptedText);
    const { maxHints } = DIFFICULTY_CONFIG[difficulty];

    setState({
      puzzle,
      encryptedText,
      cipherMap,
      reverseCipherMap,
      guessMap: {},
      selectedCipher: null,
      status: 'playing',
      difficulty,
      hintsUsed: 0,
      maxHints,
      wrongGuesses: 0,
      revealedLetters: new Set(),
      uniqueCipherLetters,
    });
  }, []);

  /** Select or deselect a cipher letter cell */
  const selectCell = useCallback((cipherLetter: string) => {
    setState((prev) => ({
      ...prev,
      selectedCipher: prev.selectedCipher === cipherLetter ? null : cipherLetter,
    }));
  }, []);

  /**
   * Assign `letter` as the guess for the currently selected cipher letter.
   * Returns whether the guess was correct.
   */
  const makeGuess = useCallback((letter: string): boolean => {
    let correct = false;

    setState((prev) => {
      if (!prev.selectedCipher || prev.status !== 'playing') return prev;

      const upper = letter.toUpperCase();
      const correctLetter = prev.reverseCipherMap[prev.selectedCipher];
      correct = upper === correctLetter;

      const newGuessMap: GuessMap = { ...prev.guessMap, [prev.selectedCipher]: upper };
      const newWrongGuesses = correct ? prev.wrongGuesses : prev.wrongGuesses + 1;

      // Win when every unique cipher letter is correctly guessed
      const won = prev.uniqueCipherLetters.every(
        (cl) => (cl === prev.selectedCipher ? upper : newGuessMap[cl]) === prev.reverseCipherMap[cl],
      );

      const newSelected = won
        ? null
        : nextUnguessed(prev.uniqueCipherLetters, prev.selectedCipher, newGuessMap, prev.reverseCipherMap);

      return {
        ...prev,
        guessMap: newGuessMap,
        wrongGuesses: newWrongGuesses,
        status: won ? 'won' : prev.status,
        selectedCipher: newSelected,
      };
    });

    return correct;
  }, []);

  /** Clear the current guess for the selected cipher letter (if not hint-revealed) */
  const clearGuess = useCallback(() => {
    setState((prev) => {
      if (!prev.selectedCipher || prev.status !== 'playing') return prev;
      if (prev.revealedLetters.has(prev.selectedCipher)) return prev;

      const newGuessMap = { ...prev.guessMap };
      delete newGuessMap[prev.selectedCipher];
      return { ...prev, guessMap: newGuessMap };
    });
  }, []);

  /** Reveal a random unsolved cipher letter as a hint */
  const useHint = useCallback(() => {
    setState((prev) => {
      if (prev.hintsUsed >= prev.maxHints || prev.status !== 'playing') return prev;

      const unrevealed = prev.uniqueCipherLetters.filter(
        (cl) =>
          !prev.revealedLetters.has(cl) &&
          prev.guessMap[cl] !== prev.reverseCipherMap[cl],
      );
      if (unrevealed.length === 0) return prev;

      const target = unrevealed[Math.floor(Math.random() * unrevealed.length)];
      const correctLetter = prev.reverseCipherMap[target];
      const newGuessMap: GuessMap = { ...prev.guessMap, [target]: correctLetter };
      const newRevealed = new Set(prev.revealedLetters).add(target);

      const won = prev.uniqueCipherLetters.every(
        (cl) => (cl === target ? correctLetter : newGuessMap[cl]) === prev.reverseCipherMap[cl],
      );

      return {
        ...prev,
        guessMap: newGuessMap,
        hintsUsed: prev.hintsUsed + 1,
        revealedLetters: newRevealed,
        status: won ? 'won' : prev.status,
      };
    });
  }, []);

  /** Toggle between playing and paused */
  const togglePause = useCallback(() => {
    setState((prev) => {
      if (prev.status === 'playing') return { ...prev, status: 'paused', selectedCipher: null };
      if (prev.status === 'paused') return { ...prev, status: 'playing' };
      return prev;
    });
  }, []);

  /** Deselect the current cell */
  const deselect = useCallback(() => {
    setState((prev) => ({ ...prev, selectedCipher: null }));
  }, []);

  /** Return to the idle/home screen */
  const resetGame = useCallback(() => {
    setState(INITIAL);
  }, []);

  return {
    ...state,
    startGame,
    selectCell,
    makeGuess,
    clearGuess,
    useHint,
    togglePause,
    deselect,
    resetGame,
  };
}
