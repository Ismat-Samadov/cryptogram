import Game from '@/components/Game';

/**
 * Root page — renders the full-screen Cryptogram game.
 * The Game component is a client component; this server component simply
 * wraps it so Next.js App Router is satisfied.
 */
export default function Home() {
  return <Game />;
}
