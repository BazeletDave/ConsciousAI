export function SiteFooter() {
  return (
    <footer className="border-t border-border">
      <div className="mx-auto flex max-w-7xl flex-col gap-4 px-6 py-10 font-mono text-xs uppercase tracking-[0.2em] text-muted-foreground md:flex-row md:items-center md:justify-between md:px-10">
        <p>
          {'© '}
          {new Date().getFullYear()} David Grand. The Back Door.
        </p>
        <p>Every system was following its rules.</p>
      </div>
    </footer>
  )
}
