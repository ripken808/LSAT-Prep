"use client";

import { useEffect, useState } from "react";

/** Seconds remaining until `deadline`, ticking once a second.
 *
 * Driven by a deadline timestamp rather than by decrementing a counter: a
 * backgrounded tab throttles intervals, so a counter would drift and hand back
 * time the test taker didn't have. Comparing against Date.now() stays correct
 * no matter how irregularly the interval fires. Returns 0 once expired.
 */
function secondsUntil(deadline: number | null): number {
  return deadline === null
    ? 0
    : Math.max(0, Math.ceil((deadline - Date.now()) / 1000));
}

export function useCountdown(deadline: number | null): number {
  // Track the deadline alongside the value and recompute DURING RENDER when it
  // changes, rather than waiting for an effect. Without this the hook returns a
  // stale 0 on the first render after a new deadline is set — and a caller that
  // treats 0 as "time is up" would end the section the instant it began. That
  // is exactly the bug this shape prevents; don't simplify it back to a plain
  // useState + useEffect.
  const [state, setState] = useState(() => ({
    deadline,
    remaining: secondsUntil(deadline),
  }));

  if (state.deadline !== deadline) {
    setState({ deadline, remaining: secondsUntil(deadline) });
  }

  useEffect(() => {
    if (deadline === null) return;
    const tick = () =>
      setState({ deadline, remaining: secondsUntil(deadline) });
    tick();
    const id = setInterval(tick, 1000);
    return () => clearInterval(id);
  }, [deadline]);

  return state.deadline === deadline ? state.remaining : secondsUntil(deadline);
}

export function formatClock(totalSeconds: number): string {
  const minutes = Math.floor(totalSeconds / 60);
  const seconds = totalSeconds % 60;
  return `${minutes}:${String(seconds).padStart(2, "0")}`;
}

export function TimerDisplay({ seconds }: { seconds: number }) {
  const urgent = seconds <= 60;
  return (
    <span
      className="result-chip"
      style={{
        background: urgent ? "var(--status-critical)" : undefined,
        fontVariantNumeric: "tabular-nums",
      }}
      // Announce politely so a screen reader isn't interrupted every second.
      aria-live="polite"
      aria-label={`${Math.floor(seconds / 60)} minutes ${seconds % 60} seconds remaining`}
    >
      {formatClock(seconds)}
    </span>
  );
}
