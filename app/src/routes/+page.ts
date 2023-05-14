export const load = async ({ fetch }) => {
	// fetch available curriculum sheets from backend on page fetch
	return {
		curriculums: fetch('http://localhost:8080/curriculum').then((resp) => resp.json())
	};
};
