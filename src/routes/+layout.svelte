<script lang="ts">
	import type { LayoutData } from "./$types";
	import { SITE_NAME } from "$lib/constants";

	export let data: LayoutData;
</script>

<svelte:head>
	<title>{SITE_NAME}</title>
</svelte:head>

<h1>{SITE_NAME}</h1>

<slot />

<footer>Page generated at {data.currentTime}.</footer>
