<script setup lang="ts">
import { ref, computed, onMounted, onUnmounted } from "vue";
import Recipes from "@/components/dashboard/Recipes.vue";
import NavBar from "@/components/dashboard/Navbar.vue";
import SkapaRecept, { type RecipePayload } from "@/components/dashboard/SkapaRecept.vue";
import VisaRecept from "@/components/dashboard/VisaRecept.vue";
import type { Recipe } from "../types/recipe.ts";

type ComplexityFilter = "Alla" | "1 - Lätt" | "2 - Medel" | "3 - Komplex";

const search = ref("");
const activePage = ref("Hitta recept");
const previousPage = ref("Hitta recept");
const selectedRecipe = ref<Recipe | null>(null);
const selectedComplexity = ref<ComplexityFilter>("Alla");
const isFilterOpen = ref(false);
const filterRef = ref<HTMLElement | null>(null);
const defaultImg = "https://images.unsplash.com/photo-1498837167922-ddd27525d352?w=600&auto=format&fit=crop";

const recipes = ref<Recipe[]>([
  {
    id: "default-1",
    title: "Krämig Kräftpasta",
    description: "En lyxig och snabbkrämig pasta med kräftstjärtar, vitlök och chili.",
    image: "https://images.unsplash.com/photo-1563379091339-03b21ab4a4f8?w=600&auto=format&fit=crop",
    imagePosition: "center center",
    difficulty: "Lätt",
    time: "20 min",
    servings: "4 portioner",
    ingredients: ["400g Pasta", "300g Kräftstjärtar", "2.5dl Vispgrädde"],
    instructions: "1. Koka pastan...\n2. Fräs vitlök...",
    isUserCreated: false,
    isFavorite: false
  },
  {
    id: "default-2",
    title: "Klassisk Köttfärssås",
    description: "En välkryddad italiensk klassiker som passar hela familjen.",
    image: "https://images.unsplash.com/photo-1551183053-bf91a1d81141?w=600&auto=format&fit=crop",
    imagePosition: "center center",
    difficulty: "Medel",
    time: "45 min",
    servings: "4 portioner",
    ingredients: ["500g Nötfärs", "1 st Gul lök", "2 msk Tomatpuré"],
    instructions: "1. Hacka löken...",
    isUserCreated: false,
    isFavorite: false
  }
]);

const mapDiff = (d: number) => {
  if (d === 1) return "Lätt";
  if (d === 2) return "Medel";
  if (d === 3) return "Komplex";
  return "Lätt";
};

const filteredRecipes = computed(() => recipes.value.filter((r) => {
  const q = search.value.toLowerCase().trim();
  const matchSearch = !q || r.title?.toLowerCase().includes(q) || r.description?.toLowerCase().includes(q);

  if (selectedComplexity.value === "Alla") return matchSearch;

  // Jämför ren text ("lätt", "medel", "komplex") oavsett om filtret har "1 - " framför
  const selectedClean = selectedComplexity.value.toLowerCase().replace(/^[0-9]\s*-\s*/, "");
  const diffClean = String(r.difficulty).toLowerCase().replace(/^[0-9]\s*-\s*/, "");

  return matchSearch && (diffClean === selectedClean);
}));

const formatTime = (h: number, m: number) => [h > 0 && `${h} tim`, (m > 0 || !h) && `${m} min`].filter(Boolean).join(" ");

const toggleFav = (id: string) => {
  const r = recipes.value.find(x => x.id === id);
  if (r) r.isFavorite = !r.isFavorite;
};

function handleRecipeSaved(p: RecipePayload) {
  const newR: Recipe = {
    id: crypto.randomUUID(),
    title: p.title,
    description: p.description,
    image: p.image || defaultImg,
    imagePosition: p.imagePosition || "center center",
    difficulty: mapDiff(p.difficulty),
    time: formatTime(p.cookingtime[0], p.cookingtime[1]),
    servings: `${p.portions} portioner`,
    ingredients: p.ingredients.split("\n").map(i => i.replace(/^[•*-]\s*/, "").trim()).filter(Boolean),
    instructions: p.instructions,
    isUserCreated: true,
    isFavorite: false
  };
  recipes.value.push(newR);
  selectedRecipe.value = newR;
  previousPage.value = "Mina recept";
  activePage.value = "Visa recept";
}

function selectRecipe(r: Recipe) {
  if (activePage.value !== "Visa recept") previousPage.value = activePage.value;
  selectedRecipe.value = r;
  activePage.value = "Visa recept";
}

function deleteRecipe(id: string) {
  recipes.value = recipes.value.filter(r => r.id !== id);
  if (selectedRecipe.value?.id === id) {
    selectedRecipe.value = null;
    activePage.value = previousPage.value !== "Visa recept" ? previousPage.value : "Mina recept";
  }
}

const onOutsideClick = (e: MouseEvent) => {
  if (filterRef.value && !filterRef.value.contains(e.target as Node)) isFilterOpen.value = false;
};

onMounted(() => document.addEventListener("click", onOutsideClick));
onUnmounted(() => document.removeEventListener("click", onOutsideClick));
</script>

<template>
  <div class="min-h-[calc(100vh-74px)] font-['Roboto'] text-[#1a1a1a]"
    :class="['Skapa Recept', 'Visa recept'].includes(activePage) ? 'bg-[#f1f1f0]' : 'bg-[#dfa06094]'">
    <div class="grid min-h-[calc(100vh-74px)] grid-cols-1 lg:grid-cols-[218px_1fr]">
      <NavBar v-model:active-page="activePage" />

      <main class="min-w-0 p-4 sm:p-5 lg:p-[34px_30px_48px]">
        <!-- Sök & Filter -->
        <section v-if="!['Skapa Recept', 'Visa recept'].includes(activePage)"
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

        <!-- Views -->
        <SkapaRecept v-if="activePage === 'Skapa Recept'" @cancel="activePage = previousPage"
          @saved="handleRecipeSaved" />

        <div v-else-if="activePage === 'Visa recept'">
          <VisaRecept v-if="selectedRecipe" :recipe="selectedRecipe" @back="activePage = previousPage"
            @delete="deleteRecipe" @toggle-favorite="toggleFav" />
          <div v-else
            class="mx-auto max-w-[600px] rounded-xl border border-dashed border-[#deddd9] bg-white p-12 text-center text-gray-500">
            <h2 class="text-lg font-bold text-[#1a1a1a]">Inget recept valt</h2>
            <p class="mt-2 text-sm">Välj ett recept från listan för att visa detaljerna här.</p>
            <button type="button" @click="activePage = previousPage"
              class="mt-4 rounded-[9px] bg-[#b89a72] px-4 py-2 text-xs font-semibold text-white hover:bg-[#a7875f]">Tillbaka</button>
          </div>
        </div>

        <Recipes v-else :search="search" :active-page="activePage" :recipes="filteredRecipes"
          @select-recipe="selectRecipe" @delete-recipe="deleteRecipe" @toggle-favorite="toggleFav" />
      </main>
    </div>
  </div>
</template>