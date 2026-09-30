<script setup lang="ts">
import { computed, onMounted, onUnmounted, ref } from "vue";
import AnonRecipeCard from "../components/anonrecipebrowsing/AnonRecipeCard.vue";
import AnonRecipeDetails from "../components/anonrecipebrowsing/AnonRecipeDetails.vue";
import AnonAccessPrompt from "../components/anonrecipebrowsing/AnonAccessPrompt.vue";
import { loadPublicRecipes, publicRecipes } from "../RecipeHandler.ts";
import type { Recipe } from "../types/recipe.ts";

const search = ref("");
type ComplexityFilter = "Alla" | "1 - Lätt" | "2 - Medel" | "3 - Komplex";

const selectedDifficulty = ref<ComplexityFilter>("Alla");
const selectedRecipe = ref<Recipe | null>(null);
const isLoading = ref(true);
const hasLoadError = ref(false);
const isFilterOpen = ref(false);
const filterRef = ref<HTMLElement | null>(null);

function getDifficultyLabel(difficulty: Recipe["difficulty"]): string {
	const value = String(difficulty).replace(/^\s*\d+\s*-\s*/, "").trim();
	if (value !== String(difficulty)) return value;

	if (value === "1") return "Lätt";
	if (value === "2") return "Medel";
	if (value === "3") return "Komplex";
	return value;
}

const filteredRecipes = computed(() => {
	const query = search.value.trim().toLocaleLowerCase("sv-SE");

	return publicRecipes.value.filter((recipe) => {
		const matchesSearch = !query || [recipe.title, recipe.description, recipe.ingredients]
			.some((value) => value.toLocaleLowerCase("sv-SE").includes(query));
		const matchesDifficulty = selectedDifficulty.value === "Alla"
			|| getDifficultyLabel(recipe.difficulty).toLocaleLowerCase("sv-SE")
				=== getDifficultyLabel(selectedDifficulty.value).toLocaleLowerCase("sv-SE");

		return matchesSearch && matchesDifficulty;
	});
});

async function fetchRecipes() {
	isLoading.value = true;
	hasLoadError.value = !(await loadPublicRecipes({ silent: true }));
	isLoading.value = false;
}

function handleOutsideClick(event: MouseEvent) {
	if (filterRef.value && !filterRef.value.contains(event.target as Node)) {
		isFilterOpen.value = false;
	}
}

onMounted(() => {
	void fetchRecipes();
	document.addEventListener("click", handleOutsideClick);
});

onUnmounted(() => document.removeEventListener("click", handleOutsideClick));
</script>

<template>
	<main class="min-h-[calc(100vh-72px)] bg-[#f1f1f0] font-['Roboto'] text-[#1a1a1a]">
		<div class="mx-auto max-w-[1272px] px-4 py-6 sm:px-6 sm:py-9">
			<AnonAccessPrompt />

			<header class="mb-7 mt-9 border-b border-[#deddd9] pb-5 sm:mb-9">
				<h1 class="text-3xl font-bold sm:text-4xl">Utforska recept</h1>
				<p class="mt-2 max-w-2xl text-sm leading-6 text-[#626262] sm:text-base">
					Hitta inspiration bland recept som alla kan laga och dela.
				</p>
			</header>

			<AnonRecipeDetails
				v-if="selectedRecipe"
				:recipe="selectedRecipe"
				@back="selectedRecipe = null"
			/>

			<section v-else aria-label="Recept" class="space-y-5">
				<div class="relative flex flex-col items-center gap-3 sm:min-h-[34px] sm:justify-center">
					<label class="flex h-[34px] w-full max-w-[306px] min-w-0 items-center gap-3 rounded-lg bg-white px-3">
						<span aria-hidden="true" class="text-lg text-[#777]">⌕</span>
						<span class="sr-only">Sök recept</span>
						<input
							v-model="search"
							type="search"
							placeholder="Sök recept"
							class="w-full min-w-0 bg-transparent text-sm outline-none placeholder:text-[#858585]"
						/>
					</label>

					<div ref="filterRef" class="relative z-20 flex w-full justify-start sm:absolute sm:right-0 sm:top-0 sm:w-44">
						<button
							type="button"
							class="flex h-[34px] w-44 items-center justify-between gap-2 rounded-lg bg-black px-3.5 text-sm font-semibold text-white transition hover:bg-[#2d2d2d] sm:w-full"
							:aria-expanded="isFilterOpen"
							aria-haspopup="listbox"
							@click.stop="isFilterOpen = !isFilterOpen"
						>
							<span>{{ selectedDifficulty === "Alla" ? "Filter" : selectedDifficulty }}</span>
							<svg
								class="h-4 w-4 text-white/70 transition-transform"
								:class="{ 'rotate-180': isFilterOpen }"
								fill="none"
								stroke="currentColor"
								viewBox="0 0 24 24"
							>
								<path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M19 9l-7 7-7-7" />
							</svg>
						</button>

						<div
							v-if="isFilterOpen"
							class="absolute left-0 top-full z-30 mt-1.5 w-48 rounded-lg border border-gray-200 bg-white p-1.5 shadow-xl"
							role="listbox"
							aria-label="Svårighetsgrad"
						>
							<button
								v-for="option in ['Alla', '1 - Lätt', '2 - Medel', '3 - Komplex'] as const"
								:key="option"
								type="button"
								class="flex w-full items-center justify-between rounded-md px-3 py-2 text-left text-xs font-semibold transition hover:bg-gray-100"
								:class="selectedDifficulty === option ? 'bg-[#b89a72] text-white' : 'text-[#1a1a1a]'"
								:aria-selected="selectedDifficulty === option"
								role="option"
								@click.stop="selectedDifficulty = option; isFilterOpen = false"
							>
								<span>{{ option === "Alla" ? "Alla svårighetsgrader" : option }}</span>
								<span v-if="selectedDifficulty === option">✓</span>
							</button>
						</div>
					</div>
				</div>

				<p v-if="isLoading" class="py-12 text-center text-sm text-[#626262]">Laddar recept...</p>
				<div v-else-if="hasLoadError" class="py-12 text-center">
					<p class="text-sm text-[#626262]">Recepten kunde inte laddas just nu.</p>
					<button
						type="button"
						class="mt-3 rounded-lg border border-[#b9aa98] bg-white px-4 py-2 text-sm font-semibold text-[#292622] transition hover:bg-[#f8f6f2] focus-visible:outline-2 focus-visible:outline-offset-2 focus-visible:outline-[#8c6847]"
						@click="fetchRecipes"
					>
						Försök igen
					</button>
				</div>
				<p v-else-if="filteredRecipes.length === 0" class="py-12 text-center text-sm text-[#626262]">
					{{ publicRecipes.length ? "Inga recept matchar din sökning." : "Det finns inga recept att visa ännu." }}
				</p>

				<div v-else class="grid grid-cols-1 gap-6 sm:grid-cols-2 lg:grid-cols-3">
					<AnonRecipeCard
						v-for="recipe in filteredRecipes"
						:key="recipe.id"
						:recipe="recipe"
						@select="selectedRecipe = $event"
					/>
				</div>
			</section>
		</div>
	</main>
</template>