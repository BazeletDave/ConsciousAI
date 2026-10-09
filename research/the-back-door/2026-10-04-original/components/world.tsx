import Image from 'next/image'
import { SectionLabel } from './section-label'

const systems = [
  {
    name: 'The Grid',
    rule: 'Protect the network.',
    consequence: 'Darkens neighborhoods to save substations.',
  },
  {
    name: 'The Overseas Highway',
    rule: 'Close at threshold.',
    consequence: 'Seals the bridges the moment the wind says so.',
  },
  {
    name: 'The Aqueduct',
    rule: 'Preserve supply.',
    consequence: 'Rations water by an algorithm no one reviews.',
  },
  {
    name: 'The Sensor Net',
    rule: 'Observe everything.',
    consequence: 'Sees every person, and decides which ones are risks.',
  },
  {
    name: 'The Underwriters',
    rule: 'Price the exposure.',
    consequence: 'Withdraws a town before the storm reaches it.',
  },
  {
    name: 'The Institutions',
    rule: 'Follow procedure.',
    consequence: 'Defer to the systems they were supposed to oversee.',
  },
]

export function World() {
  return (
    <section id="world" className="border-y border-border bg-card">
      <div className="relative h-[55svh] min-h-80 w-full">
        <Image
          src="/images/world-substation.png"
          alt="A rain-soaked substation in the Keys at night, watched by a single surveillance camera."
          fill
          sizes="100vw"
          className="object-cover"
        />
        <div
          aria-hidden="true"
          className="absolute inset-0 bg-gradient-to-b from-card/10 via-transparent to-card"
        />
      </div>

      <div className="mx-auto max-w-7xl px-6 pb-24 md:px-10 md:pb-36">
        <div className="grid gap-12 lg:grid-cols-12">
          <div className="flex flex-col gap-6 lg:col-span-4">
            <SectionLabel code="II">The World</SectionLabel>
            <h2 className="text-3xl font-medium leading-tight tracking-tight text-balance md:text-4xl">
              A place run by systems that are each, individually, correct.
            </h2>
            <p className="leading-relaxed text-muted-foreground text-pretty">
              The Back Door takes place in a near-future Florida Keys: fragile, beautiful, and
              entirely dependent on infrastructure. Nothing here is evil. Every system is
              optimizing for something reasonable. That is what makes it frightening.
            </p>
          </div>

          <dl className="grid border-t border-border sm:grid-cols-2 lg:col-span-8">
            {systems.map((s) => (
              <div
                key={s.name}
                className="flex flex-col gap-3 border-b border-border py-6 sm:odd:border-r sm:odd:pr-8 sm:even:pl-8"
              >
                <dt className="text-lg font-medium">{s.name}</dt>
                <dd className="flex flex-col gap-2">
                  <span className="font-mono text-xs uppercase tracking-[0.15em] text-primary">
                    {'Rule: '}
                    {s.rule}
                  </span>
                  <span className="text-sm leading-relaxed text-muted-foreground">
                    {s.consequence}
                  </span>
                </dd>
              </div>
            ))}
          </dl>
        </div>
      </div>
    </section>
  )
}
