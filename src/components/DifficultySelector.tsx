'use client';

import { motion } from 'framer-motion';
import type { Difficulty, HighScore } from '@/types/game';
import { DIFFICULTY_LABELS, DIFFICULTY_CONFIG } from '@/lib/constants';

interface DifficultySelectorProps {
  highScores: Record<Difficulty, HighScore | null>;
  onSelect: (difficulty: Difficulty) => void;
}

const DIFF_STYLES: Record<
  Difficulty,
  { border: string; hover: string; glow: string; badge: string; desc: string }
> = {
  easy: {
    border: 'border-green-500',
    hover: 'hover:bg-green-900/20 hover:shadow-[0_0_18px_rgba(74,222,128,0.35)]',
    glow: 'shadow-[0_0_8px_rgba(74,222,128,0.2)]',
    badge: 'bg-green-900/30 text-green-400 border-green-700',
    desc: `Up to ${DIFFICULTY_CONFIG.easy.maxHints} hints • +1 pt/3 s`,
  },
  medium: {
    border: 'border-yellow-500',
    hover: 'hover:bg-yellow-900/20 hover:shadow-[0_0_18px_rgba(234,179,8,0.35)]',
    glow: 'shadow-[0_0_8px_rgba(234,179,8,0.2)]',
    badge: 'bg-yellow-900/30 text-yellow-400 border-yellow-700',
    desc: `Up to ${DIFFICULTY_CONFIG.medium.maxHints} hints • +1 pt/8 s`,
  },
  hard: {
    border: 'border-red-500',
    hover: 'hover:bg-red-900/20 hover:shadow-[0_0_18px_rgba(239,68,68,0.35)]',
    glow: 'shadow-[0_0_8px_rgba(239,68,68,0.2)]',
    badge: 'bg-red-900/30 text-red-400 border-red-700',
    desc: `${DIFFICULTY_CONFIG.hard.maxHints} hint only • +1 pt/15 s`,
  },
};

/**
 * Home screen — pick a difficulty to start a new game.
 */
export default function DifficultySelector({ highScores, onSelect }: DifficultySelectorProps) {
  return (
    <motion.div
      initial={{ opacity: 0, y: 30 }}
      animate={{ opacity: 1, y: 0 }}
      className="flex flex-col items-center gap-6 sm:gap-8 px-4 py-8"
    >
      {/* Hero title */}
      <div className="text-center">
        <motion.div
          className="text-6xl sm:text-7xl mb-3 select-none"
          animate={{ rotateY: [0, 360] }}
          transition={{ duration: 3, repeat: Infinity, repeatDelay: 5, ease: 'easeInOut' }}
        >
          🔐
        </motion.div>
        <h2 className="font-mono font-black text-3xl sm:text-4xl text-transparent bg-clip-text bg-gradient-to-r from-cyan-400 via-purple-400 to-pink-400 mb-2">
          CRYPTOGRAM
        </h2>
        <p className="text-slate-400 text-sm font-mono max-w-xs text-center">
          Decode the encrypted quote by cracking the substitution cipher.
          <br className="hidden sm:block" /> Every letter maps to exactly one other letter.
        </p>
      </div>

      {/* Difficulty cards */}
      <div className="grid grid-cols-1 sm:grid-cols-3 gap-4 w-full max-w-lg">
        {(['easy', 'medium', 'hard'] as Difficulty[]).map((diff) => {
          const styles = DIFF_STYLES[diff];
          const hs = highScores[diff];

          return (
            <motion.button
              key={diff}
              whileHover={{ y: -3 }}
              whileTap={{ scale: 0.96 }}
              onClick={() => onSelect(diff)}
              className={`
                flex flex-col items-center gap-3 p-5 rounded-xl border-2
                bg-slate-900/60 transition-all duration-200 cursor-pointer
                focus:outline-none focus-visible:ring-2 focus-visible:ring-cyan-400
                ${styles.border} ${styles.hover} ${styles.glow}
              `}
            >
              <span className={`text-xs font-mono font-bold px-2 py-0.5 rounded border ${styles.badge}`}>
                {DIFFICULTY_LABELS[diff].toUpperCase()}
              </span>
              <span className="text-slate-400 text-xs font-mono text-center leading-relaxed">
                {styles.desc}
              </span>
              {hs ? (
                <span className="text-yellow-400 text-xs font-mono">
                  🏆 Best: {hs.score}
                </span>
              ) : (
                <span className="text-slate-600 text-xs font-mono">No score yet</span>
              )}
            </motion.button>
          );
        })}
      </div>

      {/* How to play */}
      <div className="max-w-sm text-center">
        <p className="text-slate-600 text-xs font-mono leading-relaxed">
          Click a letter cell → type the decoded letter. <br />
          Use keyboard A–Z, Backspace to clear, Tab/Arrows to navigate.
        </p>
      </div>
    </motion.div>
  );
}
