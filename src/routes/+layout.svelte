<script lang="ts">
	import { AppShell, AppBar, LightSwitch } from "@skeletonlabs/skeleton";
	import buildingColumns from "$lib/icons/building-columns.svg?raw";
	import "@fontsource-variable/inter";
	import "../app.postcss";
</script>

<svelte:head>
	<title>CA Vote Search</title>
</svelte:head>

<AppShell regionPage="space-y-4 p-4" slotPageContent="space-y-4">
	<svelte:fragment slot="header">
		<AppBar>
			<svelte:fragment slot="lead">
				<a href="/">
					<div class="flex items-center gap-x-2">
						<div class="w-6 fill-current">{@html buildingColumns}</div>
						<h1 class="h3">CA Vote Search</h1>
					</div>
				</a>
			</svelte:fragment>
			<svelte:fragment slot="trail">
				<LightSwitch rounded="rounded-full" />
			</svelte:fragment>
		</AppBar>
	</svelte:fragment>
	<slot />
	<svelte:fragment slot="pageFooter">
		<p>
			The data used in this app was downloaded from
			<a href="https://leginfo.legislature.ca.gov" target="_blank" class="anchor"
				>leginfo.legislature.ca.gov</a
			>.
		</p>
	</svelte:fragment>
</AppShell>
