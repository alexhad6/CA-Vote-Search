<script lang="ts">
	export let url: string;
	export let new_page: boolean = false;
</script>

<a href={url} target={new_page ? "_blank" : undefined}>
	<slot>
		{url}
	</slot>
</a>
