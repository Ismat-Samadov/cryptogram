'use client';

import LetterCell from './LetterCell';
import type { GuessMap } from '@/types/game';

interface CryptoGridProps {
  encryptedText: string;
  reverseCipherMap: Record<string, string>;
  guessMap: GuessMap;
  selectedCipher: string | null;
  revealedLetters: Set<string>;
  showSolution: boolean;
  onSelectCell: (cipherLetter: string) => void;
}

/**
 * Renders the full encrypted puzzle as a wrapping flex grid.
 * Letters are grouped into "words" so wrapping always happens at word boundaries.
 * Non-letter characters (spaces, punctuation, digits) are rendered as plain text.
 */
export default function CryptoGrid({
  encryptedText,
  reverseCipherMap,
  guessMap,
  selectedCipher,
  revealedLetters,
  showSolution,
  onSelectCell,
}: CryptoGridProps) {
  // Split into tokens: sequences of letters, and individual non-letter chars
  const tokens = encryptedText.match(/[A-Z]+|[^A-Z]/g) ?? [];

  return (
    <div className="flex flex-wrap justify-center gap-x-3 gap-y-4 px-2">
      {tokens.map((token, tokenIdx) => {
        // Non-letter characters are spacers
        if (!/^[A-Z]+$/.test(token)) {
          return (
            <span
              key={`sep-${tokenIdx}`}
              className="flex items-end pb-1 text-slate-500 font-mono text-sm select-none"
              aria-hidden="true"
            >
              {token === ' ' ? null : token}
            </span>
          );
        }

        // Letter word — wrap as a unit
        return (
          <span key={`word-${tokenIdx}`} className="flex gap-0.5">
            {token.split('').map((cipherLetter, charIdx) => {
              const guess = guessMap[cipherLetter] ?? '';
              const correctLetter = reverseCipherMap[cipherLetter] ?? '';
              const isCorrect = guess === correctLetter;
              const isSelected = selectedCipher === cipherLetter;
              const isRevealed = revealedLetters.has(cipherLetter);

              return (
                <LetterCell
                  key={`cell-${tokenIdx}-${charIdx}`}
                  cipherLetter={cipherLetter}
                  guess={guess}
                  isSelected={isSelected}
                  isCorrect={isCorrect}
                  isRevealed={isRevealed}
                  showSolution={showSolution}
                  correctLetter={correctLetter}
                  onClick={() => onSelectCell(cipherLetter)}
                />
              );
            })}
          </span>
        );
      })}
    </div>
  );
}
