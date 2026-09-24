
<script setup lang="ts">
import { computed, ref } from "vue";

type Recipe = {
  title: string;
  description: string;
  image: string;
  difficulty: "Lätt" | "Medel" | "Komplex";
  time: string;
  servings: string;
  ingredients: string[];
};

const props = defineProps<{
  search: string;
}>();

const favorites = ref<string[]>([]);

const recipes: Recipe[] = [
  {
    title: "Beef Wellington",
    description: "Brittisk klassiker med oxfilé",
    image:
      "https://api.builder.io/api/v1/image/assets/TEMP/ea1b6f9eea4151bcc95173edd130a44c9bd3f1ef?width=550",
    difficulty: "Komplex",
    time: "2 tim 30 min",
    servings: "6 portioner",
    ingredients: ["🥩 Oxfilé", "🥐 Smördeg", "🍄 Svamp", "🧅 Schalottenlök", "🥬 Spenat", "🧈 Smör"],
  },
  {
    title: "Pasta Carbonara",
    description: "Klassisk italiensk pasta",
    image:
      "https://api.builder.io/api/v1/image/assets/TEMP/0324cc82370f04384f90ebb1784338b69ffb6de8?width=550",
    difficulty: "Medel",
    time: "25 min",
    servings: "4 portioner",
    ingredients: ["🍝 Spaghetti", "🥚 Ägg", "🧀 Pecorino", "🥓 Guanciale", "🧂 Svartpeppar"],
  },
  {
    title: "Spaghetti med lax och köttbullar",
    description: "Italiensk pasta med lax och köttbullar",
    image:
      "https://api.builder.io/api/v1/image/assets/TEMP/5ed7e4545f97a358a4966ccd80f56651d62652ba?width=550",
    difficulty: "Lätt",
    time: "30 min",
    servings: "4 portioner",
    ingredients: ["🍝 Spaghetti", "🐟 Lax", "🧀 Pecorino", "🥩 Köttbullar", "🧂 Svartpeppar"],
  },

  {
    title: "snopppasta",
    description: "pasta med snoppar",
    image:
      "https://api.builder.io/api/v1/image/assets/TEMP/ea1b6f9eea4151bcc95173edd130a44c9bd3f1ef?width=550",
    difficulty: "Lätt",
    time: "20 min",
    servings: "6 portioner",
    ingredients: ["Pasta", "Snoppar"],
  }
];

const filteredRecipes = computed(() => {
  const query = props.search.toLowerCase().trim();

  return recipes.filter((recipe) => {
    return (
      !query ||
      recipe.title.toLowerCase().includes(query) ||
      recipe.description.toLowerCase().includes(query) ||
      recipe.ingredients.some((item) => item.toLowerCase().includes(query))
    );
  });
});

function toggleFavorite(title: string) {
  favorites.value = favorites.value.includes(title)
    ? favorites.value.filter((item) => item !== title)
    : [...favorites.value, title];
}

function difficultyColor(difficulty: Recipe["difficulty"]) {
  return {
    Lätt: "bg-green-500",
    Medel: "bg-amber-400",
    Komplex: "bg-purple-600",
  }[difficulty];
}

function difficultyDots(difficulty: Recipe["difficulty"]) {
  return {
    Lätt: 1,
    Medel: 3,
    Komplex: 5,
  }[difficulty];
}
</script>

<template>
  <section class="grid grid-cols-1 gap-8 min-[700px]:grid-cols-2 min-[700px]:gap-10 min-[1100px]:grid-cols-3 min-[1100px]:gap-[78px]">
    <article
      v-for="recipe in filteredRecipes"
      :key="recipe.title"
      class="overflow-hidden rounded-[14px] bg-white shadow-[0_2px_12px_rgba(0,0,0,0.1)] transition duration-300 hover:-translate-y-1.5 hover:shadow-xl"
    >
      <div class="relative h-[150px] overflow-hidden">
        <img
          :src="recipe.image"
          :alt="recipe.title"
          class="h-full w-full object-cover transition duration-500 hover:scale-105"
        />

        <span
          class="absolute right-2.5 top-4 rounded-full px-2.5 py-1 text-[10px] font-semibold text-white"
          :class="difficultyColor(recipe.difficulty)"
        >
          {{ recipe.difficulty }}
        </span>

        <button
          type="button"
          class="absolute left-2.5 top-2.5 grid h-7 w-7 place-items-center rounded-full bg-white/90 text-xl transition hover:scale-110"
          :class="favorites.includes(recipe.title) ? 'text-red-500' : 'text-[#6b6b6b] hover:text-[#c08153]'"
          :aria-label="`Spara ${recipe.title} som favorit`"
          :aria-pressed="favorites.includes(recipe.title)"
          @click="toggleFavorite(recipe.title)"
        >
          {{ favorites.includes(recipe.title) ? "♥" : "♡" }}
        </button>
      </div>

      <div class="p-4 pb-[15px]">
        <h2 class="text-[15px] font-semibold leading-[19px]">
          {{ recipe.title }}
        </h2>

        <p class="mb-3.5 mt-0.5 min-h-[17px] truncate text-[11px] text-[#9a9a9a]">
          {{ recipe.description }}
        </p>

        <div class="flex items-center gap-2 text-xs text-[#6b6b6b]">
          <span>◷ {{ recipe.time }}</span>
          <i class="h-3.5 w-px bg-[#dedede]"></i>
          <span>⌁ {{ recipe.servings }}</span>
        </div>

        <div class="mt-3.5 min-h-20 border-t border-[#f0efe9] pt-2.5">
          <h3 class="mb-2 text-[10px] font-semibold uppercase tracking-[0.5px] text-[#5a5248]">
            Ingredienser
          </h3>

          <div class="flex flex-wrap gap-1">
            <span
              v-for="ingredient in recipe.ingredients"
              :key="ingredient"
              class="rounded-full bg-[#f7ecec] px-2 py-1 text-[10px] text-[#5a5248] transition hover:bg-[#f1dddd]"
            >
              {{ ingredient }}
            </span>
          </div>
        </div>

        <div class="mt-2 flex items-center gap-1">
          <div class="flex gap-1">
            <span
              v-for="index in 5"
              :key="index"
              class="h-1.5 w-1.5 rounded-full"
              :class="
                index <= difficultyDots(recipe.difficulty)
                  ? difficultyColor(recipe.difficulty)
                  : 'bg-[#ebebeb]'
              "
            ></span>
          </div>

          <small class="flex-1 text-[10px] text-[#9a9a9a]">
            Svårighetsgrad
          </small>

          <button
            type="button"
            class="h-[25px] min-w-[83px] rounded-lg bg-[#2d2d2d] text-[11px] font-semibold text-white transition hover:bg-black"
          >
            Visa recept
          </button>
        </div>
      </div>
    </article>

    <p
      v-if="filteredRecipes.length === 0"
      class="col-span-full text-sm text-[#6b6b6b]"
    >
      Inga recept matchar din sökning.
    </p>
  </section>
</template>