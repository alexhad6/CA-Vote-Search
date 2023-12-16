import type { LayoutServerLoad } from "./$types";

export const prerender = true;

export const load: LayoutServerLoad = () => {
	return {
		currentTime: new Date().toString(),
	};
};
