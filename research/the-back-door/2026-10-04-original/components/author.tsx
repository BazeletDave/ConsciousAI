import { SectionLabel } from './section-label'

export function Author() {
  return (
    <section id="author" className="border-t border-border bg-card">
      <div className="mx-auto grid max-w-7xl gap-12 px-6 py-24 md:px-10 md:py-36 lg:grid-cols-12">
        <div className="lg:col-span-4">
          <SectionLabel code="VI">The Author</SectionLabel>
        </div>
        <div className="flex flex-col gap-8 lg:col-span-8">
          <h2 className="text-5xl font-semibold uppercase leading-none tracking-tight [font-stretch:80%] md:text-7xl">
            David Grand
          </h2>
          <div className="grid gap-8 leading-relaxed text-muted-foreground md:grid-cols-2">
            <p className="text-pretty">
              David Grand works at the intersection of artificial intelligence and governance,
              examining how institutions keep control of systems that increasingly act on their
              behalf.
            </p>
            <p className="text-pretty">
              The Back Door is his way of making that work felt rather than argued: a novel first,
              then a world others can step into. The assignment may end with a website. The Back
              Door does not.
            </p>
          </div>
        </div>
      </div>
    </section>
  )
}
