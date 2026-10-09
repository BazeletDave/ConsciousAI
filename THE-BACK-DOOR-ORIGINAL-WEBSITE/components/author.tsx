import Image from 'next/image'
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
          <div className="grid gap-6 sm:grid-cols-2">
            <div className="flex flex-col gap-3">
              <Image src="/images/from-code-to-consciousness-cover.jpg" alt="From Code to Consciousness by David Grand, print cover." width={606} height={903} className="h-80 w-full object-contain" />
              <p className="text-sm text-muted-foreground">From Code to Consciousness</p>
            </div>
            <div className="flex flex-col gap-3">
              <Image src="/images/from-code-to-consciousness-audio.jpg" alt="From Code to Consciousness, audiobook artwork." width={936} height={968} className="h-80 w-full object-contain" />
              <p className="text-sm text-muted-foreground">Available on Amazon and Audible</p>
            </div>
          </div>
          <div className="flex flex-col gap-6 leading-relaxed text-muted-foreground">
            <p className="text-pretty">
              David Grand is the author of <em>From Code to Consciousness</em>, his first
              publication through the Grand Research Institute, available today on Amazon
              and Audible. His work spans multiple decades and industries, connecting
              global business, leadership, artificial intelligence, and institutional governance.
            </p>
            <p className="text-pretty">
              He graduated magna cum laude with a degree in global management from
              Thunderbird School of Global Management at Arizona State University.
              He is currently completing a master&apos;s in leadership and management
              with a specialization in artificial intelligence at Thunderbird.
            </p>
            <p className="text-pretty">
              Grand founded the Grand Research Institute in Florida as a living ecosystem
              for his research journey, bringing scholarship, business experience, and
              practical experimentation together. His upcoming novel, <em>The Back Door</em>,
              extends that inquiry into fiction, exploring a world that feels closer to
              reality every day.
            </p>
            <p className="text-sm text-pretty">
              Arizona State University has been ranked No. 1 in the U.S. for innovation
              by U.S. News &amp; World Report for 12 consecutive years. Thunderbird is
              ranked No. 1 in the world for international trade in the 2026 QS International
              Trade Rankings.
              {' '}
              <a href="https://news.asu.edu/20260921-university-news-asu-no-1-innovation-12th-year" className="underline underline-offset-4">ASU rankings</a>
              {' · '}
              <a href="https://thunderbird.asu.edu/about/rankings-and-accreditation" className="underline underline-offset-4">Thunderbird rankings</a>
            </p>
          </div>
          <Image src="/images/from-code-to-consciousness-promotion.jpg" alt="From Code to Consciousness by David Grand, available on Amazon and Audible." width={782} height={857} className="mx-auto h-auto w-full max-w-lg" />
        </div>
      </div>
    </section>
  )
}
