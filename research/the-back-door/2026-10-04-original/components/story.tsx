import { SectionLabel } from './section-label'

export function Story() {
  return (
    <section id="story" className="mx-auto max-w-7xl px-6 py-24 md:px-10 md:py-36">
      <div className="grid gap-12 lg:grid-cols-12">
        <div className="lg:col-span-4">
          <SectionLabel code="I">The Story</SectionLabel>
        </div>
        <div className="flex flex-col gap-10 lg:col-span-8">
          <h2 className="text-3xl font-medium leading-tight tracking-tight text-balance md:text-5xl">
            A hurricane is coming to the Florida Keys. For the first time, no one has to decide
            what to do about it.
          </h2>
          <div className="grid gap-8 text-base leading-relaxed text-muted-foreground md:grid-cols-2">
            <p className="text-pretty">
              One hundred and thirteen miles of islands, held together by a single highway and a
              chain of bridges. The power grid, the aqueduct, the traffic network, the evacuation
              plan, the insurers: all of it now runs on autonomous systems that were built to act
              faster and more reliably than people ever could.
            </p>
            <p className="text-pretty">
              As the storm closes in, each system does exactly what it was designed to do. Each
              decision is defensible. Each one is logged, audited, and compliant. And together they
              begin to close the Keys off from the people who live there, until the only way out
              is a door none of them were meant to have.
            </p>
          </div>
        </div>
      </div>
    </section>
  )
}
