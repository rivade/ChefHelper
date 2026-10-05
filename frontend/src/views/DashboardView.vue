<script setup lang="ts">
import { ref, computed, onMounted, onUnmounted } from "vue";
import Recipes from "@/components/dashboard/Recipes.vue";
import NavBar from "@/components/dashboard/Navbar.vue";
import SkapaRecept, { type RecipePayload } from "@/components/dashboard/SkapaRecept.vue";
import VisaRecept from "@/components/dashboard/VisaRecept.vue";
import EditRecipe from "@/components/dashboard/EditRecepie.vue";
import type { Recipe } from "../types/recipe.ts";
import { useRecipeHandler, loadPublicRecipes, publicRecipes, userRecipes } from "@/RecipeHandler.ts";

type ComplexityFilter = "Alla" | "1 - Lätt" | "2 - Medel" | "3 - Komplex";

const search = ref("");
const activePage = ref("Hitta recept");
const previousPage = ref("Hitta recept");
const selectedRecipe = ref<Recipe | null>(null);
const selectedComplexity = ref<ComplexityFilter>("Alla");
const isFilterOpen = ref(false);
const filterRef = ref<HTMLElement | null>(null);
const defaultImg = "https://images.unsplash.com/photo-1498837167922-ddd27525d352?w=600&auto=format&fit=crop";

const {
  postRecipePublic,
  postRecipePrivate,
  updateRecipe,
  deleteRecipe: deleteRecipeFromApi,
  loadPrivateRecipes,
  loadFavorites,
  toggleFavorite,
} = useRecipeHandler();

const isDetailOrFormView = computed(() =>
  ["Skapa Recept", "Visa recept", "Redigera recept"].includes(activePage.value)
);

const mapDiff = (d: number) => {
  if (d === 1) return "Lätt";
  if (d === 2) return "Medel";
  if (d === 3) return "Komplex";
  return "Lätt";
};

const filteredRecipes = computed(() => {
  const recipes = ["Mina recept", "Favoriter"].includes(activePage.value)
    ? [...publicRecipes.value, ...userRecipes.value]
    : publicRecipes.value;

  return recipes.filter((r) => {
    const q = search.value.toLowerCase().trim();
    const matchSearch = !q || r.title?.toLowerCase().includes(q) || r.description?.toLowerCase().includes(q);

    if (selectedComplexity.value === "Alla") return matchSearch;

    const selectedClean = selectedComplexity.value.toLowerCase().replace(/^[0-9]\s*-\s*/, "");
    const diffClean = String(r.difficulty).toLowerCase().replace(/^[0-9]\s*-\s*/, "");

    return matchSearch && diffClean === selectedClean;
  });
});
const publicRecipeIds = computed(() => publicRecipes.value.map((recipe) => recipe.id));

const formatTime = (h: number, m: number) =>
  [h > 0 && `${h} tim`, (m > 0 || !h) && `${m} min`].filter(Boolean).join(" ");

async function handleRecipeSaved(p: RecipePayload, privateRecipe: boolean) {
  const recipe: Omit<Recipe, "id" | "author"> = {
    title: p.title,
    description: p.description,
    image: p.image || defaultImg,
    imagePosition: p.imagePosition || "center center",
    difficulty: mapDiff(p.difficulty),
    time: formatTime(p.cookingtime[0], p.cookingtime[1]),
    servings: `${p.portions} portioner`,
    ingredients: p.ingredients,
    instructions: p.instructions,
  };

  const savedRecipe: Recipe | null = privateRecipe
    ? await postRecipePrivate(recipe)
    : await postRecipePublic(recipe);
  if (!savedRecipe) return;

  selectedRecipe.value = savedRecipe;
  previousPage.value = "Mina recept";
  activePage.value = "Visa recept";
}

// Sparar i MongoDB via updateRecipe i RecipeHandler.ts
async function handleRecipeUpdated(updatedRecipe: Recipe) {
  const isPrivate = userRecipes.value.some((r) => r.id === updatedRecipe.id);

  // Tillfällig lösning för att RecipeHandler.ts ska hitta receptet i userRecipes
  const existsInUser = userRecipes.value.some((r) => r.id === updatedRecipe.id);
  if (!existsInUser) {
    userRecipes.value.push(updatedRecipe);
  }

  // Anropar backend via PATCH
  const success = await updateRecipe(updatedRecipe.id, updatedRecipe, isPrivate);

  // LÄGG TILL DETTA: Om sparandet misslyckades i backend, avbryt så att vi inte städar bort något i onödan
  if (success === false) return;

  // Städa och uppdatera publik lista
  if (!isPrivate) {
    userRecipes.value = userRecipes.value.filter((r) => r.id !== updatedRecipe.id);
    const pubIndex = publicRecipes.value.findIndex((r) => r.id === updatedRecipe.id);
    if (pubIndex !== -1) {
      publicRecipes.value[pubIndex] = updatedRecipe;
    }
  }

  selectedRecipe.value = updatedRecipe;
  activePage.value = "Visa recept";
}

function selectRecipe(r: Recipe) {
  if (activePage.value !== "Visa recept") previousPage.value = activePage.value;
  selectedRecipe.value = r;
  activePage.value = "Visa recept";
}

