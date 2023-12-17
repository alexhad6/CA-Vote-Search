<script lang="ts">
	import "@fontsource-variable/roboto-slab";
	import { SITE_NAME } from "$lib/constants";
	import { Link } from "$lib/components";
</script>

<svelte:head>
	<title>{SITE_NAME}</title>
</svelte:head>

<Link url="/">
	<h1>{SITE_NAME}</h1>
</Link>

<slot />

<style>
	:global(body) {
		font-family: "Roboto Slab Variable", sans-serif;
	}
</style>
