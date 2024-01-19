<script lang="ts">
	import "@fontsource-variable/roboto-slab";
	import { SITE_NAME, CA_LEGISLATURE_URL } from "$lib/constants";
	import { Link } from "$lib/components";
</script>

<svelte:head>
	<title>{SITE_NAME}</title>
</svelte:head>

<Link url="/">
	<h1>{SITE_NAME}</h1>
</Link>

<slot />

<footer>
	<p>
		The data used in this app is downloaded from
		<Link url={CA_LEGISLATURE_URL} new_page />.
	</p>
	<p></p>
</footer>

<style>
	:global(body) {
		font-family: "Roboto Slab Variable", sans-serif;
	}
</style>
