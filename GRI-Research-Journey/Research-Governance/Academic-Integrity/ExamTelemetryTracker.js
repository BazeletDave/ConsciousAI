/** Research-only browser event collector. No clipboard content is stored. */
export class ExamTelemetryTracker {
  constructor({ sessionId, onTelemetryUpdate, studentNoticeAccepted = false } = {}) {
    if (!studentNoticeAccepted) throw new Error("Assessment telemetry requires confirmed notice");
    this.sessionId = sessionId || `session_${Date.now()}`;
    this.onTelemetryUpdate = onTelemetryUpdate;
    this.active = true;
    this.tabSwitchesCount = 0;
    this.eventLog = [];
    this.handlers = {
      visibilitychange: () => {
        if (document.hidden) this.tabSwitchesCount++;
        this.record(document.hidden ? "TAB_HIDDEN" : "TAB_VISIBLE");
      },
      blur: () => this.record("WINDOW_BLUR"),
      focus: () => this.record("WINDOW_FOCUS"),
      paste: (event) => {
        // No clipboard reads: even snippets can reveal personal information.
        this.record("PASTE_EVENT", { clipboardCharacterCount: null });
      },
      copy: () => this.record("COPY_EVENT")
    };
    document.addEventListener("visibilitychange", this.handlers.visibilitychange);
    window.addEventListener("blur", this.handlers.blur);
    window.addEventListener("focus", this.handlers.focus);
    document.addEventListener("paste", this.handlers.paste);
    document.addEventListener("copy", this.handlers.copy);
  }
  record(eventType, details = {}) {
    if (!this.active) return;
    const payload = {
      sessionId: this.sessionId,
      timestamp: new Date().toISOString(),
      eventType,
      tabSwitchesCount: this.tabSwitchesCount,
      ...details
    };
    this.eventLog.push(payload);
    if (typeof this.onTelemetryUpdate === "function") this.onTelemetryUpdate(payload);
  }
  destroy() {
    document.removeEventListener("visibilitychange", this.handlers.visibilitychange);
    window.removeEventListener("blur", this.handlers.blur);
    window.removeEventListener("focus", this.handlers.focus);
    document.removeEventListener("paste", this.handlers.paste);
    document.removeEventListener("copy", this.handlers.copy);
    this.active = false;
    this.eventLog.length = 0;
  }
}
