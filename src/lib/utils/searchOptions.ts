import fuzzysort from "fuzzysort";
import type { Option } from "$lib/types";

/**
 * Search the given list of options with indices for the given input, returning a ranked
 * list of results.
 */
export default function searchOptions<T extends Option>(input: string, options: T[]) {
	const results: { option: T; score: number }[] = [];

	options.forEach((option) => {
		const result = fuzzysort.single(input, option.label);
		if (result !== null) {
			results.push({ option, score: result.score });
		}
	});

	return results
		.sort(({ score: s1 }, { score: s2 }) => s2 - s1)
		.map(({ option }) => option);
}
