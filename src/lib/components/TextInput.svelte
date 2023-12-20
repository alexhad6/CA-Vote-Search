<script lang="ts">
	export let label: string;
	export let name: string;
</script>

<label>
	{label}
	<input {name} />
</label>

<style>
	label {
		display: flex;
		justify-content: space-between;
	}
</style>