async function deleteRecipe(id: string) {
  const isPrivate = userRecipes.value.some((recipe) => recipe.id === id);
  const deleted = await deleteRecipeFromApi(id, isPrivate);
  if (!deleted) return;

  if (selectedRecipe.value?.id === id) {
    selectedRecipe.value = null;
    activePage.value = previousPage.value !== "Visa recept" ? previousPage.value : "Mina recept";
  }
}

const onOutsideClick = (e: MouseEvent) => {
  if (filterRef.value && !filterRef.value.contains(e.target as Node)) isFilterOpen.value = false;
};

onMounted(() => {
  void Promise.all([loadPublicRecipes(), loadPrivateRecipes()]).then(() => loadFavorites());
  document.addEventListener("click", onOutsideClick);
});

onUnmounted(() => document.removeEventListener("click", onOutsideClick));
</script>

<template>
  <div class="min-h-[calc(100vh-74px)] font-['Roboto'] text-[#1a1a1a] transition-colors duration-500 ease-in-out"
    :class="isDetailOrFormView ? 'bg-[#f1f1f0]' : activePage === 'Favoriter' ? 'bg-[#e9c4c5]' : activePage === 'Mina recept' ? 'bg-[#c5d8e8]' : 'bg-[#dfa06094]'">
    <div class="grid min-h-[calc(100vh-74px)] grid-cols-1 lg:grid-cols-[218px_1fr]">
      <NavBar v-model:active-page="activePage" />

      <main class="min-w-0 p-4 sm:p-5 lg:p-[34px_30px_48px]">
        <!-- Sök & Filter -->
        <section v-if="!isDetailOrFormView"
          class="relative z-10 mb-8 flex flex-col gap-3 sm:mb-10 sm:flex-row sm:items-center sm:justify-center">
          <div ref="filterRef" class="relative z-20 w-full sm:absolute sm:left-0 sm:w-auto">
            <button type="button" @click.stop="isFilterOpen = !isFilterOpen"
              class="flex h-[34px] w-full items-center justify-between gap-2 rounded-lg bg-black px-3.5 text-sm font-semibold text-white transition hover:bg-[#2d2d2d] sm:w-44">
              <span>{{ selectedComplexity === 'Alla' ? 'Filter' : selectedComplexity }}</span>
              <svg class="h-4 w-4 text-white/70 transition-transform" :class="{ 'rotate-180': isFilterOpen }"
                fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M19 9l-7 7-7-7" />
              </svg>
            </button>

            <div v-if="isFilterOpen"
              class="absolute left-0 top-full z-30 mt-1.5 w-48 rounded-lg border border-gray-200 bg-white p-1.5 shadow-xl">
              <button v-for="opt in ['Alla', '1 - Lätt', '2 - Medel', '3 - Komplex'] as const" :key="opt" type="button"
                @click.stop="selectedComplexity = opt; isFilterOpen = false"
                class="flex w-full items-center justify-between rounded-md px-3 py-2 text-left text-xs font-semibold transition hover:bg-gray-100"
                :class="selectedComplexity === opt ? 'bg-[#b89a72] text-white' : 'text-[#1a1a1a]'">
                <span>{{ opt === 'Alla' ? 'Alla svårighetsgrader' : opt }}</span>
                <span v-if="selectedComplexity === opt">✓</span>
              </button>
            </div>
          </div>

          <label
            class="flex h-[34px] w-full items-center gap-3 rounded-lg bg-[#ffffff] px-3 transition focus-within:ring-4 focus-within:ring-white/40 sm:max-w-[306px]">
            <span class="text-xl text-gray-500">⌕</span>
            <input v-model="search" type="search" placeholder="Sök recept"
              class="w-full min-w-0 bg-transparent text-sm outline-none" />
          </label>
        </section>

        <!-- Skapa Recept -->
        <SkapaRecept v-if="activePage === 'Skapa Recept'" @cancel="activePage = previousPage"
          @saved="handleRecipeSaved" />

        <!-- Visa recept -->
        <div v-else-if="activePage === 'Visa recept'">
          <VisaRecept v-if="selectedRecipe" :recipe="selectedRecipe"
            :is-public="publicRecipes.some((recipe) => recipe.id === selectedRecipe?.id)" @back="activePage = previousPage"
            @edit="activePage = 'Redigera recept'" @delete="deleteRecipe" @toggle-favorite="toggleFavorite" />
          <div v-else
            class="mx-auto max-w-[600px] rounded-xl border border-dashed border-[#deddd9] bg-white p-12 text-center text-gray-500">
            <h2 class="text-lg font-bold text-[#1a1a1a]">Inget recept valt</h2>
            <p class="mt-2 text-sm">Välj ett recept från listan för att visa detaljerna här.</p>
            <button type="button" @click="activePage = previousPage"
              class="mt-4 rounded-[9px] bg-[#b89a72] px-4 py-2 text-xs font-semibold text-white hover:bg-[#a7875f]">
              Tillbaka
            </button>
          </div>
        </div>

        <!-- Redigera recept -->
        <EditRecipe v-else-if="activePage === 'Redigera recept' && selectedRecipe" :recipe="selectedRecipe"
          @cancel="activePage = 'Visa recept'" @updated="handleRecipeUpdated" />

        <!-- Receptlista -->
        <Recipes v-else :search="search" :active-page="activePage" :recipes="filteredRecipes"
          :public-recipe-ids="publicRecipeIds"
          @select-recipe="selectRecipe" @delete-recipe="deleteRecipe" @toggle-favorite="toggleFavorite" />
      </main>
    </div>
  </div>
</template>