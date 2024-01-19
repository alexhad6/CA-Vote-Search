<script lang="ts">
	import { Link } from "$lib/components";
	import legislators from "$lib/data/legislators.json";
	import bills from "$lib/data/bills.json";
</script>

<p>
	You can find your representatives at
	<Link url="https://findyourrep.legislature.ca.gov" new_page />.
</p>

<form action="search">
	<div class="fields">
		<label>
			Assemblymember
			<select name="assemblymember">
				{#each Object.entries(legislators["A"]) as [name, { district, displayName, party }] (name)}
					<option value={name}>{district}: {displayName} ({party})</option>
				{/each}
			</select>
		</label>
		<label>
			Senator
			<select name="senator">
				{#each Object.entries(legislators["S"]) as [name, { district, displayName, party }] (name)}
					<option value={name}>{district}: {displayName} ({party})</option>
				{/each}
			</select>
		</label>
		<label>
			Bill
			<select name="bill">
				{#each Object.entries(bills) as [bill_id, { measure }] (bill_id)}
					<option value={bill_id}>{measure}</option>
				{/each}
			</select>
		</label>
	</div>
	<input type="submit" value="Search" />
</form>

<style>
	.fields {
		display: flex;
		flex-direction: column;
		row-gap: 1rem;
		margin-bottom: 1rem;
		max-width: 40rem;
	}
</style>
