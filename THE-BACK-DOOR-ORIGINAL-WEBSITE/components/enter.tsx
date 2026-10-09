import { ArrowUpRight } from 'lucide-react'
import { links } from '@/lib/site'

const doors = [
  { verb: 'Enter', object: 'the world', href: links.enter },
  { verb: 'Play', object: 'the experience', href: links.play },
  { verb: 'Read', object: 'the novel', href: links.read },
]

const horizon = ['Novel', 'Multiplayer experience', 'Film', 'Interactive', 'What comes next']

export function Enter() {
  return (
    <section aria-labelledby="enter-heading" className="border-t border-border">
      <div className="mx-auto max-w-7xl px-6 py-24 md:px-10 md:py-32">
        <h2
          id="enter-heading"
          className="mb-12 font-mono text-xs uppercase tracking-[0.3em] text-muted-foreground"
        >
          Choose a door
        </h2>
        <ul className="flex flex-col border-t border-border">
          {doors.map((d) => (
            <li key={d.verb}>
              <a
                href={d.href}
                className="group flex items-center justify-between gap-6 border-b border-border py-8 transition-colors hover:text-primary"
              >
                <span className="flex flex-wrap items-baseline gap-x-4">
                  <span className="text-5xl font-semibold uppercase leading-none tracking-tight [font-stretch:80%] md:text-8xl">
                    {d.verb}
                  </span>
                  <span className="text-lg text-muted-foreground transition-colors group-hover:text-primary/80 md:text-2xl">
                    {d.object}
                  </span>
                </span>
                <ArrowUpRight
                  aria-hidden="true"
                  className="size-8 shrink-0 transition-transform group-hover:-translate-y-1 group-hover:translate-x-1 md:size-12"
                  strokeWidth={1.25}
                />
              </a>
            </li>
          ))}
        </ul>

        <div className="mt-16 flex flex-col gap-4 md:flex-row md:items-center md:justify-between">
          <p className="font-mono text-xs uppercase tracking-[0.2em] text-muted-foreground">
            The universe
          </p>
          <ul className="flex flex-wrap gap-x-6 gap-y-2 font-mono text-xs uppercase tracking-[0.15em]">
            {horizon.map((h, i) => (
              <li key={h} className={i < 2 ? 'text-foreground' : 'text-muted-foreground'}>
                {h}
              </li>
            ))}
          </ul>
        </div>
      </div>
    </section>
  )
}
