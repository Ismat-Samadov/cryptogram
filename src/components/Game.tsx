'use client';

import { useEffect, useCallback, useMemo, useRef } from 'react';
import { motion, AnimatePresence } from 'framer-motion';

import { useGame } from '@/hooks/useGame';
import { useTimer } from '@/hooks/useTimer';
import { useHighScore } from '@/hooks/useHighScore';
import { useSound } from '@/hooks/useSound';

import Header from './Header';
import DifficultySelector from './DifficultySelector';
import CryptoGrid from './CryptoGrid';
import AlphabetBar from './AlphabetBar';
import Keyboard from './Keyboard';
import GameControls from './GameControls';
import EndScreen from './EndScreen';
import PauseOverlay from './PauseOverlay';

import { calculateScore } from '@/lib/score';
import type { Difficulty } from '@/types/game';

/**
 * Root game component — wires together all hooks and sub-components.
 */
export default function Game() {
  const game = useGame();
  const timer = useTimer();
  const { highScores, saveScore } = useHighScore();
  const { soundEnabled, toggleSound, sfx } = useSound();

  // Track whether the player just set a new high score (for the end screen)
  const isNewHighScoreRef = useRef(false);

  // ── Derived values ─────────────────────────────────────────────────────────

  const currentScore = useMemo(
    () =>
      game.status !== 'idle'
        ? calculateScore(game.difficulty, timer.elapsed, game.hintsUsed, game.wrongGuesses)
        : 0,
    [game.status, game.difficulty, timer.elapsed, game.hintsUsed, game.wrongGuesses],
  );

  /** Set of original letters that have already been correctly guessed (for keyboard dimming) */
  const solvedOriginalLetters = useMemo(() => {
    const s = new Set<string>();
    Object.entries(game.guessMap).forEach(([cipher, guess]) => {
      if (guess === game.reverseCipherMap[cipher]) s.add(guess);
    });
    return s;
  }, [game.guessMap, game.reverseCipherMap]);

  // ── Timer sync ─────────────────────────────────────────────────────────────

  useEffect(() => {
    if (game.status === 'playing') timer.start();
    else if (game.status === 'paused') timer.pause();
    else if (game.status === 'idle') timer.reset();
    // 'won' — let the timer freeze at current value
  }, [game.status]); // eslint-disable-line react-hooks/exhaustive-deps

  // ── Win handling ───────────────────────────────────────────────────────────

  useEffect(() => {
    if (game.status !== 'won') return;
    timer.pause();
    sfx.win();
    isNewHighScoreRef.current = saveScore(currentScore, timer.elapsed, game.difficulty);
  }, [game.status]); // eslint-disable-line react-hooks/exhaustive-deps

  // ── Keyboard handling ──────────────────────────────────────────────────────

  const handleKey = useCallback(
    (e: KeyboardEvent) => {
      if (game.status !== 'playing') return;

      const key = e.key.toUpperCase();

      if (key === 'ESCAPE') {
        sfx.click();
        game.deselect();
        return;
      }

      if (key === 'P') {
        sfx.pause();
        game.togglePause();
        return;
      }

      if ((key === 'BACKSPACE' || key === 'DELETE') && game.selectedCipher) {
        e.preventDefault();
        sfx.click();
        game.clearGuess();
        return;
      }

      // Tab / Arrow keys — advance to next unguessed cipher letter
      if (key === 'TAB' || key === 'ARROWRIGHT') {
        e.preventDefault();
        const letters = game.uniqueCipherLetters;
        if (letters.length === 0) return;
        const cur = game.selectedCipher;
        const idx = cur ? letters.indexOf(cur) : -1;
        for (let i = 1; i <= letters.length; i++) {
          const candidate = letters[(idx + i) % letters.length];
          if (game.guessMap[candidate] !== game.reverseCipherMap[candidate]) {
            sfx.select();
            game.selectCell(candidate);
            return;
          }
        }
        return;
      }

      if (key === 'ARROWLEFT') {
        e.preventDefault();
        const letters = game.uniqueCipherLetters;
        if (letters.length === 0) return;
        const cur = game.selectedCipher;
        const idx = cur ? letters.indexOf(cur) : letters.length;
        for (let i = 1; i <= letters.length; i++) {
          const candidate = letters[(idx - i + letters.length) % letters.length];
          if (game.guessMap[candidate] !== game.reverseCipherMap[candidate]) {
            sfx.select();
            game.selectCell(candidate);
            return;
          }
        }
        return;
      }

      // Letter guess
      if (/^[A-Z]$/.test(key) && game.selectedCipher) {
        e.preventDefault();
        const isCorrect = game.makeGuess(key);
        if (isCorrect) sfx.correct();
        else sfx.wrong();
      }
    },
    [game, sfx],
  );

  useEffect(() => {
    window.addEventListener('keydown', handleKey);
    return () => window.removeEventListener('keydown', handleKey);
  }, [handleKey]);

  // ── Handlers ───────────────────────────────────────────────────────────────

  const handleStartGame = useCallback(
    (difficulty: Difficulty) => {
      sfx.click();
      game.startGame(difficulty);
    },
    [game, sfx],
  );

  const handleSelectCell = useCallback(
    (cipherLetter: string) => {
      if (game.status !== 'playing') return;
      sfx.select();
      game.selectCell(cipherLetter);
    },
    [game, sfx],
  );

  const handleLetter = useCallback(
    (letter: string) => {
      if (!game.selectedCipher || game.status !== 'playing') return;
      const isCorrect = game.makeGuess(letter);
      if (isCorrect) sfx.correct();
      else sfx.wrong();
    },
    [game, sfx],
  );

  const handleBackspace = useCallback(() => {
    sfx.click();
    game.clearGuess();
  }, [game, sfx]);

  const handleHint = useCallback(() => {
    if (game.hintsUsed >= game.maxHints || game.status !== 'playing') return;
    sfx.hint();
    game.useHint();
  }, [game, sfx]);

  const handlePause = useCallback(() => {
    sfx.pause();
    game.togglePause();
  }, [game, sfx]);

  const handleNewGame = useCallback(() => {
    sfx.click();
    game.resetGame();
    timer.reset();
  }, [game, sfx, timer]);

  const handlePlayAgain = useCallback(() => {
    sfx.click();
    timer.reset();
    game.startGame(game.difficulty);
  }, [game, sfx, timer]);

  // ── Render ─────────────────────────────────────────────────────────────────

  return (
    <div className="min-h-screen flex flex-col bg-[#020818] text-slate-200">
      <Header
        status={game.status}
        difficulty={game.difficulty}
        elapsed={timer.elapsed}
        score={currentScore}
        wrongGuesses={game.wrongGuesses}
        highScore={highScores[game.difficulty]}
        soundEnabled={soundEnabled}
        onToggleSound={toggleSound}
      />

      <main className="flex-1 flex flex-col">
        <AnimatePresence mode="wait">
          {game.status === 'idle' ? (
            <motion.div
              key="home"
              initial={{ opacity: 0 }}
              animate={{ opacity: 1 }}
              exit={{ opacity: 0 }}
              className="flex-1 flex items-center justify-center"
            >
              <DifficultySelector highScores={highScores} onSelect={handleStartGame} />
            </motion.div>
          ) : (
            <motion.div
              key="game"
              initial={{ opacity: 0, y: 20 }}
              animate={{ opacity: 1, y: 0 }}
              exit={{ opacity: 0 }}
              className="flex-1 flex flex-col gap-5 py-4 px-2 sm:px-4 relative overflow-hidden"
            >
              {/* Pause overlay */}
              <PauseOverlay visible={game.status === 'paused'} onResume={handlePause} />

              {/* Puzzle attribution */}
              {game.puzzle && (
                <div className="text-center text-xs font-mono text-slate-500">
                  {game.puzzle.category}
                  {game.puzzle.author && (
                    <span className="text-slate-600"> — {game.puzzle.author}</span>
                  )}
                </div>
              )}

              {/* Cipher grid */}
              <div className="flex-1 flex items-center justify-center py-2">
                <CryptoGrid
                  encryptedText={game.encryptedText}
                  reverseCipherMap={game.reverseCipherMap}
                  guessMap={game.guessMap}
                  selectedCipher={game.selectedCipher}
                  revealedLetters={game.revealedLetters}
                  showSolution={game.status === 'won'}
                  onSelectCell={handleSelectCell}
                />
              </div>

              {/* Section divider */}
              <div className="border-t border-slate-800 mx-4" />

              {/* Alphabet reference bar */}
              <div className="flex flex-col items-center gap-2">
                <p className="text-xs font-mono text-slate-600">CIPHER MAP</p>
                <AlphabetBar
                  uniqueCipherLetters={game.uniqueCipherLetters}
                  reverseCipherMap={game.reverseCipherMap}
                  guessMap={game.guessMap}
                  selectedCipher={game.selectedCipher}
                  revealedLetters={game.revealedLetters}
                  onSelect={handleSelectCell}
                />
              </div>

              {/* Controls */}
              <GameControls
                status={game.status}
                difficulty={game.difficulty}
                hintsUsed={game.hintsUsed}
                maxHints={game.maxHints}
                onHint={handleHint}
                onPause={handlePause}
                onNewGame={handleNewGame}
              />

              {/* On-screen keyboard */}
              <div className="pb-2">
                <Keyboard
                  onLetter={handleLetter}
                  onBackspace={handleBackspace}
                  usedLetters={solvedOriginalLetters}
                  disabled={game.status !== 'playing' || !game.selectedCipher}
                />
              </div>
            </motion.div>
          )}
        </AnimatePresence>
      </main>

      {/* Win overlay */}
      {game.puzzle && (
        <EndScreen
          visible={game.status === 'won'}
          score={currentScore}
          elapsed={timer.elapsed}
          hintsUsed={game.hintsUsed}
          wrongGuesses={game.wrongGuesses}
          difficulty={game.difficulty}
          isNewHighScore={isNewHighScoreRef.current}
          puzzleAuthor={game.puzzle.author}
          puzzleCategory={game.puzzle.category}
          onPlayAgain={handlePlayAgain}
          onHome={handleNewGame}
        />
      )}
    </div>
  );
}
