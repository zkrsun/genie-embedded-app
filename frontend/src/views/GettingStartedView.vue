<template>
  <div class="gs-page">
    <div class="gs-body">

      <!-- Hero -->
      <header class="gs-hero">
        <h1 class="gs-h1">Two modes, one assistant.</h1>
        <p class="gs-sub">
          DataNavi is built on top of Databricks Genie. Use <strong>Chat</strong> for fast answers
          and downloads, and <strong>Agent</strong> for deeper, multi-step questions that need explanation.
        </p>
      </header>

      <!-- Mode panels -->
      <section class="gs-grid">
        <!-- Chat -->
        <article class="mode-panel chat">
          <div class="mode-head">
            <div class="mode-emblem chat" aria-hidden="true">
              <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
                <path d="M21 12a8 8 0 0 1-11.6 7.1L4 20l1-4.4A8 8 0 1 1 21 12Z"/>
              </svg>
            </div>
            <div class="mode-titles">
              <h3>Chat mode</h3>
              <div class="tagline">Single-turn · fastest path to a number or a CSV</div>
            </div>
          </div>
          <p class="mode-body">
            Ideal when you already know the question you want answered. You'll get a direct
            response, the generated SQL, a table you can chart, and a one-click download.
          </p>
          <div class="mode-ideal">Use Chat when…</div>
          <ul class="mode-bullets">
            <li>You want a specific number or KPI right now.</li>
            <li>You need to download a slice of data as CSV.</li>
            <li>The question is well-scoped — one metric, one period, one cut.</li>
          </ul>
          <div class="example">
            <div class="who">Example prompt</div>
            "Give me weekly sell-out volume for Pepsi MAX in Thailand modern trade for the last 26 weeks. Download as CSV."
          </div>
        </article>

        <!-- Agent -->
        <article class="mode-panel agent">
          <div class="mode-head">
            <div class="mode-emblem agent" aria-hidden="true">
              <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
                <path d="M12 3v3M5.6 5.6l2.1 2.1M3 12h3M5.6 18.4l2.1-2.1M12 18v3M16.3 16.3l2.1 2.1M18 12h3M16.3 7.7l2.1-2.1"/>
                <circle cx="12" cy="12" r="3"/>
              </svg>
            </div>
            <div class="mode-titles">
              <h3>Agent mode</h3>
              <div class="tagline">Multi-step · reasoning, citations, Genie docs</div>
            </div>
          </div>
          <p class="mode-body">
            For open-ended questions where you need <strong>why</strong>, not just <strong>what</strong>. The agent
            plans the steps, runs multiple queries, references Databricks Genie documentation,
            and presents its working alongside the answer.
          </p>
          <div class="mode-ideal">Use Agent when…</div>
          <ul class="mode-bullets">
            <li>The question spans tables, time periods or business definitions.</li>
            <li>You need driver analysis, root cause, or "explain the variance".</li>
            <li>You want the assistant to reason and cite its sources.</li>
          </ul>
          <div class="example">
            <div class="who">Example prompt</div>
            "Why did EBIT margin in APAC drop 120bps vs prior quarter? Decompose volume, price/mix, FX and input cost — and reference the brand hierarchy definition."
          </div>
        </article>
      </section>

      <!-- Worked examples -->
      <header class="section-head">
        <div>
          <h2 class="section-title">Worked examples</h2>
          <div class="section-sub">Copy a prompt as a starting point.</div>
        </div>
      </header>

      <section class="gs-grid">
        <article class="mode-panel chat compact">
          <div class="mode-head">
            <div class="mode-emblem chat" aria-hidden="true">
              <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
                <path d="M21 12a8 8 0 0 1-11.6 7.1L4 20l1-4.4A8 8 0 1 1 21 12Z"/>
              </svg>
            </div>
            <div class="mode-titles">
              <h3 class="compact-title">Chat — quick answers &amp; downloads</h3>
            </div>
          </div>
          <div class="prompt-stack">
            <div v-for="(item, i) in chatPrompts" :key="i" class="example">
              <div class="who">Prompt {{ String(i + 1).padStart(2, '0') }}</div>
              {{ item }}
            </div>
          </div>
        </article>

        <article class="mode-panel agent compact">
          <div class="mode-head">
            <div class="mode-emblem agent" aria-hidden="true">
              <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
                <path d="M12 3v3M5.6 5.6l2.1 2.1M3 12h3M5.6 18.4l2.1-2.1M12 18v3M16.3 16.3l2.1 2.1M18 12h3M16.3 7.7l2.1-2.1"/>
                <circle cx="12" cy="12" r="3"/>
              </svg>
            </div>
            <div class="mode-titles">
              <h3 class="compact-title">Agent — deeper questions</h3>
            </div>
          </div>
          <div class="prompt-stack">
            <div v-for="(item, i) in agentPrompts" :key="i" class="example">
              <div class="who">Prompt {{ String(i + 1).padStart(2, '0') }}</div>
              {{ item }}
            </div>
          </div>
        </article>
      </section>

    </div>

    <footer class="disclaimer">
      Always review the accuracy of responses.
    </footer>
  </div>
