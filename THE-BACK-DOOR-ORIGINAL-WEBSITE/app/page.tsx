import { Author } from '@/components/author'
import { Enter } from '@/components/enter'
import { Experience } from '@/components/experience'
import { Hero } from '@/components/hero'
import { Ideas } from '@/components/ideas'
import { Novel } from '@/components/novel'
import { SiteFooter } from '@/components/site-footer'
import { SiteHeader } from '@/components/site-header'
import { Story } from '@/components/story'
import { World } from '@/components/world'

export default function Page() {
  return (
    <>
      <SiteHeader />
      <main>
        <Hero />
        <Story />
        <World />
        <Novel />
        <Experience />
        <Ideas />
        <Author />
        <Enter />
      </main>
      <SiteFooter />
    </>
  )
}
