'use client';

import { motion } from 'framer-motion';

interface LetterCellProps {
  /** The encrypted letter shown to the player */
  cipherLetter: string;
  /** Player's current guess for this cipher letter (may be empty string) */
  guess: string;
  /** Whether this cell's cipher letter is currently selected */
  isSelected: boolean;
  /** True when guess matches the correct original letter */
  isCorrect: boolean;
  /** True when the letter was filled in by a hint */
  isRevealed: boolean;
  /** When the game is won, show the correct answer regardless */
  showSolution: boolean;
  /** The actual plaintext letter (used only when showSolution=true) */
  correctLetter: string;
  onClick: () => void;
}

/**
 * A single cipher cell: cipher letter on top, guess box on the bottom.
 * Visual states: default → selected → correct → wrong → revealed.
 */
export default function LetterCell({
  cipherLetter,
  guess,
  isSelected,
  isCorrect,
  isRevealed,
  showSolution,
  correctLetter,
  onClick,
}: LetterCellProps) {
  const displayGuess = showSolution ? correctLetter : guess;
  const hasWrongGuess = !isCorrect && !isRevealed && guess !== '';

  // Determine border / glow class
  const borderClass = isSelected
    ? 'border-cyan-400 shadow-[0_0_12px_rgba(34,211,238,0.7)] bg-cyan-900/20'
    : isRevealed
      ? 'border-purple-400 shadow-[0_0_8px_rgba(192,132,252,0.5)] bg-purple-900/10'
      : isCorrect
        ? 'border-green-400 shadow-[0_0_8px_rgba(74,222,128,0.5)] bg-green-900/10'
        : hasWrongGuess
          ? 'border-red-400 shadow-[0_0_8px_rgba(248,113,113,0.4)] bg-red-900/10'
          : 'border-slate-600 hover:border-cyan-600 hover:bg-slate-800/60 bg-slate-900/40';

  const guessColor = showSolution
    ? 'text-cyan-300'
    : isRevealed
      ? 'text-purple-300'
      : isCorrect
        ? 'text-green-400'
        : hasWrongGuess
          ? 'text-red-400'
          : 'text-slate-300';

  return (
    <motion.button
      onClick={onClick}
      whileTap={{ scale: 0.92 }}
      className={`
        flex flex-col items-center justify-between
        w-9 h-14 sm:w-10 sm:h-16
        border rounded-sm cursor-pointer select-none
        transition-all duration-150
        focus:outline-none focus-visible:ring-2 focus-visible:ring-cyan-400
        ${borderClass}
      `}
      aria-label={`Cipher letter ${cipherLetter}, guess: ${displayGuess || 'empty'}`}
    >
      {/* Cipher letter — always visible */}
      <span className="pt-1 text-xs sm:text-sm font-mono font-bold text-slate-400 leading-none">
        {cipherLetter}
      </span>

      {/* Divider */}
      <span className="w-full border-t border-slate-700" />

      {/* Player's guess */}
      <span
        className={`pb-1 text-sm sm:text-base font-mono font-bold leading-none transition-colors duration-150 ${guessColor}`}
      >
        {displayGuess || '\u00A0'}
      </span>
    </motion.button>
  );
}
