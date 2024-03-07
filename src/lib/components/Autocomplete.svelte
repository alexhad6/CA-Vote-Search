<script context="module" lang="ts">
	const ITEM_HEIGHT = 40;
	const ITEM_GAP = 4;
	const MAX_ITEMS_IN_VIEW = 5;
</script>

<script lang="ts">
	import type { PopupSettings } from "@skeletonlabs/skeleton";
	import { tick } from "svelte";
	import { popup } from "@skeletonlabs/skeleton";
	import VirtualList from "svelte-tiny-virtual-list";
	import type { Option } from "$lib/types";
	import { searchOptions } from "$lib/utils";

	export let id: string;
	export let name: string;
	export let label: string;
	export let options: Option[];

	let popupExpanded = false;
	let filterOptions = false;
	let selectedIndex = 0;
	let focusedIndex = selectedIndex;
	let scrollToIndex: number | null = null;
	let input = options[selectedIndex].label;
	let inputWidth: number;
	let inputElement: HTMLInputElement;
	let listboxElement: HTMLDivElement;

	$: listboxId = `${id}-listbox`;
	$: popupTarget = `${id}-popup`;
	$: popupSettings = {
		event: "focus-blur",
		target: popupTarget,
		placement: "bottom",
		state: ({ state }) => (popupExpanded = state),
	} satisfies PopupSettings;

	$: optionsWithIndices = options.map((option, index) => ({ index, ...option }));
	$: filteredOptions =
		filterOptions && input.length > 0
			? searchOptions(input, optionsWithIndices)
			: optionsWithIndices;
	$: listHeight =
		(ITEM_HEIGHT + ITEM_GAP) * Math.min(MAX_ITEMS_IN_VIEW, filteredOptions.length) -
		ITEM_GAP;
	$: itemHeights = Array.apply(null, new Array(options.length * 2 - 1)).map((_, index) =>
		index % 2 === 0 ? ITEM_HEIGHT : ITEM_GAP,
	);

	$: optionId = (index: number) => `${id}-${index}`;

	$: optionClasses = (index: number, filteredIndex: number) => {
		if (index === selectedIndex) return "bg-primary-active-token";
		if (filteredIndex === focusedIndex) return "bg-primary-500/20";
		return "";
	};

	$: resetInput = (index: number) => {
		input = options[index].label;
	};
</script>

<div class="w-full" bind:clientWidth={inputWidth}>
	<label class="label" for={id}>{label}</label>
	<input
		{id}
		type="text"
		class="input form-select"
		role="combobox"
		aria-autocomplete="list"
		aria-controls={listboxId}
		aria-expanded={popupExpanded ? "true" : "false"}
		aria-activedescendant={focusedIndex < filteredOptions.length
			? optionId(filteredOptions[focusedIndex].index)
			: ""}
		use:popup={popupSettings}
		bind:this={inputElement}
		bind:value={input}
		on:focus={async ({ currentTarget }) => {
			filterOptions = false;
			await tick();
			focusedIndex = selectedIndex;
			currentTarget.select();
			scrollToIndex = selectedIndex;
			await tick();
			scrollToIndex = null;
		}}
		on:blur={({ relatedTarget }) => {
			if (
				!(
					relatedTarget instanceof Element &&
					relatedTarget.role === "option" &&
					listboxElement.contains(relatedTarget)
				)
			) {
				resetInput(selectedIndex);
			}
		}}
		on:input={async () => {
			filterOptions = true;
			focusedIndex = 0;
			scrollToIndex = focusedIndex;
			await tick();
			scrollToIndex = null;
		}}
		on:keydown={async (event) => {
			const { key } = event;
			if (focusedIndex !== null) {
				if (key === "ArrowUp") {
					focusedIndex = Math.max(0, focusedIndex - 1);
					scrollToIndex = focusedIndex;
					await tick();
					scrollToIndex = null;
				} else if (key === "ArrowDown") {
					focusedIndex = Math.min(filteredOptions.length - 1, focusedIndex + 1);
					scrollToIndex = focusedIndex;
					await tick();
					scrollToIndex = null;
				} else if (key === "Enter") {
					selectedIndex = filteredOptions[focusedIndex].index;
					filterOptions = false;
					resetInput(selectedIndex);
					focusedIndex = selectedIndex;
					await tick();
					inputElement.select();
					scrollToIndex = selectedIndex;
					await tick();
					scrollToIndex = null;
				} else {
					return;
				}
				event.preventDefault();
			}
		}}
	/>
</div>

<div
	id={listboxId}
	class="card z-10 duration-0 [&>div]:my-4 [&>div]:px-4"
	style:width="{inputWidth}px"
	role="listbox"
	aria-label="{label} Options"
	data-popup={popupTarget}
	bind:this={listboxElement}
>
	{#if filteredOptions.length > 0}
		<VirtualList
			width="100%"
			height={listHeight}
			itemCount={filteredOptions.length * 2 - 1}
			itemSize={itemHeights}
			scrollToIndex={scrollToIndex === null ? undefined : scrollToIndex * 2}
			scrollToAlignment="auto"
		>
			<svelte:fragment slot="item" let:index={filteredIndex} let:style>
				{#if filteredIndex % 2 == 0}
					<!-- svelte-ignore a11y-click-events-have-key-events -->
					<div
						id={optionId(filteredOptions[filteredIndex / 2].index)}
						role="option"
						aria-selected={selectedIndex === filteredOptions[filteredIndex / 2].index}
						class={"cursor-pointer truncate px-4 py-2 rounded-token " +
							optionClasses(filteredOptions[filteredIndex / 2].index, filteredIndex / 2)}
						title={filteredOptions[filteredIndex / 2].label}
						tabindex="-1"
						{style}
						on:mousemove={() => (focusedIndex = filteredIndex / 2)}
						on:click={async () => {
							selectedIndex = filteredOptions[filteredIndex / 2].index;
							resetInput(selectedIndex);
							filterOptions = false;
							await tick();
							inputElement.focus();
						}}
					>
						{filteredOptions[filteredIndex / 2].label}
					</div>
				{/if}
			</svelte:fragment>
		</VirtualList>
	{:else}
		<div style="height:{listHeight}px;">
			<div class="px-4 py-2">No results found</div>
		</div>
	{/if}
</div>

<input hidden {name} value={options[selectedIndex].value} />
