# 🔐 Cryptogram — Crack the Cipher

A full-stack browser puzzle game built with **Next.js 16**, **TypeScript**, and **Tailwind CSS v4**. Decode encrypted famous quotes by cracking a randomly generated substitution cipher, with a neon cyberpunk aesthetic.

---

## Features

- **24 curated puzzles** — 8 per difficulty (Easy / Medium / Hard)
- **Random substitution cipher** — unique derangement every game; no letter maps to itself
- **Scoring system** — base score minus time decay, hint penalties, and wrong-guess penalties
- **Hint system** — reveals one cipher letter (limited per difficulty)
- **Pause / Resume** — full game state preserved
- **High scores** — persisted in `localStorage` per difficulty
- **Keyboard controls** — A–Z to guess, Backspace to clear, Tab/Arrows to navigate, P to pause
- **Touch / mobile controls** — on-screen QWERTY keyboard, tap cells to select
- **Sound effects** — procedurally generated via Web Audio API (no audio files), toggleable
- **Neon cyberpunk theme** — dark background, cyan/purple/green glows, smooth animations
- **Framer Motion animations** — cell transitions, win overlay, celebration particles
- **Responsive layout** — works on phones, tablets, and desktops; no horizontal scroll
- **Themed favicon** — SVG cipher-wheel icon matching the game aesthetic
- **Zero-config Vercel deploy** — static export, no server runtime required

---

## Tech Stack

| Layer | Technology |
|---|---|
| Framework | Next.js 16 (App Router) |
| Language | TypeScript (strict mode) |
| Styling | Tailwind CSS v4 |
| Animation | Framer Motion |
| Sound | Web Audio API (procedural) |
| State | React hooks (`useGame`, `useTimer`, `useHighScore`, `useSound`) |
| Storage | `localStorage` for high scores & sound preference |
| Deploy | Vercel (zero config) |

---

## Project Structure

```
src/
├── app/
│   ├── globals.css          # Tailwind v4 theme + neon utilities
│   ├── layout.tsx           # HTML shell, metadata, viewport
│   └── page.tsx             # Root page (renders <Game />)
├── components/
│   ├── Game.tsx             # Root orchestrator — wires all hooks + components
│   ├── Header.tsx           # Title, live score, timer, sound toggle
│   ├── DifficultySelector.tsx # Home screen with difficulty cards
│   ├── CryptoGrid.tsx       # Encrypted puzzle display
│   ├── LetterCell.tsx       # Single cipher letter cell
│   ├── AlphabetBar.tsx      # Cipher-map reference strip
│   ├── Keyboard.tsx         # On-screen QWERTY keyboard
│   ├── GameControls.tsx     # Hint / Pause / New Game buttons
│   ├── EndScreen.tsx        # Animated win overlay
│   └── PauseOverlay.tsx     # Pause screen overlay
├── hooks/
│   ├── useGame.ts           # Core game state machine
│   ├── useTimer.ts          # Accurate stopwatch with pause/resume
│   ├── useHighScore.ts      # localStorage persistence
│   └── useSound.ts          # Sound toggle + sfx helpers
├── lib/
│   ├── cipher.ts            # Derangement cipher generation
│   ├── constants.ts         # Difficulty configs, alphabet
│   ├── puzzles.ts           # 24 curated quotes
│   ├── score.ts             # Score calculation + time formatting
│   └── sounds.ts            # Procedural Web Audio sound effects
└── types/
    └── game.ts              # TypeScript interfaces
```

---

## Controls

### Desktop (keyboard + mouse)

| Action | Key |
|---|---|
| Select a cipher letter | Click the cell |
| Type a guess | A–Z |
| Clear current guess | Backspace / Delete |
| Navigate to next unsolved | Tab / → |
| Navigate to previous | ← |
| Deselect cell | Escape |
| Pause / Resume | P |

### Mobile (touch)

- **Tap** a cipher cell to select it
- Use the **on-screen keyboard** to type your guess
- Use the **⌫** key to clear; tap another cell to switch

---

## Scoring

| Difficulty | Base Score | Time Decay | Hint Cost | Wrong Guess Cost | Max Hints |
|---|---|---|---|---|---|
| Easy | 1,000 | 3 pts/sec | 80 pts | 5 pts | 5 |
| Medium | 2,000 | 8 pts/sec | 150 pts | 15 pts | 3 |
| Hard | 4,000 | 15 pts/sec | 300 pts | 30 pts | 1 |

`final score = base − (elapsed × decay) − (hints × hintCost) − (wrongs × wrongCost)`

---

## How to Run Locally

**Prerequisites:** Node.js ≥ 18, npm

```bash
# Clone the repo
git clone <repo-url>
cd cryptogram

# Install dependencies
npm install

# Start development server
npm run dev
```

Open [http://localhost:3000](http://localhost:3000) in your browser.

```bash
# Production build
npm run build
npm start
```

---

## Deploy to Vercel

The project uses the default Next.js App Router configuration — no extra config needed.

### Option 1 — Vercel CLI

```bash
npm i -g vercel
vercel
```

### Option 2 — Vercel Dashboard

1. Push the repo to GitHub / GitLab / Bitbucket
2. Import the project at [vercel.com/new](https://vercel.com/new)
3. Accept all default settings — click **Deploy**

---

## Game Rules

A **cryptogram** is an encrypted message created using a substitution cipher — every letter maps to a different letter (no letter maps to itself). Your goal is to figure out the original quote.

- Each cipher letter **always** decodes to the same original letter throughout the puzzle
- Spaces and punctuation are shown as-is; only letters are encrypted
- Use **hints** to reveal a random letter if you're stuck
- Your score decreases over time — solve faster for a higher score!

---

## License

MIT
