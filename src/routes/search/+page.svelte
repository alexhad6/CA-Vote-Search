<script lang="ts">
	import { page } from "$app/stores";
</script>

{#each $page.url.searchParams as [key, value]}
	<p>{key} is "{value}"</p>
{/each}
