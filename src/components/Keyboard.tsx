'use client';

import { motion } from 'framer-motion';

const ROWS = [
  ['Q', 'W', 'E', 'R', 'T', 'Y', 'U', 'I', 'O', 'P'],
  ['A', 'S', 'D', 'F', 'G', 'H', 'J', 'K', 'L'],
  ['⌫', 'Z', 'X', 'C', 'V', 'B', 'N', 'M', '✓'],
];

interface KeyboardProps {
  onLetter: (letter: string) => void;
  onBackspace: () => void;
  /** Letters that have been correctly guessed already */
  usedLetters: Set<string>;
  disabled: boolean;
}

/**
 * On-screen QWERTY keyboard for touch devices.
 * Correct letters are dimmed. Backspace and Enter are shown as special keys.
 */
export default function Keyboard({ onLetter, onBackspace, usedLetters, disabled }: KeyboardProps) {
  const handleKey = (key: string) => {
    if (disabled) return;
    if (key === '⌫') {
      onBackspace();
    } else if (key !== '✓') {
      onLetter(key);
    }
  };

  return (
    <div className="flex flex-col items-center gap-1.5 w-full select-none">
      {ROWS.map((row, rowIdx) => (
        <div key={rowIdx} className="flex gap-1">
          {row.map((key) => {
            const isSpecial = key === '⌫' || key === '✓';
            const isUsed = !isSpecial && usedLetters.has(key);

            return (
              <motion.button
                key={key}
                whileTap={{ scale: 0.88 }}
                onPointerDown={(e) => {
                  e.preventDefault(); // prevent focus stealing
                  handleKey(key);
                }}
                disabled={disabled}
                className={`
                  flex items-center justify-center
                  h-10 rounded font-mono font-bold text-sm
                  transition-all duration-100 cursor-pointer
                  focus:outline-none select-none
                  ${isSpecial ? 'min-w-[2.8rem] bg-cyan-700/40 border border-cyan-600 text-cyan-300 hover:bg-cyan-700/60' : ''}
                  ${!isSpecial && !isUsed ? 'w-8 bg-slate-700/60 border border-slate-600 text-slate-200 hover:bg-slate-600/80 hover:border-cyan-500' : ''}
                  ${!isSpecial && isUsed ? 'w-8 bg-slate-800/40 border border-slate-700 text-slate-600 cursor-not-allowed' : ''}
                  ${disabled ? 'opacity-50 cursor-not-allowed' : ''}
                `}
              >
                {key}
              </motion.button>
            );
          })}
        </div>
      ))}
    </div>
  );
}
