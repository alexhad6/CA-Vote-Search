<script lang="ts">
	import type { Option } from "$lib/types";
	import { Autocomplete } from "$lib/components";
	import legislators from "$lib/data/legislators.json";
	import bills from "$lib/data/bills.json";

	const assemblymembers: Option[] = Object.entries(legislators["A"]).map(
		([name, { district, displayName, party }]) => ({
			value: name,
			label: `${district}: ${displayName} (${party})`,
		}),
	);

	const senators: Option[] = Object.entries(legislators["S"]).map(
		([name, { district, displayName, party }]) => ({
			value: name,
			label: `${district}: ${displayName} (${party})`,
		}),
	);

	const billOptions: Option[] = Object.entries(bills).map(([billId, { measure }]) => ({
		value: billId,
		label: measure,
	}));
</script>

<p>
	You can find your representatives at
	<a href="https://findyourrep.legislature.ca.gov" target="_blank" class="anchor"
		>findyourrep.legislature.ca.gov</a
	>.
</p>

<form action="/search" class="card flex max-w-xl flex-col items-start gap-4 p-4">
	<Autocomplete
		id="assemblymember"
		name="assemblymember"
		label="Assemblymember"
		options={assemblymembers}
	/>
	<Autocomplete id="senator" name="senator" label="Senator" options={senators} />
	<Autocomplete id="bills" name="bills" label="Bills" options={billOptions} />
	<input type="submit" value="Search" class="variant-filled btn" />
</form>
