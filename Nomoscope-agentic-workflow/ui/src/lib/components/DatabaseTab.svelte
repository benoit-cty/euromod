<script>
  // Legislation: search the library (ArticleSearch), and its status per
  // country with the technical statistics folded below (LibraryStatus).
  import ArticleSearch from './ArticleSearch.svelte';
  import LibraryStatus from './LibraryStatus.svelte';

  // dbUrl: the app's database, password masked; onchangedb switches the whole app.
  let { dbUrl = '', onchangedb } = $props();

  let searchPart = $state(null);
  let statusPart = $state(null);

  // Target of the shell's Reload button while this tab is showing: stats plus
  // the current search, so results reflect a corpus that changed under us.
  export async function reload() {
    await statusPart?.loadStats();
    await searchPart?.rerun();
  }
</script>

<div class="db">
  <ArticleSearch bind:this={searchPart} />
  <LibraryStatus bind:this={statusPart} {dbUrl} {onchangedb} />
</div>

<style>
  .db { overflow: auto; display: flex; flex-direction: column; gap: 1rem; min-height: 0; }
</style>
