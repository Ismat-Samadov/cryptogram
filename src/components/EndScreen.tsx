'use client';

import { motion, AnimatePresence } from 'framer-motion';
import type { Difficulty } from '@/types/game';
import { formatTime } from '@/lib/score';
import { DIFFICULTY_LABELS } from '@/lib/constants';

interface EndScreenProps {
  visible: boolean;
  score: number;
  elapsed: number;
  hintsUsed: number;
  wrongGuesses: number;
  difficulty: Difficulty;
  isNewHighScore: boolean;
  puzzleAuthor?: string;
  puzzleCategory: string;
  onPlayAgain: () => void;
  onHome: () => void;
}

/**
 * Animated win overlay displayed when the player solves the puzzle.
 */
export default function EndScreen({
  visible,
  score,
  elapsed,
  hintsUsed,
  wrongGuesses,
  difficulty,
  isNewHighScore,
  puzzleAuthor,
  puzzleCategory,
  onPlayAgain,
  onHome,
}: EndScreenProps) {
  return (
    <AnimatePresence>
      {visible && (
        <motion.div
          key="end"
          initial={{ opacity: 0 }}
          animate={{ opacity: 1 }}
          exit={{ opacity: 0 }}
          className="fixed inset-0 z-50 flex items-center justify-center p-4 bg-slate-950/80 backdrop-blur-sm"
        >
          <motion.div
            initial={{ scale: 0.7, y: 40, opacity: 0 }}
            animate={{ scale: 1, y: 0, opacity: 1 }}
            exit={{ scale: 0.7, y: 40, opacity: 0 }}
            transition={{ type: 'spring', stiffness: 300, damping: 25 }}
            className="relative w-full max-w-sm bg-slate-900 border-2 border-cyan-500 rounded-2xl p-6 text-center shadow-[0_0_60px_rgba(34,211,238,0.25)]"
          >
            {/* Celebration particles */}
            {[...Array(8)].map((_, i) => (
              <motion.span
                key={i}
                className="absolute text-xl pointer-events-none"
                initial={{ opacity: 1, x: 0, y: 0, scale: 0 }}
                animate={{
                  opacity: 0,
                  x: (Math.cos((i * Math.PI * 2) / 8) * 90),
                  y: (Math.sin((i * Math.PI * 2) / 8) * 90),
                  scale: 1.5,
                }}
                transition={{ duration: 0.9, delay: i * 0.05 }}
                style={{ top: '50%', left: '50%', translateX: '-50%', translateY: '-50%' }}
              >
                {['🎉', '✨', '🌟', '💫', '⭐', '🎊', '💥', '🔓'][i]}
              </motion.span>
            ))}

            {/* NEW HIGH SCORE banner */}
            {isNewHighScore && (
              <motion.div
                initial={{ scale: 0, rotate: -10 }}
                animate={{ scale: 1, rotate: 0 }}
                transition={{ delay: 0.4, type: 'spring', stiffness: 400 }}
                className="mb-4 inline-block px-3 py-1 rounded-full bg-yellow-500/20 border border-yellow-400 text-yellow-300 text-xs font-mono font-bold tracking-wider"
              >
                ★ NEW HIGH SCORE ★
              </motion.div>
            )}

            <motion.h2
              initial={{ y: -10, opacity: 0 }}
              animate={{ y: 0, opacity: 1 }}
              transition={{ delay: 0.15 }}
              className="font-mono font-black text-2xl sm:text-3xl text-transparent bg-clip-text bg-gradient-to-r from-cyan-400 to-green-400 mb-1"
            >
              DECODED!
            </motion.h2>

            <p className="text-slate-400 text-xs font-mono mb-5">
              {DIFFICULTY_LABELS[difficulty]} — {puzzleCategory}
              {puzzleAuthor && <span className="block text-slate-500">— {puzzleAuthor}</span>}
            </p>

            {/* Stats grid */}
            <div className="grid grid-cols-2 gap-3 mb-6">
              {[
                { label: 'Score', value: score, color: 'text-cyan-300' },
                { label: 'Time', value: formatTime(elapsed), color: 'text-slate-200' },
                { label: 'Hints', value: hintsUsed, color: 'text-purple-300' },
                { label: 'Errors', value: wrongGuesses, color: wrongGuesses > 0 ? 'text-red-400' : 'text-green-400' },
              ].map(({ label, value, color }) => (
                <div key={label} className="bg-slate-800/60 rounded-lg p-3 border border-slate-700">
                  <div className="text-slate-500 text-xs font-mono uppercase mb-1">{label}</div>
                  <div className={`text-xl font-mono font-bold ${color}`}>{value}</div>
                </div>
              ))}
            </div>

            {/* Buttons */}
            <div className="flex gap-3">
              <motion.button
                whileTap={{ scale: 0.94 }}
                onClick={onPlayAgain}
                className="flex-1 py-2.5 rounded-lg border-2 border-cyan-500 text-cyan-300 bg-cyan-900/20 font-mono font-bold text-sm hover:bg-cyan-900/40 transition-all"
              >
                Play Again
              </motion.button>
              <motion.button
                whileTap={{ scale: 0.94 }}
                onClick={onHome}
                className="flex-1 py-2.5 rounded-lg border border-slate-600 text-slate-400 bg-slate-800/40 font-mono font-bold text-sm hover:bg-slate-700/50 transition-all"
              >
                Home
              </motion.button>
            </div>
          </motion.div>
        </motion.div>
      )}
    </AnimatePresence>
  );
}
