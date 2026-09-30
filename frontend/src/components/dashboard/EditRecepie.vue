<script setup lang="ts">
import { ref, reactive, computed } from "vue";
import type { Recipe } from "../../types/recipe";


const props = defineProps<{
    recipe: Recipe;
}>();

const emit = defineEmits<{
    cancel: [];
    updated: [recipe: Recipe];
}>();

// Hjälpfunktioner för att läsa in befintlig data
function parseTime(timeStr: string) {
    const hoursMatch = timeStr.match(/(\d+)\s*tim/);
    const minMatch = timeStr.match(/(\d+)\s*min/);
    return {
        hours: hoursMatch ? hoursMatch[1] : "",
        minutes: minMatch ? minMatch[1] : !hoursMatch && !isNaN(Number(timeStr)) ? timeStr : "",
    };
}

function parseServings(servingsStr: string) {
    const match = servingsStr.match(/(\d+)/);
    return match ? match[1] : "";
}

function parseDifficulty(diff: string | number) {
    if (typeof diff === "number") return diff;
    const str = String(diff).toLowerCase();
    if (str.includes("lätt") || str.startsWith("1")) return 1;
    if (str.includes("medel") || str.startsWith("2")) return 2;
    if (str.includes("komplex") || str.startsWith("3")) return 3;
    return 1;
}

const initialTime = parseTime(props.recipe.time);

const form = reactive({
    title: props.recipe.title || "",
    description: props.recipe.description || "",
    cookingHours: initialTime.hours,
    cookingMinutes: initialTime.minutes,
    portions: parseServings(props.recipe.servings),
    difficulty: parseDifficulty(props.recipe.difficulty),
    ingredients: props.recipe.ingredients || "",
    instructions: props.recipe.instructions || "",
    image: props.recipe.image || "",
    imagePosition: props.recipe.imagePosition || "center center",
});

const isDifficultyOpen = ref(false);
const showImageModal = ref(false);

const inputStyle =
    "w-full rounded-[9px] border border-[#deddd9] bg-[#fdfdfd] px-3.5 py-2.5 text-sm text-[#1a1a1a] outline-none transition focus:border-[#b89a72] focus:bg-white focus:ring-2 focus:ring-[#b89a72]/20";
const areaStyle =
    "w-full rounded-[9px] border border-[#deddd9] bg-[#fdfdfd] p-3 text-sm text-[#1a1a1a] outline-none transition focus:border-[#b89a72] focus:bg-white focus:ring-2 focus:ring-[#b89a72]/20";

const difficultyOptions = [
    { value: 1, label: "Lätt" },
    { value: 2, label: "Medel" },
    { value: 3, label: "Komplex" },
];

const selectedDifficultyLabel = computed(
    () => difficultyOptions.find((o) => o.value === form.difficulty)?.label ?? "Lätt"
);

function mapDiffToLabel(level: number) {
    if (level === 1) return "Lätt";
    if (level === 2) return "Medel";
    if (level === 3) return "Komplex";
    return "Lätt";
}

function formatTimeString(h: number, m: number) {
    const hoursNum = Number(h) || 0;
    const minNum = Number(m) || 0;
    return [hoursNum > 0 && `${hoursNum} tim`, (minNum > 0 || !hoursNum) && `${minNum} min`]
        .filter(Boolean)
        .join(" ");
}

function handleImageConfirmed(payload: { image: string; imagePosition: string }) {
    form.image = payload.image;
    form.imagePosition = payload.imagePosition;
    showImageModal.value = false;
}

function handleSubmit() {
    const updatedRecipe: Recipe = {
        ...props.recipe,
        title: form.title.trim(),
        description: form.description.trim(),
        image: form.image,
        imagePosition: form.imagePosition,
        difficulty: mapDiffToLabel(form.difficulty),
        time: formatTimeString(Number(form.cookingHours), Number(form.cookingMinutes)),
        servings: `${form.portions || 1} portioner`,
        ingredients: form.ingredients
            .split("\n")
            .map((i) => i.replace(/^[•*]\s*/, "").trim())
            .filter(Boolean)
            .join("\n"),
        instructions: form.instructions.trim(),
    };

    emit("updated", updatedRecipe);
}
</script>

