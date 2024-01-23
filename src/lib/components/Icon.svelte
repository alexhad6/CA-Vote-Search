<script lang="ts">
	import { svgStrings } from "$lib/icons";

	export let icon: keyof typeof svgStrings;
</script>

<div class="fill-token w-6">
	<!-- eslint-disable-next-line svelte/no-at-html-tags -->
	{@html svgStrings[icon]}
</div>