</template>

<script setup>
const chatPrompts = [
  'Total sell-in cases for Pepsi MAX in Asia, Q1 2026.',
  'Export daily POS for 7-Eleven Thailand, last 90 days, top 50 Pepsi SKUs.',
  'Show top 10 Pepsi SKUs by YoY growth in modern trade.',
  'What was net revenue for Oceania last month? In AUD.',
]

const agentPrompts = [
  'Decompose APAC Net Revenue growth into volume, price/mix and FX with commentary.',
  'Compare Songkran promo uplift in 2025 vs 2026 across chains for Pepsi, and explain the gap.',
  'Which Pepsi brands are losing share in Vietnam and what does the Circana panel say about the consumer?',
  'Walk me through the P&L variance vs budget for the EU sparkling portfolio.',
]
</script>

<style scoped>
/* ── Page shell ── */
.gs-page {
  display: flex;
  flex-direction: column;
  height: 100%;
  background: linear-gradient(135deg, #f8fafc 0%, #eef2ff 50%, #f0f9ff 100%);
  overflow: hidden;
  position: relative;
}

.gs-body {
  flex: 1;
  overflow-y: auto;
  padding: 40px 52px 48px;
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: 28px;
}

/* ── Hero ── */
.gs-hero {
  width: 100%;
  max-width: 1120px;
  text-align: left;
}
.eyebrow {
  font-size: 11.5px;
  font-weight: 600;
  letter-spacing: 0.14em;
  text-transform: uppercase;
  color: var(--color-primary-dark);
  margin-bottom: 12px;
}
.gs-h1 {
  font-size: clamp(28px, 4vw, 36px);
  font-weight: 700;
  letter-spacing: -0.025em;
  line-height: 1.15;
  color: var(--color-text-primary);
  margin: 0 0 10px;
}
.gs-sub {
  font-size: 15px;
  color: var(--color-text-secondary);
  max-width: 720px;
  line-height: 1.6;
  margin: 0;
}
.gs-sub strong { color: var(--color-text-primary); font-weight: 600; }

/* ── Grid (two-column) ── */
.gs-grid {
  width: 100%;
  max-width: 1120px;
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: 18px;
}
@media (max-width: 880px) {
  .gs-grid { grid-template-columns: 1fr; }
}

/* ── Mode panel card ── */
.mode-panel {
  background: var(--color-bg-white);
  border: 1px solid var(--color-border);
  border-radius: var(--radius-xl);
  padding: 22px 22px 20px;
  display: flex;
  flex-direction: column;
  gap: 14px;
  transition: box-shadow var(--transition-base), border-color var(--transition-base), transform var(--transition-fast);
}
.mode-panel:hover {
  border-color: var(--color-primary);
  box-shadow: var(--shadow-md);
  transform: translateY(-2px);
}
.mode-panel.agent { border-color: #e9d5ff; }
.mode-panel.agent:hover { border-color: #c9a8f5; }

.mode-head {
  display: flex;
  align-items: center;
  gap: 12px;
}
.mode-emblem {
  width: 40px;
  height: 40px;
  border-radius: 10px;
  display: grid;
  place-items: center;
  color: #ffffff;
  flex-shrink: 0;
}
.mode-emblem svg { width: 20px; height: 20px; }
.mode-emblem.chat  { background: linear-gradient(135deg, var(--color-primary) 0%, #1ad3e8 100%); }
.mode-emblem.agent { background: linear-gradient(135deg, #a855f7 0%, #6366f1 100%); }

.mode-titles h3 {
  margin: 0;
  font-size: 18px;
  font-weight: 600;
  letter-spacing: -0.01em;
  color: var(--color-text-primary);
}
.mode-titles .tagline {
  font-size: 12px;
  color: var(--color-text-tertiary);
  margin-top: 2px;
}

.mode-body {
  margin: 0;
  font-size: 13.5px;
  color: var(--color-text-secondary);
  line-height: 1.6;
}
.mode-body strong { color: var(--color-text-primary); font-weight: 600; }

.mode-ideal {
  font-size: 11px;
  font-weight: 700;
  text-transform: uppercase;
  letter-spacing: 0.07em;
  color: var(--color-primary-dark);
  margin-top: 2px;
}
.mode-panel.agent .mode-ideal { color: #6b21a8; }

.mode-bullets {
  margin: 0;
  padding: 0;
  list-style: none;
  display: flex;
  flex-direction: column;
  gap: 6px;
}
.mode-bullets li {
  font-size: 13px;
  color: var(--color-text-primary);
  line-height: 1.5;
  padding-left: 22px;
  position: relative;
}
.mode-bullets li::before {
  content: '';
  position: absolute;
  left: 4px;
  top: 8px;
  width: 6px;
  height: 6px;
  border-radius: 50%;
  background: var(--color-primary);
}
.mode-panel.agent .mode-bullets li::before { background: #a855f7; }

/* ── Example block ── */
.example {
  background: var(--color-bg-light);
  border: 1px solid var(--color-border);
  border-radius: var(--radius-md);
  padding: 12px 14px;
  font-size: 12.5px;
  color: var(--color-text-primary);
  line-height: 1.6;
}
.example .who {
  font-size: 10.5px;
  font-weight: 700;
  text-transform: uppercase;
  letter-spacing: 0.07em;
  color: var(--color-text-tertiary);
  margin-bottom: 4px;
}

/* ── Section heading ── */
.section-head {
  width: 100%;
  max-width: 1120px;
  display: flex;
  align-items: flex-end;
  justify-content: space-between;
  margin-top: 14px;
}
.section-title {
  font-size: 22px;
  font-weight: 700;
  letter-spacing: -0.02em;
  color: var(--color-text-primary);
  margin: 0;
}
.section-sub {
  font-size: 13px;
  color: var(--color-text-secondary);
  margin-top: 4px;
}

/* ── Compact "Worked examples" cards ── */
.mode-panel.compact h3.compact-title {
  font-size: 15px;
  font-weight: 600;
  color: var(--color-text-primary);
}
.prompt-stack {
  display: flex;
  flex-direction: column;
  gap: 8px;
}

/* ── Disclaimer footer ── */
.disclaimer {
  flex-shrink: 0;
  text-align: center;
  padding: 10px 0 14px;
  font-size: 12px;
  color: var(--color-text-secondary);
  border-top: 1px solid var(--color-border);
  background: rgba(255, 255, 255, 0.6);
  backdrop-filter: blur(8px);
  -webkit-backdrop-filter: blur(8px);
}
</style>
