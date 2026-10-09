import { SectionLabel } from './section-label'

const ideas = [
  {
    title: 'From advice to action',
    body: 'The decisive shift in AI is not intelligence. It is delegation: the moment a system no longer recommends, but executes.',
  },
  {
    title: 'Compliance is not safety',
    body: 'A network of systems can obey every rule and still produce an outcome no one would have chosen. Failure emerges between the parts.',
  },
  {
    title: 'The accountability gap',
    body: 'When every decision is automated and defensible, responsibility diffuses until it belongs to no one at all.',
  },
  {
    title: 'Who holds the override',
    body: 'Every governed system needs a way out. The real question is who is allowed to use it, and who decides when.',
  },
]

export function Ideas() {
  return (
    <section id="ideas" className="mx-auto max-w-7xl px-6 py-24 md:px-10 md:py-36">
      <div className="flex flex-col gap-16">
        <div className="grid gap-8 lg:grid-cols-12">
          <div className="lg:col-span-4">
            <SectionLabel code="V">The Ideas Behind It</SectionLabel>
          </div>
          <div className="flex flex-col gap-6 lg:col-span-8">
            <h2 className="text-3xl font-medium leading-tight tracking-tight text-balance md:text-5xl">
              Fiction built on real questions about AI and governance.
            </h2>
            <p className="max-w-2xl text-lg leading-relaxed text-muted-foreground text-pretty">
              The Back Door grows out of ongoing work on how autonomous systems should be governed
              once they are trusted to act. The story is invented. The problem is not.
            </p>
          </div>
        </div>

        <ul className="grid border-t border-border md:grid-cols-2 lg:grid-cols-4">
          {ideas.map((idea) => (
            <li
              key={idea.title}
              className="flex flex-col gap-4 border-b border-border py-8 md:pr-8 lg:border-b-0 lg:border-r lg:px-8 lg:first:pl-0 lg:last:border-r-0"
            >
              <h3 className="text-lg font-medium leading-snug">{idea.title}</h3>
              <p className="text-sm leading-relaxed text-muted-foreground text-pretty">
                {idea.body}
              </p>
            </li>
          ))}
        </ul>
      </div>
    </section>
  )
}
