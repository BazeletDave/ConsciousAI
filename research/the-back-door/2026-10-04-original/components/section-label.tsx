import { cn } from '@/lib/utils'

export function SectionLabel({
  code,
  children,
  className,
}: {
  code: string
  children: React.ReactNode
  className?: string
}) {
  return (
    <p
      className={cn(
        'flex items-center gap-3 font-mono text-xs uppercase tracking-[0.2em] text-muted-foreground',
        className,
      )}
    >
      <span className="text-primary">{code}</span>
      <span aria-hidden="true" className="h-px w-8 bg-border" />
      <span>{children}</span>
    </p>
  )
}
