'use client';

import { motion, AnimatePresence } from 'framer-motion';

interface PauseOverlayProps {
  visible: boolean;
  onResume: () => void;
}

/** Semi-transparent overlay shown when the game is paused */
export default function PauseOverlay({ visible, onResume }: PauseOverlayProps) {
  return (
    <AnimatePresence>
      {visible && (
        <motion.div
          initial={{ opacity: 0 }}
          animate={{ opacity: 1 }}
          exit={{ opacity: 0 }}
          onClick={onResume}
          className="absolute inset-0 z-20 flex flex-col items-center justify-center bg-slate-950/90 backdrop-blur-sm rounded-xl cursor-pointer"
        >
          <motion.div
            initial={{ scale: 0.8 }}
            animate={{ scale: 1 }}
            exit={{ scale: 0.8 }}
            className="text-center"
          >
            <div className="text-5xl mb-4">⏸</div>
            <p className="font-mono font-black text-xl text-cyan-400 mb-2">PAUSED</p>
            <p className="font-mono text-slate-400 text-sm">Click anywhere to resume</p>
          </motion.div>
        </motion.div>
      )}
    </AnimatePresence>
  );
}
