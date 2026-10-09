'use client'

import { useEffect, useState } from 'react'

const entries = [
  { t: '03:12:04', sys: 'GRID.KEYS', act: 'Load shed — Marathon, sector 7' },
  { t: '03:12:09', sys: 'US1.TRAFFIC', act: 'Bridge closed — sustained wind 61 kt' },
  { t: '03:12:15', sys: 'WATER.AQUEDUCT', act: 'Pressure reduced — Lower Keys' },
  { t: '03:12:22', sys: 'EVAC.ROUTING', act: 'Reroute denied — capacity rule 4.2' },
  { t: '03:12:30', sys: 'SENSOR.NET', act: 'Human override request — logged' },
  { t: '03:12:41', sys: 'RISK.UNDERWRITE', act: 'Coverage suspended — zone AE' },
  { t: '03:12:47', sys: 'COMMS.ALERT', act: 'Advisory deferred — confidence 0.61' },
  { t: '03:12:58', sys: 'MEDEVAC.DISPATCH', act: 'Request queued — priority recalculated' },
]

const VISIBLE = 5

export function SystemLog() {
  const [offset, setOffset] = useState(0)

  useEffect(() => {
    if (window.matchMedia('(prefers-reduced-motion: reduce)').matches) return
    const id = window.setInterval(() => setOffset((o) => (o + 1) % entries.length), 2600)
    return () => window.clearInterval(id)
  }, [])

  const rows = Array.from({ length: VISIBLE }, (_, i) => entries[(offset + i) % entries.length])

  return (
    <div
      className="w-full max-w-md border border-border bg-background/70 backdrop-blur-md"
      role="img"
      aria-label="Simulated autonomous systems log. Every action is marked compliant."
    >
      <div className="flex items-center justify-between border-b border-border px-4 py-2 font-mono text-[11px] uppercase tracking-[0.2em] text-muted-foreground">
        <span>Keys Autonomy Layer</span>
        <span className="flex items-center gap-2">
          <span aria-hidden="true" className="size-1.5 animate-pulse rounded-full bg-primary" />
          Live
        </span>
      </div>
      <ol aria-hidden="true" className="flex flex-col font-mono text-[11px] leading-relaxed">
        {rows.map((row, i) => (
          <li
            key={`${row.t}-${offset}-${i}`}
            className={`grid grid-cols-[auto_1fr_auto] items-baseline gap-3 border-b border-border/50 px-4 py-2 last:border-b-0 ${
              i === VISIBLE - 1 ? 'animate-in fade-in slide-in-from-bottom-1 duration-500' : ''
            }`}
            style={{ opacity: 0.45 + (i / (VISIBLE - 1)) * 0.55 }}
          >
            <span className="text-muted-foreground">{row.t}</span>
            <span className="min-w-0">
              <span className="block text-foreground">{row.sys}</span>
              <span className="block truncate text-muted-foreground">{row.act}</span>
            </span>
            <span className="text-primary">Compliant</span>
          </li>
        ))}
      </ol>
    </div>
  )
}
