'use client';

import { motion } from 'framer-motion';
import type { Difficulty, GameStatus } from '@/types/game';
import { DIFFICULTY_CONFIG } from '@/lib/constants';

interface GameControlsProps {
  status: GameStatus;
  difficulty: Difficulty;
  hintsUsed: number;
  maxHints: number;
  onHint: () => void;
  onPause: () => void;
  onNewGame: () => void;
}

/**
 * Bottom control bar: Hint, Pause/Resume, and New Game buttons.
 */
export default function GameControls({
  status,
  difficulty,
  hintsUsed,
  maxHints,
  onHint,
  onPause,
  onNewGame,
}: GameControlsProps) {
  const hintsLeft = maxHints - hintsUsed;
  const canHint = hintsLeft > 0 && status === 'playing';
  const isPaused = status === 'paused';

  return (
    <div className="flex items-center justify-center gap-3 flex-wrap">
      {/* Hint button */}
      <motion.button
        whileTap={{ scale: 0.93 }}
        onClick={onHint}
        disabled={!canHint}
        className={`
          flex items-center gap-2 px-4 py-2 rounded-md border font-mono text-sm font-bold
          transition-all duration-150 focus:outline-none focus-visible:ring-2 focus-visible:ring-purple-400
          ${canHint
            ? 'border-purple-400 text-purple-300 bg-purple-900/20 hover:bg-purple-900/40 hover:shadow-[0_0_12px_rgba(168,85,247,0.4)]'
            : 'border-slate-700 text-slate-600 cursor-not-allowed bg-slate-900/20'
          }
        `}
        title={canHint ? `Use a hint (${hintsLeft} left)` : 'No hints remaining'}
      >
        <span>💡</span>
        <span>Hint ({hintsLeft}/{maxHints})</span>
      </motion.button>

      {/* Pause / Resume */}
      {(status === 'playing' || status === 'paused') && (
        <motion.button
          whileTap={{ scale: 0.93 }}
          onClick={onPause}
          className="
            flex items-center gap-2 px-4 py-2 rounded-md border font-mono text-sm font-bold
            border-cyan-600 text-cyan-300 bg-cyan-900/10 hover:bg-cyan-900/30
            hover:shadow-[0_0_12px_rgba(34,211,238,0.3)]
            transition-all duration-150 focus:outline-none focus-visible:ring-2 focus-visible:ring-cyan-400
          "
        >
          <span>{isPaused ? '▶' : '⏸'}</span>
          <span>{isPaused ? 'Resume' : 'Pause'}</span>
        </motion.button>
      )}

      {/* New Game */}
      <motion.button
        whileTap={{ scale: 0.93 }}
        onClick={onNewGame}
        className="
          flex items-center gap-2 px-4 py-2 rounded-md border font-mono text-sm font-bold
          border-slate-500 text-slate-400 bg-slate-800/30 hover:bg-slate-700/40 hover:border-slate-400
          transition-all duration-150 focus:outline-none focus-visible:ring-2 focus-visible:ring-slate-400
        "
      >
        <span>↺</span>
        <span>New Game</span>
      </motion.button>
    </div>
  );
}
