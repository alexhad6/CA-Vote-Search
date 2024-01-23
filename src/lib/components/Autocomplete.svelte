<script lang="ts">
	import { tick } from "svelte";
	import type { Option } from "$lib/types";
	import { searchOptions } from "$lib/utils";

	export let id: string;
	export let name: string;
	export let label: string;
	export let options: Option[];

	let filterOptions = false;
	let focusedIndex = 0;
	let selectedIndex = 0;
	let input = options[selectedIndex].label;
	let inputElement: HTMLInputElement;
	let listElement: HTMLUListElement;

	$: listboxId = `${id}-listbox`;
	$: optionsWithIndices = options.map((option, index) => ({ index, ...option }));
	$: filteredOptions =
		filterOptions && input.length > 0
			? searchOptions(input, optionsWithIndices)
			: optionsWithIndices;

	$: optionId = (index: number) => `${id}-${index}`;

	$: optionClasses = (index: number, filteredIndex: number) => {
		if (index === selectedIndex) return "bg-primary-active-token";
		if (filteredIndex === focusedIndex) return "bg-primary-500/20";
		return "";
	};

	$: resetInput = (index: number) => {
		input = options[index].label;
	};

	$: scrollOptionIntoView = (filteredIndex: number) => {
		if (filteredIndex < filteredOptions.length) {
			const { index } = filteredOptions[filteredIndex];
			const optionElement = document.getElementById(optionId(index));
			if (optionElement !== null) {
				optionElement.scrollIntoView({ block: "nearest" });
			}
		}
	};
</script>

<label class="label" for={id}>{label}</label>
<input
	{id}
	type="text"
	class="input form-select"
	role="combobox"
	aria-autocomplete="list"
	aria-controls={listboxId}
	aria-expanded="true"
	aria-activedescendant={focusedIndex < filteredOptions.length
		? optionId(filteredOptions[focusedIndex].index)
		: ""}
	bind:this={inputElement}
	bind:value={input}
	on:focus={({ currentTarget }) => {
		filterOptions = false;
		focusedIndex = selectedIndex;
		currentTarget.select();
		scrollOptionIntoView(selectedIndex);
	}}
	on:blur={({ relatedTarget }) => {
		if (
			!(relatedTarget instanceof HTMLLIElement && listElement.contains(relatedTarget))
		) {
			resetInput(selectedIndex);
		}
	}}
	on:input={() => {
		filterOptions = true;
		focusedIndex = 0;
		scrollOptionIntoView(focusedIndex);
	}}
	on:keydown={async (event) => {
		const { key } = event;
		if (focusedIndex !== null) {
			if (key === "ArrowUp") {
				focusedIndex = Math.max(0, focusedIndex - 1);
				scrollOptionIntoView(focusedIndex);
			} else if (key === "ArrowDown") {
				focusedIndex = Math.min(filteredOptions.length - 1, focusedIndex + 1);
				scrollOptionIntoView(focusedIndex);
			} else if (key === "Enter") {
				selectedIndex = filteredOptions[focusedIndex].index;
				filterOptions = false;
				resetInput(selectedIndex);
				focusedIndex = selectedIndex;
				await tick();
				inputElement.select();
				scrollOptionIntoView(selectedIndex);
			} else {
				return;
			}
			event.preventDefault();
		}
	}}
/>

<ul
	id={listboxId}
	class="card list max-h-48 w-full overflow-y-auto p-4"
	role="listbox"
	aria-label="{label} Options"
	bind:this={listElement}
>
	{#each filteredOptions as { index, value, label }, filteredIndex (value)}
		<!-- svelte-ignore a11y-click-events-have-key-events -->
		<li
			id={optionId(index)}
			role="option"
			aria-selected={selectedIndex === index}
			class="cursor-pointer px-4 py-2 {optionClasses(index, filteredIndex)}"
			tabindex="-1"
			on:mousemove={() => (focusedIndex = filteredIndex)}
			on:click={async () => {
				selectedIndex = index;
				resetInput(selectedIndex);
				filterOptions = false;
				await tick();
				inputElement.focus();
			}}
		>
			{label}
		</li>
	{/each}
</ul>
<input hidden {name} value={options[selectedIndex].value} />
