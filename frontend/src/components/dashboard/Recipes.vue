<script setup lang="ts">
import { computed } from "vue";
import type { Recipe } from "../../types/recipe.ts";

const props = defineProps<{
    search: string;
    activePage: string;
    recipes: Recipe[];
}>();

const emit = defineEmits<{
    "select-recipe": [recipe: Recipe];
    "delete-recipe": [id: string];
    "toggle-favorite": [id: string];
}>();

const fallbackImage = "https://images.unsplash.com/photo-1498837167922-ddd27525d352?w=600&auto=format&fit=crop";

function handleImageError(event: Event) {
    const target = event.target as HTMLImageElement;
    target.src = fallbackImage;
}

const filteredRecipes = computed(() => {
    let list = props.recipes;

    if (props.activePage === "Favoriter") {
        list = list.filter((r) => r.isFavorite);
    } else if (props.activePage === "Mina recept") {
        list = list.filter((r) => r.isUserCreated);
    }

    if (props.search.trim()) {
        const q = props.search.toLowerCase();
        list = list.filter(
            (r) => r.title.toLowerCase().includes(q) || r.description.toLowerCase().includes(q)
        );
    }

    return list;
});
</script>

<template>
    <div>
        <div v-if="filteredRecipes.length === 0" class="py-12 text-center text-gray-500">
            <p v-if="activePage === 'Favoriter'" class="text-base">Inga favoriter ännu. Klicka på hjärtat på ett recept
                för att spara det här!</p>
            <p v-else class="text-base">Inga recept hittades.</p>
        </div>

        <div v-else class="grid grid-cols-1 gap-6 sm:grid-cols-2 lg:grid-cols-3">
            <div v-for="recipe in filteredRecipes" :key="recipe.id"
                class="flex flex-col justify-between overflow-hidden rounded-xl bg-white p-4 shadow-sm transition hover:shadow-md">
                <div>
                    <div class="relative">
                        <img :src="recipe.image || fallbackImage" :alt="recipe.title" @error="handleImageError"
                            :style="{ objectPosition: recipe.imagePosition || 'center center' }"
                            class="h-44 w-full rounded-lg object-cover" />

                        <!-- Interactive Heart Icon -->
                        <button type="button" @click.stop="emit('toggle-favorite', recipe.id)"
                            class="absolute top-2 right-2 flex h-8 w-8 items-center justify-center rounded-full bg-white/80 text-base backdrop-blur-xs transition hover:scale-110 shadow-sm"
                            :title="recipe.isFavorite ? 'Ta bort från favoriter' : 'Lägg till i favoriter'">
                            <span v-if="recipe.isFavorite">❤️</span>
                            <span v-else class="grayscale opacity-60 hover:opacity-100">🤍</span>
                        </button>
                    </div>

                    <div class="mt-3 flex items-center justify-between">
                        <span class="rounded bg-[#b4895e]/15 px-2 py-0.5 text-xs font-medium text-[#b4895e]">
                            {{ recipe.difficulty }}
                        </span>
                        <span class="text-xs text-gray-500">{{ recipe.time }}</span>
                    </div>

                    <h3 class="mt-2 text-lg font-bold text-[#1a1a1a]">{{ recipe.title }}</h3>
                    <p class="mt-1 line-clamp-2 text-xs text-gray-600">{{ recipe.description }}</p>
                </div>

                <div class="mt-4 flex items-center justify-between border-t border-[#deddd9] pt-3">
                    <button type="button" @click="emit('select-recipe', recipe)"
                        class="rounded-[9px] bg-[#b89a72] px-3 py-1.5 text-xs font-semibold text-white transition hover:bg-[#a7875f]">
                        Visa recept
                    </button>

                    <button v-if="recipe.isUserCreated" type="button" @click="emit('delete-recipe', recipe.id)"
                        class="text-xs text-red-600 transition hover:underline">
                        Ta bort
                    </button>
                </div>
            </div>
        </div>
    </div>
</template>