/** @type {import('@sveltejs/kit').Config} */
import node from '@sveltejs/adapter-node';
import {preprocess} from "svelte/compiler";

const config = {
	kit: {
		// hydrate the <div id="svelte"> element in src/app.html
		target: '#svelte',
		adapter: node(),
		prerender: {
			enabled: true
		}
	}
};

export default config;
