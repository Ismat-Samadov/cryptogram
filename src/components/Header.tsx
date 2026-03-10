'use client';

import { motion } from 'framer-motion';
import type { Difficulty, GameStatus, HighScore } from '@/types/game';
import { formatTime } from '@/lib/score';
import { DIFFICULTY_LABELS } from '@/lib/constants';

interface HeaderProps {
  status: GameStatus;
  difficulty: Difficulty;
  elapsed: number;
  score: number;
  wrongGuesses: number;
  highScore: HighScore | null;
  soundEnabled: boolean;
  onToggleSound: () => void;
}

/**
 * Top navigation bar — title, live stats, and sound toggle.
 */
export default function Header({
  status,
  difficulty,
  elapsed,
  score,
  wrongGuesses,
  highScore,
  soundEnabled,
  onToggleSound,
}: HeaderProps) {
  const isPlaying = status === 'playing' || status === 'paused';

  const difficultyBadge: Record<Difficulty, string> = {
    easy: 'text-green-400 border-green-700 bg-green-900/20',
    medium: 'text-yellow-400 border-yellow-700 bg-yellow-900/20',
    hard: 'text-red-400 border-red-700 bg-red-900/20',
  };

  return (
    <header className="flex items-center justify-between px-3 sm:px-6 py-3 border-b border-slate-800 bg-slate-950/80 backdrop-blur-sm sticky top-0 z-10">
      {/* Title */}
      <motion.h1
        className="font-mono font-black text-lg sm:text-2xl text-transparent bg-clip-text bg-gradient-to-r from-cyan-400 to-purple-400"
        style={{ textShadow: 'none' }}
        initial={{ opacity: 0, x: -20 }}
        animate={{ opacity: 1, x: 0 }}
      >
        CRYPTOGRAM
      </motion.h1>

      {/* Live game stats */}
      {isPlaying && (
        <div className="flex items-center gap-2 sm:gap-4 text-xs sm:text-sm font-mono">
          {/* Difficulty badge */}
          <span
            className={`hidden sm:inline-block px-2 py-0.5 rounded border text-xs font-bold ${difficultyBadge[difficulty]}`}
          >
            {DIFFICULTY_LABELS[difficulty].toUpperCase()}
          </span>

          {/* Timer */}
          <div className="flex items-center gap-1 text-slate-300">
            <span className="text-slate-500">⏱</span>
            <span>{formatTime(elapsed)}</span>
          </div>

          {/* Score */}
          <div className="flex items-center gap-1">
            <span className="text-slate-500">⭐</span>
            <motion.span
              key={score}
              initial={{ scale: 1.3, color: '#fbbf24' }}
              animate={{ scale: 1, color: '#e2e8f0' }}
              transition={{ duration: 0.3 }}
              className="text-slate-200"
            >
              {score}
            </motion.span>
          </div>

          {/* Wrongs */}
          {wrongGuesses > 0 && (
            <div className="hidden sm:flex items-center gap-1 text-red-400">
              <span>✗</span>
              <span>{wrongGuesses}</span>
            </div>
          )}

          {/* High score */}
          {highScore && (
            <div className="hidden lg:flex items-center gap-1 text-yellow-500">
              <span>🏆</span>
              <span>{highScore.score}</span>
            </div>
          )}
        </div>
      )}

      {/* Sound toggle */}
      <motion.button
        whileTap={{ scale: 0.88 }}
        onClick={onToggleSound}
        className="ml-2 sm:ml-0 text-lg sm:text-xl focus:outline-none focus-visible:ring-2 focus-visible:ring-cyan-400 rounded"
        title={soundEnabled ? 'Mute sounds' : 'Enable sounds'}
        aria-label={soundEnabled ? 'Mute sounds' : 'Enable sounds'}
      >
        {soundEnabled ? '🔊' : '🔇'}
      </motion.button>
    </header>
  );
}
