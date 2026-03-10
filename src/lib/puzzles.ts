import type { Difficulty, Puzzle } from '@/types/game';

export const PUZZLES: Puzzle[] = [
  // ── Easy ──────────────────────────────────────────────────────────────────
  {
    id: 'e1',
    text: 'ACTIONS SPEAK LOUDER THAN WORDS',
    author: 'Abraham Lincoln',
    category: 'Wisdom',
    difficulty: 'easy',
  },
  {
    id: 'e2',
    text: 'BE YOURSELF EVERYONE ELSE IS ALREADY TAKEN',
    author: 'Oscar Wilde',
    category: 'Humor',
    difficulty: 'easy',
  },
  {
    id: 'e3',
    text: 'TO ERR IS HUMAN TO FORGIVE IS DIVINE',
    author: 'Alexander Pope',
    category: 'Wisdom',
    difficulty: 'easy',
  },
  {
    id: 'e4',
    text: 'KNOWLEDGE IS POWER AND POWER IS FREEDOM',
    author: 'Francis Bacon',
    category: 'Philosophy',
    difficulty: 'easy',
  },
  {
    id: 'e5',
    text: 'THE ONLY WAY OUT IS THROUGH',
    author: 'Robert Frost',
    category: 'Perseverance',
    difficulty: 'easy',
  },
  {
    id: 'e6',
    text: 'DREAM BIG START SMALL ACT NOW',
    author: 'Robin Sharma',
    category: 'Action',
    difficulty: 'easy',
  },
  {
    id: 'e7',
    text: 'WELL DONE IS BETTER THAN WELL SAID',
    author: 'Benjamin Franklin',
    category: 'Wisdom',
    difficulty: 'easy',
  },
  {
    id: 'e8',
    text: 'WHERE THERE IS WILL THERE IS A WAY',
    category: 'Proverb',
    difficulty: 'easy',
  },

  // ── Medium ────────────────────────────────────────────────────────────────
  {
    id: 'm1',
    text: 'IN THE MIDDLE OF EVERY DIFFICULTY LIES OPPORTUNITY',
    author: 'Albert Einstein',
    category: 'Inspiration',
    difficulty: 'medium',
  },
  {
    id: 'm2',
    text: 'IT DOES NOT MATTER HOW SLOWLY YOU GO AS LONG AS YOU DO NOT STOP',
    author: 'Confucius',
    category: 'Perseverance',
    difficulty: 'medium',
  },
  {
    id: 'm3',
    text: 'THE FUTURE BELONGS TO THOSE WHO BELIEVE IN THE BEAUTY OF THEIR DREAMS',
    author: 'Eleanor Roosevelt',
    category: 'Dreams',
    difficulty: 'medium',
  },
  {
    id: 'm4',
    text: 'WHEN YOU REACH THE END OF YOUR ROPE TIE A KNOT IN IT AND HANG ON',
    author: 'Franklin D Roosevelt',
    category: 'Resilience',
    difficulty: 'medium',
  },
  {
    id: 'm5',
    text: 'ALWAYS REMEMBER THAT YOU ARE ABSOLUTELY UNIQUE JUST LIKE EVERYONE ELSE',
    author: 'Margaret Mead',
    category: 'Humor',
    difficulty: 'medium',
  },
  {
    id: 'm6',
    text: 'THE ONLY IMPOSSIBLE JOURNEY IS THE ONE YOU NEVER BEGIN',
    author: 'Tony Robbins',
    category: 'Journey',
    difficulty: 'medium',
  },
  {
    id: 'm7',
    text: 'SPREAD LOVE EVERYWHERE YOU GO LET NO ONE EVER COME TO YOU WITHOUT LEAVING HAPPIER',
    author: 'Mother Teresa',
    category: 'Love',
    difficulty: 'medium',
  },
  {
    id: 'm8',
    text: 'SUCCESS IS NOT FINAL FAILURE IS NOT FATAL IT IS THE COURAGE TO CONTINUE THAT COUNTS',
    author: 'Winston Churchill',
    category: 'Success',
    difficulty: 'medium',
  },

  // ── Hard ──────────────────────────────────────────────────────────────────
  {
    id: 'h1',
    text: 'TWENTY YEARS FROM NOW YOU WILL BE MORE DISAPPOINTED BY THE THINGS THAT YOU DID NOT DO THAN BY THE ONES YOU DID',
    author: 'Mark Twain',
    category: 'Regret',
    difficulty: 'hard',
  },
  {
    id: 'h2',
    text: 'IF YOU LOOK AT WHAT YOU HAVE IN LIFE YOU WILL ALWAYS HAVE MORE IF YOU LOOK AT WHAT YOU DO NOT HAVE YOU WILL NEVER HAVE ENOUGH',
    author: 'Oprah Winfrey',
    category: 'Gratitude',
    difficulty: 'hard',
  },
  {
    id: 'h3',
    text: 'WHEN I WAS YOUNG I OBSERVED THAT NINE OUT OF TEN THINGS I DID WERE FAILURES SO I DID TEN TIMES MORE WORK',
    author: 'George Bernard Shaw',
    category: 'Work',
    difficulty: 'hard',
  },
  {
    id: 'h4',
    text: 'THE GREATEST GLORY IN LIVING LIES NOT IN NEVER FALLING BUT IN RISING EVERY TIME WE FALL',
    author: 'Nelson Mandela',
    category: 'Resilience',
    difficulty: 'hard',
  },
  {
    id: 'h5',
    text: 'DO NOT GO WHERE THE PATH MAY LEAD GO INSTEAD WHERE THERE IS NO PATH AND LEAVE A TRAIL FOR OTHERS TO FOLLOW',
    author: 'Ralph Waldo Emerson',
    category: 'Leadership',
    difficulty: 'hard',
  },
  {
    id: 'h6',
    text: 'IT IS DURING OUR DARKEST MOMENTS THAT WE MUST FOCUS TO SEE THE LIGHT AND TRUST THAT DAWN WILL COME',
    author: 'Aristotle Onassis',
    category: 'Hope',
    difficulty: 'hard',
  },
  {
    id: 'h7',
    text: 'THE MIND IS EVERYTHING WHAT YOU THINK YOU BECOME AND WHAT YOU BECOME SHAPES THE WORLD AROUND YOU',
    author: 'Buddha',
    category: 'Mindset',
    difficulty: 'hard',
  },
  {
    id: 'h8',
    text: 'HAPPINESS IS NOT SOMETHING READY MADE IT COMES FROM YOUR OWN ACTIONS AND EVERY CHOICE YOU MAKE DEFINES YOUR PATH',
    author: 'Dalai Lama',
    category: 'Happiness',
    difficulty: 'hard',
  },
];

/** Return all puzzles for a given difficulty */
export function getPuzzlesByDifficulty(difficulty: Difficulty): Puzzle[] {
  return PUZZLES.filter((p) => p.difficulty === difficulty);
}

/** Pick a random puzzle for the given difficulty */
export function getRandomPuzzle(difficulty: Difficulty): Puzzle {
  const pool = getPuzzlesByDifficulty(difficulty);
  return pool[Math.floor(Math.random() * pool.length)];
}
