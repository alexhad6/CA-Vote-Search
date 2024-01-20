<script lang="ts">
	import { page } from "$app/stores";

	const { searchParams } = $page.url;
</script>

<div class="table-container max-w-3xl">
	<table class="table table-hover">
		<thead>
			<tr>
				<th>Key</th>
				<th>Value</th>
			</tr>
		</thead>
		<tbody>
			<tr>
				<td>Assemblymember</td>
				<td>
					<code class="code">{JSON.stringify(searchParams.get("assemblymember"))}</code>
				</td>
			</tr>
			<tr>
				<td>Senator</td>
				<td>
					<code class="code">{JSON.stringify(searchParams.get("senator"))}</code>
				</td>
			</tr>
			<tr>
				<td>Bills</td>
				<td>
					<code class="code">{JSON.stringify(searchParams.getAll("bills"))}</code>
				</td>
			</tr>
		</tbody>
	</table>
</div>
