<script lang="ts">
	import { page } from "$app/stores";
	import { SITE_NAME } from "$lib/constants";

	// Remove slash before search parameters
	const { href, searchParams } = $page.url;
	const urlWithoutSearchParams = href.split("?")[0];
	if (urlWithoutSearchParams.slice(-1) === "/") {
		history.replaceState(
			history.state,
			"",
			`${urlWithoutSearchParams.slice(0, -1)}?${searchParams}`,
		);
	}
</script>

<svelte:head>
	<title>{$page.url.searchParams.get("bill-number")} - {SITE_NAME}</title>
</svelte:head>

{#each $page.url.searchParams as [key, value]}
	<p>{key} is "{value}"</p>
{/each}