<template>
    <!-- Samma vita kort-wrapper som VisaRecept.vue -->
    <div class="mx-auto max-w-[1000px] rounded-xl bg-white p-5 shadow-sm sm:p-8 font-['Roboto'] text-[#1a1a1a]">

        <!-- Header -->
        <div class="mb-6 flex items-center justify-between border-b border-[#deddd9] pb-4">
            <h1 class="text-xl font-bold text-[#1a1a1a] sm:text-2xl">Redigera recept</h1>

            <button type="button" @click="showImageModal = true"
                class="flex items-center gap-2 rounded-[9px] border border-[#d0cfcc] px-4 py-2 text-xs font-semibold text-[#1a1a1a] transition hover:bg-black/5 sm:text-sm">
                📷 Byt bild
            </button>
        </div>

        <!-- Formulär -->
        <form @submit.prevent="handleSubmit" class="space-y-6">

            <!-- Rad 1: Titel & Svårighetsgrad -->
            <div class="grid grid-cols-1 gap-4 md:grid-cols-2">
                <div>
                    <label class="mb-1.5 block text-xs font-bold text-gray-700 sm:text-sm">Namn på recept</label>
                    <input v-model="form.title" :class="inputStyle" required />
                </div>

                <div>
                    <label class="mb-1.5 block text-xs font-bold text-gray-700 sm:text-sm">Svårighetsgrad</label>
                    <div class="relative">
                        <button type="button" @click="isDifficultyOpen = !isDifficultyOpen"
                            class="flex w-full items-center justify-between rounded-[9px] border border-[#deddd9] bg-[#fdfdfd] px-3.5 py-2.5 text-sm">
                            <span>{{ selectedDifficultyLabel }}</span>
                            <span class="text-xs text-gray-400">▼</span>
                        </button>
                        <div v-if="isDifficultyOpen"
                            class="absolute left-0 right-0 top-full z-20 mt-1 rounded-[9px] border border-[#deddd9] bg-white p-1 shadow-lg">
                            <button v-for="opt in difficultyOptions" :key="opt.value" type="button"
                                @click="form.difficulty = opt.value; isDifficultyOpen = false"
                                class="w-full rounded-md px-3 py-2 text-left text-sm hover:bg-[#f1f1f0]">
                                {{ opt.label }}
                            </button>
                        </div>
                    </div>
                </div>
            </div>

            <!-- Rad 2: Beskrivning -->
            <div>
                <label class="mb-1.5 block text-xs font-bold text-gray-700 sm:text-sm">Kort beskrivning</label>
                <textarea v-model="form.description" :class="areaStyle" rows="2" required></textarea>
            </div>

            <!-- Rad 3: Tid och portioner -->
            <div class="grid grid-cols-1 gap-4 sm:grid-cols-3">
                <div>
                    <label class="mb-1.5 block text-xs font-bold text-gray-700 sm:text-sm">Timmar</label>
                    <input v-model="form.cookingHours" type="number" min="0" placeholder="0" :class="inputStyle" />
                </div>
                <div>
                    <label class="mb-1.5 block text-xs font-bold text-gray-700 sm:text-sm">Minuter</label>
                    <input v-model="form.cookingMinutes" type="number" min="0" placeholder="30" :class="inputStyle" />
                </div>
                <div>
                    <label class="mb-1.5 block text-xs font-bold text-gray-700 sm:text-sm">Portioner</label>
                    <input v-model="form.portions" type="number" min="1" placeholder="4" :class="inputStyle" required />
                </div>
            </div>

            <!-- Rad 4: Ingredienser & Instruktioner -->
            <div class="grid grid-cols-1 gap-6 border-t border-[#deddd9] pt-6 md:grid-cols-2">
                <div>
                    <label class="mb-1.5 block text-xs font-bold text-gray-700 sm:text-sm">Ingredienser (en per
                        rad)</label>
                    <textarea v-model="form.ingredients" :class="areaStyle" rows="8" required></textarea>
                </div>

                <div>
                    <label class="mb-1.5 block text-xs font-bold text-gray-700 sm:text-sm">Instruktioner</label>
                    <textarea v-model="form.instructions" :class="areaStyle" rows="8" required></textarea>
                </div>
            </div>

            <!-- Knappar -->
            <div class="flex justify-end gap-3 border-t border-[#deddd9] pt-4">
                <button type="button" @click="emit('cancel')"
                    class="rounded-[9px] border border-[#d0cfcc] px-5 py-2.5 text-xs font-semibold text-[#6b6b6b] transition hover:bg-black/5 sm:text-sm">
                    Avbryt
                </button>
                <button type="submit"
                    class="rounded-[9px] bg-[#b89a72] px-5 py-2.5 text-xs font-semibold text-white transition hover:bg-[#a7875f] sm:text-sm">
                    Spara ändringar
                </button>
            </div>
        </form>

        <!-- Modal för bildbyte -->
        <ImageUploadModal :show="showImageModal" :initial-image="form.image" :initial-position="form.imagePosition"
            @close="showImageModal = false" @confirm="handleImageConfirmed" />
    </div>
</template>