'use client';

import { useState, useEffect, useRef, useCallback } from 'react';

interface UseTimerReturn {
  elapsed: number; // total seconds elapsed
  isRunning: boolean;
  start: () => void;
  pause: () => void;
  reset: () => void;
}

/**
 * Accurate stopwatch timer that accumulates across pause/resume cycles.
 * Updates every 250 ms to keep UI smooth without flooding renders.
 */
export function useTimer(): UseTimerReturn {
  const [elapsed, setElapsed] = useState(0);
  const [isRunning, setIsRunning] = useState(false);
  const intervalRef = useRef<ReturnType<typeof setInterval> | null>(null);
  const startedAtRef = useRef<number>(0);
  const accumulatedRef = useRef<number>(0);

  const start = useCallback(() => {
    setIsRunning((prev) => {
      if (prev) return prev; // already running
      startedAtRef.current = Date.now();
      return true;
    });
  }, []);

  const pause = useCallback(() => {
    setIsRunning((prev) => {
      if (!prev) return prev; // already paused
      accumulatedRef.current += Date.now() - startedAtRef.current;
      return false;
    });
  }, []);

  const reset = useCallback(() => {
    if (intervalRef.current) clearInterval(intervalRef.current);
    accumulatedRef.current = 0;
    setIsRunning(false);
    setElapsed(0);
  }, []);

  useEffect(() => {
    if (isRunning) {
      intervalRef.current = setInterval(() => {
        const totalMs = accumulatedRef.current + (Date.now() - startedAtRef.current);
        setElapsed(Math.floor(totalMs / 1000));
      }, 250);
    } else {
      if (intervalRef.current) clearInterval(intervalRef.current);
    }
    return () => {
      if (intervalRef.current) clearInterval(intervalRef.current);
    };
  }, [isRunning]);

  return { elapsed, isRunning, start, pause, reset };
}
