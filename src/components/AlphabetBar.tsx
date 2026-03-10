'use client';

import { motion } from 'framer-motion';
import type { GuessMap } from '@/types/game';

interface AlphabetBarProps {
  /** Only the cipher letters that actually appear in this puzzle */
  uniqueCipherLetters: string[];
  reverseCipherMap: Record<string, string>;
  guessMap: GuessMap;
  selectedCipher: string | null;
  revealedLetters: Set<string>;
  onSelect: (cipherLetter: string) => void;
}

/**
 * A compact reference strip showing every cipher letter in the puzzle
 * with the player's current guess below it. Doubles as a click target
 * for selecting a cipher letter.
 */
export default function AlphabetBar({
  uniqueCipherLetters,
  reverseCipherMap,
  guessMap,
  selectedCipher,
  revealedLetters,
  onSelect,
}: AlphabetBarProps) {
  return (
    <div className="flex flex-wrap justify-center gap-1 px-2">
      {uniqueCipherLetters.map((cl) => {
        const guess = guessMap[cl] ?? '';
        const correct = reverseCipherMap[cl] ?? '';
        const isCorrect = guess === correct && guess !== '';
        const isRevealed = revealedLetters.has(cl);
        const isSelected = selectedCipher === cl;
        const hasWrong = guess !== '' && !isCorrect && !isRevealed;

        const bg = isSelected
          ? 'bg-cyan-500/20 border-cyan-400'
          : isRevealed
            ? 'bg-purple-500/10 border-purple-400'
            : isCorrect
              ? 'bg-green-500/10 border-green-400'
              : hasWrong
                ? 'bg-red-500/10 border-red-400'
                : 'bg-slate-800/60 border-slate-600 hover:border-cyan-600';

        const guessColor = isRevealed
          ? 'text-purple-300'
          : isCorrect
            ? 'text-green-400'
            : hasWrong
              ? 'text-red-400'
              : 'text-slate-400';

        return (
          <motion.button
            key={cl}
            whileTap={{ scale: 0.9 }}
            onClick={() => onSelect(cl)}
            className={`
              flex flex-col items-center justify-between
              w-8 h-12 border rounded-sm
              transition-all duration-100 cursor-pointer
              focus:outline-none focus-visible:ring-1 focus-visible:ring-cyan-400
              ${bg}
            `}
            title={`Cipher: ${cl} → Guess: ${guess || '?'}`}
          >
            <span className="pt-0.5 text-[10px] font-mono font-bold text-slate-400 leading-none">
              {cl}
            </span>
            <span className="w-full border-t border-slate-700" />
            <span className={`pb-0.5 text-xs font-mono font-bold leading-none ${guessColor}`}>
              {guess || '\u00A0'}
            </span>
          </motion.button>
        );
      })}
    </div>
  );
}
