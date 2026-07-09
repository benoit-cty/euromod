// Single seam between the Svelte frontend and the Rust commands.
import { invoke } from '@tauri-apps/api/core';
import { open } from '@tauri-apps/plugin-shell';

export const api = {
  getEnvConfig: () => invoke('get_env_config'),
  loadQueue: (dataDir) => invoke('load_queue', { payload: { data_dir: dataDir } }),
  saveDecision: (payload) => invoke('save_decision', { payload }),
  loadDecisions: (dataDir, limit = 200) =>
    invoke('load_decisions', { payload: { data_dir: dataDir, limit } }),
  exportAccepted: (dataDir) => invoke('export_accepted', { payload: { data_dir: dataDir } }),
  pickDataDir: () => invoke('pick_data_dir'),
  dbStats: (dbUrl) => invoke('db_stats', { payload: { db_url: dbUrl } }),
  searchArticles: (payload) => invoke('search_articles', { payload }),
  openExternal: (url) => open(url),
};
