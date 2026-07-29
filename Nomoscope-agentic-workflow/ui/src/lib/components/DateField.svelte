<script>
  // ISO date field with a calendar popover we own, because the native
  // <input type="date"> picker (WebKitGTK) only closes on Escape — this one
  // also closes on any click outside. Typing an ISO date stays possible.
  let { value = $bindable(''), placeholder = 'YYYY-MM-DD' } = $props();

  const ISO = /^\d{4}-\d{2}-\d{2}$/;
  const WEEKDAYS = ['Mo', 'Tu', 'We', 'Th', 'Fr', 'Sa', 'Su'];

  let open = $state(false);
  let up = $state(false);
  let view = $state({ y: 2000, m: 0 });
  let root;

  const pad = (n) => String(n).padStart(2, '0');
  const iso = (y, m, d) => `${y}-${pad(m + 1)}-${pad(d)}`;

  function todayIso() {
    const now = new Date();
    return iso(now.getFullYear(), now.getMonth(), now.getDate());
  }

  const valid = $derived(value === '' || ISO.test(value));
  const monthLabel = $derived(
    new Intl.DateTimeFormat('en-GB', { month: 'long', year: 'numeric', timeZone: 'UTC' }).format(
      new Date(Date.UTC(view.y, view.m, 1)),
    ),
  );

  // leading blanks + day numbers, Monday-first
  const grid = $derived.by(() => {
    const lead = (new Date(Date.UTC(view.y, view.m, 1)).getUTCDay() + 6) % 7;
    const days = new Date(Date.UTC(view.y, view.m + 1, 0)).getUTCDate();
    const cells = Array.from({ length: lead }, () => null);
    for (let d = 1; d <= days; d += 1) cells.push(d);
    return cells;
  });

  function toggle(event) {
    if (open) {
      open = false;
      return;
    }
    const base = ISO.test(value) ? value : todayIso();
    view = { y: Number(base.slice(0, 4)), m: Number(base.slice(5, 7)) - 1 };
    // flip upwards when there is no room below (the panel scrolls)
    const rect = event.currentTarget.getBoundingClientRect();
    up = rect.bottom + 290 > window.innerHeight;
    open = true;
  }

  function shiftMonth(delta) {
    const m = view.m + delta;
    view = { y: view.y + Math.floor(m / 12), m: ((m % 12) + 12) % 12 };
  }

  function pick(day) {
    value = iso(view.y, view.m, day);
    open = false;
  }

  $effect(() => {
    if (!open) return;
    const onPointerDown = (event) => {
      if (!root?.contains(event.target)) open = false;
    };
    const onKey = (event) => {
      if (event.key === 'Escape') open = false;
    };
    // capture phase: closes even if the click target stops propagation
    window.addEventListener('pointerdown', onPointerDown, true);
    window.addEventListener('keydown', onKey);
    return () => {
      window.removeEventListener('pointerdown', onPointerDown, true);
      window.removeEventListener('keydown', onKey);
    };
  });
</script>

<div class="date-field" bind:this={root}>
  <input
    class="mono"
    class:invalid={!valid}
    {placeholder}
    {value}
    oninput={(e) => (value = e.currentTarget.value.trim())}
  />
  <button
    type="button"
    class="cal"
    aria-label="Open calendar"
    aria-expanded={open}
    onclick={toggle}
  >
    🗓
  </button>

  {#if open}
    <div class="popover" class:up>
      <div class="nav">
        <button type="button" aria-label="Previous month" onclick={() => shiftMonth(-1)}>‹</button>
        <span>{monthLabel}</span>
        <button type="button" aria-label="Next month" onclick={() => shiftMonth(1)}>›</button>
      </div>
      <div class="days">
        {#each WEEKDAYS as day}<span class="wd">{day}</span>{/each}
        {#each grid as day}
          {#if day == null}
            <span></span>
          {:else}
            <button
              type="button"
              class:selected={value === iso(view.y, view.m, day)}
              class:today={todayIso() === iso(view.y, view.m, day)}
              onclick={() => pick(day)}
            >
              {day}
            </button>
          {/if}
        {/each}
      </div>
      <div class="foot">
        <button type="button" onclick={() => ((value = todayIso()), (open = false))}>Today</button>
        <button type="button" onclick={() => ((value = ''), (open = false))}>Clear</button>
      </div>
    </div>
  {/if}
</div>

<style>
  .date-field { position: relative; display: flex; gap: 0.25rem; }
  .date-field input { flex: 1; min-width: 0; }
  .date-field input.invalid { border-color: var(--err); color: var(--err); }
  .cal { padding: 0 0.4rem; line-height: 1; }
  .popover {
    position: absolute;
    z-index: 20;
    top: calc(100% + 0.25rem);
    left: 0;
    padding: 0.5rem;
    background: var(--panel);
    border: 1px solid var(--border);
    border-radius: 8px;
    box-shadow: 0 8px 24px rgb(0 0 0 / 0.18);
    width: 15rem;
  }
  .popover.up { top: auto; bottom: calc(100% + 0.25rem); }
  .nav { display: flex; align-items: center; justify-content: space-between; gap: 0.3rem; }
  .nav span { font-size: 0.85rem; color: var(--text); }
  .days { display: grid; grid-template-columns: repeat(7, 1fr); gap: 2px; margin-top: 0.4rem; }
  .days .wd { text-align: center; font-size: 0.7rem; color: var(--muted); padding: 0.15rem 0; }
  .days button {
    padding: 0.2rem 0;
    font-size: 0.8rem;
    border-color: transparent;
    background: none;
  }
  .days button:hover { background: var(--accent-soft); }
  .days button.today { border-color: var(--border); }
  .days button.selected { background: var(--accent); color: #fff; }
  .foot { display: flex; gap: 0.3rem; margin-top: 0.4rem; }
  .foot button { flex: 1; font-size: 0.8rem; }
</style>
