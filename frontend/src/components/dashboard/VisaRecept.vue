<script setup lang="ts">
import { computed } from "vue";
import { useAuth0 } from "@auth0/auth0-vue";
import { hasAdminRole } from "../../auth/roles";
import type { Recipe } from "../../types/recipe.ts";

const props = defineProps<{
    recipe: Recipe;
    isPublic: boolean;
}>();

const { user, isAuthenticated } = useAuth0();

// Kontrollerar om den inloggade användaren är skaparen av receptet
const isRecipeAuthor = computed(
    () => isAuthenticated.value && user.value?.sub === props.recipe.author
);
const canManageRecipe = computed(
    () => isRecipeAuthor.value || (props.isPublic && hasAdminRole(user.value))
);

const emit = defineEmits<{
    back: [];
    edit: [];
    delete: [id: string];
    "toggle-favorite": [id: string];
}>();

const fallbackImage = "https://images.unsplash.com/photo-1498837167922-ddd27525d352?w=800&auto=format&fit=crop";

const difficultyLabel = computed(() => {
    if (typeof props.recipe.difficulty === "number") {
        if (props.recipe.difficulty === 1) return "Lätt";
        if (props.recipe.difficulty === 2) return "Medel";
        if (props.recipe.difficulty === 3) return "Komplex";
    }
    return String(props.recipe.difficulty || "").replace(/^[0-9]\s*-\s*/, "");
});

function handleImageError(event: Event) {
    const target = event.target as HTMLImageElement;
    target.src = fallbackImage;
}

function handleDelete() {
    if (confirm("Är du säker på att du vill ta bort detta recept?")) {
        emit("delete", props.recipe.id);
    }
}
</script>

<template>
    <div class="mx-auto max-w-[1000px] rounded-xl bg-white p-5 shadow-sm sm:p-8 font-['Roboto'] text-[#1a1a1a]">
        <!-- Header / Navigationsfält -->
        <div class="mb-6 flex items-center justify-between border-b border-[#deddd9] pb-4">
            <button type="button" @click="emit('back')"
                class="flex items-center gap-2 rounded-[9px] border border-[#d0cfcc] px-4 py-2 text-xs font-semibold text-[#6b6b6b] transition hover:bg-black/5 sm:text-sm">
                ← Tillbaka
            </button>

            <div class="flex items-center gap-3">
                <!-- FAVORIT-KNAPP -->
                <button type="button" @click="emit('toggle-favorite', recipe.id)"
                    class="flex h-9 w-9 items-center justify-center rounded-full bg-[#f1f1f0] text-lg transition hover:scale-110"
                    :title="recipe.isFavorite ? 'Ta bort från favoriter' : 'Lägg till i favoriter'">
                    <span v-if="recipe.isFavorite">❤️</span>
                    <span v-else class="grayscale opacity-60 hover:opacity-100">🤍</span>
                </button>

                <!-- REDIGERA-KNAPP (Visas endast för författaren) -->
                <button v-if="canManageRecipe" type="button" @click="emit('edit')"
                    class="rounded-[9px] bg-[#b4895e] px-4 py-2 text-xs font-semibold text-white transition hover:bg-[#966f48] sm:text-sm">
                    Redigera recept
                </button>

                <!-- TA BORT-KNAPP (Visas endast för författaren) -->
                <button v-if="canManageRecipe" type="button" @click="handleDelete"
                    class="rounded-[9px] bg-[#b42318] px-4 py-2 text-xs font-semibold text-white transition hover:bg-[#911c13] sm:text-sm">
                    Ta bort recept
                </button>
            </div>
        </div>

        <!-- Huvudinnehåll (Bild & Detaljer) -->
        <div class="grid grid-cols-1 gap-6 md:grid-cols-2">
            <img :src="recipe.image || fallbackImage" :alt="recipe.title" @error="handleImageError"
                :style="{ objectPosition: recipe.imagePosition || 'center' }"
                class="h-64 w-full rounded-[9px] object-cover sm:h-80" />

            <div class="flex flex-col justify-between">
                <div>
                    <span
                        class="inline-block rounded-md bg-[#b4895e]/15 px-2.5 py-1 text-xs font-medium text-[#b4895e]">
                        {{ difficultyLabel }}
                    </span>
                    <h1 class="mt-2 text-2xl font-bold sm:text-3xl">{{ recipe.title }}</h1>
                    <p class="mt-3 text-sm text-gray-600 leading-relaxed">{{ recipe.description }}</p>
                </div>

                <div
                    class="mt-6 flex flex-wrap gap-4 rounded-[9px] bg-[#f1f1f0] p-4 text-xs font-medium text-gray-700 sm:text-sm">
                    <div><span class="font-bold">Tid:</span> {{ recipe.time }}</div>
                    <div><span class="font-bold">Portioner:</span> {{ recipe.servings }}</div>
                </div>
            </div>
        </div>

        <!-- Ingredienser & Instruktioner -->
        <div class="mt-8 grid grid-cols-1 gap-8 border-t border-[#deddd9] pt-8 md:grid-cols-2">
            <div>
                <h2 class="mb-4 text-lg font-bold">Ingredienser</h2>
                <p class="whitespace-pre-line text-sm leading-relaxed text-gray-700">{{ recipe.ingredients }}</p>
            </div>

            <div>
                <h2 class="mb-4 text-lg font-bold">Instruktioner</h2>
                <p v-if="recipe.instructions" class="whitespace-pre-line text-sm leading-relaxed text-gray-700">
                    {{ recipe.instructions }}
                </p>
                <p v-else class="text-sm italic text-gray-400">
                    Inga instruktioner angivna för detta recept.
                </p>
            </div>
        </div>
    </div>
</template>