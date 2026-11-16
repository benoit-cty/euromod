<script>
  // EUROMOD's own layout, shared by the review UI and the RAG chat: a tab
  // strip under the logo, a ribbon of grouped commands, the brand star behind
  // the pages, a status bar at the foot. The app supplies its tabs, its own
  // ribbon groups and its pages; the shell adds the Display group (theme, plus
  // whatever `display` renders) and the Connection group (worker, login).
  import '../shell.css';
  import Icon from './Icon.svelte';
  import brandBackground from '../assets/brand_background_EUROMOD.jpg';

  let {
    logoTitle = 'Nómos',
    // localStorage key of the theme, one per app
    themeKey = 'theme',
    // null = unknown yet
    workerAlive = null,
    workerHint = {
      online: 'The worker is online.',
      offline: 'No worker is running: submitted work waits in the queue until one starts.',
    },
    user = null,
    userHint = 'Your database login: everything you do is recorded under it.',
    // the page-wide error banner; dismissing it clears it
    error = $bindable(''),
    // the status bar's left-hand text
    status = 'Ready',
    tabs,
    ribbon,
    display = null,
    children,
  } = $props();

  function readTheme() {
    try {
      return localStorage.getItem(themeKey) === 'dark';
    } catch {
      return false; // private window: the theme just isn't remembered
    }
  }

  let dark = $state(readTheme());

  $effect(() => {
    document.body.classList.toggle('dark', dark);
    try {
      localStorage.setItem(themeKey, dark ? 'dark' : 'light');
    } catch {
      /* preferences are a convenience */
    }
  });
</script>

<div class="app">
  <header class="tabstrip">
    <div class="logo" title={logoTitle}>N</div>
    <div class="tabs" role="tablist">{@render tabs()}</div>
  </header>

  <div class="ribbon">
    {@render ribbon?.()}
    <div class="group">
      <div class="cmds col">
        <label class="inline">
          Theme:
          <select value={dark ? 'dark' : 'light'} onchange={(e) => (dark = e.currentTarget.value === 'dark')}>
            <option value="light">Light</option>
            <option value="dark">Dark</option>
          </select>
        </label>
        {@render display?.()}
      </div>
      <div class="group-label">Display</div>
    </div>
    <div class="group">
      <div class="cmds col">
        <div
          class="inline"
          title={workerAlive ? workerHint.online : workerAlive === false ? workerHint.offline : 'Worker status unknown'}
        >
          <span class="dot" class:on={workerAlive} class:off={workerAlive === false}></span>
          {workerAlive ? 'Worker online' : workerAlive === false ? 'Worker offline' : 'Worker …'}
        </div>
        <div class="inline" title={userHint}>
          Signed in as <strong>{user ?? '—'}</strong>
        </div>
      </div>
      <div class="group-label">Connection</div>
    </div>
  </div>

  <div class="content" style:--brand-bg={`url(${brandBackground})`}>
    {#if error}
      <div class="callout err banner">
        <span>{error}</span>
        <button class="ghost" onclick={() => (error = '')} title="Dismiss"><Icon name="x" size={14} /></button>
      </div>
    {/if}
    {@render children()}
  </div>

  <footer class="statusbar">
    <span>{status}</span>
    <span class="muted">{user ? `Signed in as ${user}` : 'Not connected'}</span>
  </footer>
</div>
