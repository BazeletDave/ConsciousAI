import Image from 'next/image'
import { links } from '@/lib/site'
import { SectionLabel } from './section-label'

const roles = [
  { role: 'Operators', brief: 'Run a system. Follow its mandate. Defend every decision.' },
  { role: 'Officials', brief: 'Hold the authority, but not the information.' },
  { role: 'Residents', brief: 'Live with the outcome. Look for a way through.' },
]

export function Experience() {
  return (
    <section id="play" className="relative isolate overflow-hidden border-y border-border">
      <Image
        src="/images/game-control-room.png"
        alt=""
        fill
        sizes="100vw"
        className="-z-20 object-cover"
      />
      <div aria-hidden="true" className="absolute inset-0 -z-10 bg-background/85" />

      <div className="mx-auto grid max-w-7xl gap-16 px-6 py-24 md:px-10 md:py-36 lg:grid-cols-12">
        <div className="flex flex-col gap-8 lg:col-span-6">
          <SectionLabel code="IV">The Playable Experience</SectionLabel>
          <h2 className="text-3xl font-medium leading-tight tracking-tight text-balance md:text-5xl">
            Don&apos;t read about the problem. Be part of it.
          </h2>
          <p className="text-lg leading-relaxed text-foreground/80 text-pretty">
            A multiplayer extension of the novel. Each player takes a seat inside the Keys as the
            storm approaches, with their own rules, their own information, and their own
            incentives. Everyone plays correctly. The question is whether anyone can stop what
            happens next.
          </p>
          <div className="flex flex-wrap items-center gap-6">
            <a
              href={links.play}
              className="border border-primary px-6 py-3 font-mono text-xs uppercase tracking-[0.2em] text-primary transition-colors hover:bg-primary hover:text-primary-foreground"
            >
              Play the experience
            </a>
            <span className="font-mono text-xs uppercase tracking-[0.2em] text-muted-foreground">
              In development
            </span>
          </div>
        </div>

        <ul className="flex flex-col self-end border-t border-border lg:col-span-5 lg:col-start-8">
          {roles.map((r) => (
            <li key={r.role} className="flex flex-col gap-1 border-b border-border py-6">
              <span className="font-mono text-xs uppercase tracking-[0.2em] text-primary">
                {r.role}
              </span>
              <span className="leading-relaxed text-foreground/80">{r.brief}</span>
            </li>
          ))}
        </ul>
      </div>
    </section>
  )
}
