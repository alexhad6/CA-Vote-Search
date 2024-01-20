<script lang="ts">
	import type { AutocompleteOption } from "@skeletonlabs/skeleton";
	import { Autocomplete, InputChip } from "@skeletonlabs/skeleton";
	import legislators from "$lib/data/legislators.json";
	import bills from "$lib/data/bills.json";

	const billOptions: AutocompleteOption<string>[] = Object.entries(bills).map(
		([, { measure }]) => ({ label: measure, value: measure }),
	);
	const billSet = new Set(billOptions.map(({ label }) => label));

	let billInput = "";
	let selectedBills: string[] = [];

	function onInputChipSelect(event: CustomEvent<AutocompleteOption<string>>): void {
		selectedBills.push(event.detail.label);
		selectedBills = selectedBills;
	}

	function isValidBill(value: string) {
		const upperCaseValue = value.toUpperCase();
		return billSet.has(upperCaseValue) && !selectedBills.includes(upperCaseValue);
	}
</script>

<p>
	You can find your representatives at
	<a href="https://findyourrep.legislature.ca.gov" target="_blank" class="anchor"
		>findyourrep.legislature.ca.gov</a
	>.
</p>

<form action="/search" class="card flex max-w-xl flex-col items-start gap-4 p-4">
	<label class="label">
		Assemblymember
		<select name="assemblymember" class="select">
			{#each Object.entries(legislators["A"]) as [name, { district, displayName, party }] (name)}
				<option value={name}>{district}: {displayName} ({party})</option>
			{/each}
		</select>
	</label>
	<label class="label">
		Senator
		<select name="senator" class="select">
			{#each Object.entries(legislators["S"]) as [name, { district, displayName, party }] (name)}
				<option value={name}>{district}: {displayName} ({party})</option>
			{/each}
		</select>
	</label>
	<!-- <label>
		Bill
		<select name="bill" multiple class="select">
			{#each Object.entries(bills) as [bill_id, { measure }] (bill_id)}
				<option value={bill_id}>{measure}</option>
			{/each}
		</select>
	</label> -->

	<!-- svelte-ignore a11y-label-has-associated-control -->
	<label class="label">
		Bills
		<InputChip
			regionInput="outline-none"
			bind:input={billInput}
			bind:value={selectedBills}
			name="bills"
			placeholder="Add bills…"
			validation={isValidBill}
			on:add={({ detail: { chipIndex, chipValue } }) => {
				selectedBills[chipIndex] = chipValue.toUpperCase();
			}}
		/>
	</label>

	<div class="card max-h-48 w-full max-w-sm overflow-y-auto p-4" tabindex="-1">
		<Autocomplete
			limit={100}
			transitions={false}
			bind:input={billInput}
			options={billOptions}
			denylist={selectedBills}
			on:selection={onInputChipSelect}
		/>
	</div>

	<input type="submit" value="Search" class="variant-filled btn" />
</form>
