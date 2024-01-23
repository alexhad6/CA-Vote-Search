<script lang="ts">
	import { AppShell, AppBar, LightSwitch } from "@skeletonlabs/skeleton";
	import { Icon } from "$lib/components";
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
						<Icon icon="buildingColumns" />
						<h1 class="h3 font-bold">CA Vote Search</h1>
					</div>
				</a>
			</svelte:fragment>
			<svelte:fragment slot="trail">
				<a
					class="btn-icon hover:bg-primary-500/20"
					href="https://github.com/alexhad6/CAVoteSearch"
					target="_blank"
				>
					<Icon icon="githubMark" />
				</a>
				<LightSwitch rounded="rounded-full" />
			</svelte:fragment>
		</AppBar>
	</svelte:fragment>
	<slot />
	<svelte:fragment slot="pageFooter">
		<p>
			The data used in this app was downloaded from
			<a class="anchor" href="https://leginfo.legislature.ca.gov" target="_blank">
				leginfo.legislature.ca.gov
			</a>.
		</p>
	</svelte:fragment>
</AppShell>
