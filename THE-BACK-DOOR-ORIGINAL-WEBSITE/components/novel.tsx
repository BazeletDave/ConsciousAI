import Image from 'next/image'
import { links } from '@/lib/site'
import { SectionLabel } from './section-label'

export function Novel() {
  return (
    <section id="novel" className="mx-auto max-w-7xl px-6 py-24 md:px-10 md:py-36">
      <div className="grid items-center gap-16 lg:grid-cols-12">
        <div className="relative mx-auto w-full max-w-sm lg:col-span-5 lg:mx-0">
          <div className="relative aspect-[2/3] w-full shadow-2xl shadow-background">
            <Image
              src="/images/the-back-door-cover.jpg"
              alt="The Back Door by David Grand, official novel cover."
              fill
              sizes="(min-width: 1024px) 384px, 90vw"
              className="object-contain"
            />
          </div>
        </div>

        <div className="flex flex-col gap-8 lg:col-span-6 lg:col-start-7">
          <SectionLabel code="III">The Novel</SectionLabel>
          <h2 className="text-3xl font-medium leading-tight tracking-tight text-balance md:text-5xl">
            The foundation of the universe.
          </h2>
          <p className="text-lg leading-relaxed text-foreground/80 text-pretty">
            Told across a single storm, The Back Door follows the people caught inside a region
            that has quietly handed its judgment to machines: the engineers who built the systems,
            the officials who signed off on them, and the residents who discover that no one is
            actually in charge.
          </p>
          <p className="leading-relaxed text-muted-foreground text-pretty">
            It is a thriller about infrastructure and power, about the gap between what is
            permitted and what is right, and about who gets to open the door when the rules
            say it must stay closed.
          </p>
          <div className="flex flex-wrap items-center gap-6">
            <a
              href={links.read}
              className="bg-primary px-6 py-3 font-mono text-xs uppercase tracking-[0.2em] text-primary-foreground transition-opacity hover:opacity-90"
            >
              Read the novel
            </a>
            <span className="font-mono text-xs uppercase tracking-[0.2em] text-muted-foreground">
              Forthcoming
            </span>
          </div>
        </div>
      </div>
    </section>
  )
}
