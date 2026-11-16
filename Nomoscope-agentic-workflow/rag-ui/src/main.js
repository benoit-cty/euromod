import { mount } from 'svelte';
import App from './App.svelte';
import '@shared/styles.css';
import './styles.css';

export default mount(App, { target: document.getElementById('app') });
