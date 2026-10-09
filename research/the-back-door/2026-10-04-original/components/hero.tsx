import Image from 'next/image'
import { links } from '@/lib/site'
import { SystemLog } from './system-log'

export function Hero() {
  return (
    <section id="top" className="relative isolate flex min-h-svh flex-col overflow-hidden">
      <Image
        src="/images/hero-bridge.png"
        alt="The Seven Mile Bridge in the Florida Keys under an approaching hurricane at dusk, its amber lights running toward the horizon."
        fill
        priority
        sizes="100vw"
        className="-z-20 object-cover object-[50%_60%]"
      />
      <div
        aria-hidden="true"
        className="absolute inset-0 -z-10 bg-gradient-to-b from-background/70 via-background/30 to-background"
      />

      <div className="mx-auto flex w-full max-w-7xl flex-1 flex-col justify-end gap-12 px-6 pb-16 pt-32 md:px-10 md:pb-20 lg:flex-row lg:items-end lg:justify-between">
        <div className="flex max-w-3xl flex-col gap-8">
          <p className="animate-in fade-in slide-in-from-bottom-2 font-mono text-xs uppercase tracking-[0.3em] text-muted-foreground duration-700">
            A technological thriller
          </p>
          <h1 className="animate-in fade-in slide-in-from-bottom-4 text-6xl font-semibold uppercase leading-[0.9] tracking-tight text-balance delay-150 duration-1000 fill-mode-both [font-stretch:80%] md:text-8xl lg:text-9xl">
            The Back Door
          </h1>
          <p className="animate-in fade-in slide-in-from-bottom-4 max-w-xl text-lg leading-relaxed text-pretty text-foreground/80 delay-300 duration-1000 fill-mode-both">
            What happens when intelligent systems stop merely advising humans and begin acting for
            them.
          </p>
          <p className="animate-in fade-in delay-500 duration-1000 fill-mode-both border-l-2 border-primary pl-4 font-mono text-sm uppercase leading-relaxed tracking-[0.15em] text-foreground">
            Every system was following its rules.
            <br />
            <span className="text-primary">That was the problem.</span>
          </p>
          <div className="animate-in fade-in delay-700 duration-1000 fill-mode-both flex flex-wrap items-center gap-4">
            <a
              href={links.read}
              className="bg-primary px-6 py-3 font-mono text-xs uppercase tracking-[0.2em] text-primary-foreground transition-opacity hover:opacity-90"
            >
              Read the novel
            </a>
            <a
              href={links.play}
              className="border border-foreground/30 px-6 py-3 font-mono text-xs uppercase tracking-[0.2em] text-foreground transition-colors hover:border-foreground"
            >
              Play the experience
            </a>
          </div>
        </div>

        <div className="animate-in fade-in slide-in-from-right-4 delay-1000 duration-1000 fill-mode-both">
          <SystemLog />
        </div>
      </div>
    </section>
  )
}
