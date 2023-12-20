<script lang="ts">
	import { CA_LEGISLATURE_URL } from "$lib/constants";
	import { Link, TextInput } from "$lib/components";
</script>

<p>
	The data used in this app is downloaded from <Link url={CA_LEGISLATURE_URL} new_page />.
</p>

<form action="search">
	<div class="fields">
		<TextInput label="Bill Number" name="bill-number" />
		<TextInput label="Legislator" name="legislator" />
	</div>
	<input type="submit" value="Search" />
</form>

<style>
	.fields {
		display: flex;
		flex-direction: column;
		row-gap: 1rem;
		margin-bottom: 1rem;
		max-width: 20rem;
	}
</style>
