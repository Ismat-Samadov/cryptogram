import { ALPHABET } from './constants';

/**
 * Fisher-Yates shuffle — returns a new shuffled copy of the array.
 */
function shuffle<T>(array: T[]): T[] {
  const arr = [...array];
  for (let i = arr.length - 1; i > 0; i--) {
    const j = Math.floor(Math.random() * (i + 1));
    [arr[i], arr[j]] = [arr[j], arr[i]];
  }
  return arr;
}

/**
 * Generate a random derangement of the alphabet so that no letter
 * maps to itself (standard requirement for substitution ciphers).
 * Returns a map of originalLetter → cipherLetter.
 */
export function generateCipher(): Record<string, string> {
  let derangement: string[];
  do {
    derangement = shuffle([...ALPHABET]);
  } while (derangement.some((letter, i) => letter === ALPHABET[i]));

  const cipher: Record<string, string> = {};
  ALPHABET.forEach((letter, i) => {
    cipher[letter] = derangement[i];
  });
  return cipher;
}

/**
 * Invert a cipher map — swaps keys and values.
 * Used to create cipherLetter → originalLetter lookup.
 */
export function invertCipher(cipher: Record<string, string>): Record<string, string> {
  const inverted: Record<string, string> = {};
  Object.entries(cipher).forEach(([key, value]) => {
    inverted[value] = key;
  });
  return inverted;
}

/**
 * Encrypt plaintext using the supplied cipher map.
 * Only A-Z letters are encrypted; spaces and punctuation pass through unchanged.
 */
export function encryptText(plaintext: string, cipher: Record<string, string>): string {
  return plaintext
    .toUpperCase()
    .split('')
    .map((char) => cipher[char] ?? char)
    .join('');
}

/**
 * Return the sorted unique A-Z letters that appear in a string.
 */
export function getUniqueLetters(text: string): string[] {
  return [...new Set(text.toUpperCase().split('').filter((c) => /[A-Z]/.test(c)))].sort();
}
