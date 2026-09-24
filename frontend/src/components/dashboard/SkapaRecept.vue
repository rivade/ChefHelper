<script setup lang="ts">
import { computed, ref } from "vue";

const emit = defineEmits<{
    cancel: [];
    saved: [recipe: RecipePayload];
}>();

type RecipePayload = {
    author: string;
    title: string;
    description: string;
    ingredients: string;
    instructions: string;
    cookingtime: [number, number];
    portions: number;
    difficulty: number;
};

const author = ref("");
const title = ref("");
const description = ref("");
const cookingHours = ref("");
const cookingMinutes = ref("");
const portions = ref("");
const difficulty = ref(1);
const ingredients = ref("");
const instructions = ref("");
const submitted = ref(false);

// Dropdown-status och alternativ för svårighetsgrad
const isDifficultyOpen = ref(false);
const difficultyOptions = [
    { value: 1, label: "1 - Lätt" },
    { value: 2, label: "2" },
    { value: 3, label: "3 - Medel" },
    { value: 4, label: "4" },
    { value: 5, label: "5 - Komplex" },
];

const selectedDifficultyLabel = computed(
    () => difficultyOptions.find((o) => o.value === difficulty.value)?.label ?? "Välj svårighetsgrad"
);

const numericValues = computed(() => ({
    cookingHours: cookingHours.value === "" ? NaN : Number(cookingHours.value),
    cookingMinutes: cookingMinutes.value === "" ? NaN : Number(cookingMinutes.value),
    portions: portions.value === "" ? NaN : Number(portions.value),
}));

const errors = computed(() => ({
    author: author.value.trim() ? "" : "Författare krävs.",
    title: title.value.trim() ? "" : "Namn krävs.",
    description: description.value.trim() ? "" : "Beskrivning krävs.",
    ingredients: ingredients.value.trim() ? "" : "Ingredienser krävs.",
    instructions: instructions.value.trim() ? "" : "Instruktioner krävs.",
    cookingtime:
        !Number.isInteger(numericValues.value.cookingHours) ||
            numericValues.value.cookingHours < 0 ||
            numericValues.value.cookingHours > 72
            ? "Timmar måste vara mellan 0 och 72."
            : !Number.isInteger(numericValues.value.cookingMinutes) ||
                numericValues.value.cookingMinutes < 0 ||
                numericValues.value.cookingMinutes > 59
                ? "Minuter måste vara mellan 0 och 59."
                : "",
    portions:
        !isNaN(numericValues.value.portions) &&
            numericValues.value.portions > 0 &&
            numericValues.value.portions <= 100
            ? ""
            : "Portioner måste vara mellan 1 och 100.",
    difficulty:
        difficulty.value >= 1 && difficulty.value <= 5
            ? ""
            : "Svårighetsgrad måste vara mellan 1 och 5.",
}));

const canSave = computed(() =>
    Object.values(errors.value).every((error) => !error),
);

function selectDifficulty(val: number) {
    difficulty.value = val;
    isDifficultyOpen.value = false;
}

function handleHoursInput() {
    if (Number(cookingHours.value) > 72) {
        cookingHours.value = "72";
    }
}

function handleMinutesInput() {
    if (Number(cookingMinutes.value) > 59) {
        cookingMinutes.value = "59";
    }
}

function handlePortionsInput() {
    if (Number(portions.value) > 100) {
        portions.value = "100";
    }
}

function saveRecipe() {
    submitted.value = true;
    if (!canSave.value) return;

    emit("saved", {
        author: author.value.trim(),
        title: title.value.trim(),
        description: description.value.trim(),
        ingredients: ingredients.value.trim(),
        instructions: instructions.value.trim(),
        cookingtime: [
            numericValues.value.cookingHours,
            numericValues.value.cookingMinutes,
        ],
        portions: numericValues.value.portions,
        difficulty: difficulty.value,
    });
}

function cancel() {
    emit("cancel");
}
</script>

<template>
    <main class="flex h-full w-full flex-col overflow-hidden bg-[#f1f1f0] p-3 font-['Roboto'] text-[#1a1a1a] sm:p-5">
        <form class="mx-auto flex h-full w-full max-w-[1272px] flex-1 flex-col min-h-0" @submit.prevent="saveRecipe">

            <!-- Rubrik -->
            <div class="shrink-0 mb-3 border-b border-[#deddd9] pb-2">
                <h1 class="text-xl font-bold sm:text-2xl">Skapa recept</h1>
            </div>

            <!-- Trekolumnsgrid -->
            <div class="grid flex-1 grid-cols-1 gap-4 lg:grid-cols-3 lg:gap-6 min-h-0">

                <!-- Kolumn 1 -->
                <section class="flex flex-col flex-1 gap-4 min-h-0">
                    <label class="block shrink-0">
                        <span class="mb-1.5 flex items-center gap-2 text-sm font-semibold sm:text-base">
                            <b
                                class="grid h-6 w-6 place-items-center rounded-md bg-[#b4895e] text-xs font-normal text-white">1</b>
                            Namn
                        </span>
                        <input v-model="title"
                            class="w-full rounded-[9px] bg-[#dededc] px-3.5 py-2.5 text-xs outline-none transition focus:bg-[#e5e4e1] focus:ring-2 focus:ring-[#b4895e]/40 sm:text-sm"
                            placeholder="Ge ditt recept ett namn!" required />
                    </label>

                    <label class="flex flex-col flex-1 min-h-0">
                        <span class="mb-1.5 flex items-center gap-2 text-sm font-semibold sm:text-base shrink-0">
                            <b
                                class="grid h-6 w-6 place-items-center rounded-md bg-[#b4895e] text-xs font-normal text-white">2</b>
                            Beskrivning
                        </span>
                        <textarea v-model="description"
                            class="w-full flex-1 min-h-0 resize-none rounded-[9px] bg-[#dededc] p-3 text-xs outline-none transition focus:bg-[#e5e4e1] focus:ring-2 focus:ring-[#b4895e]/40 sm:text-sm"
                            placeholder="Skriv en kort beskrivning om vad det är för recept..." required></textarea>
                    </label>

                    <div class="shrink-0">
                        <span class="mb-1.5 flex items-center gap-2 text-sm font-semibold sm:text-base">
                            <b
                                class="grid h-6 w-6 place-items-center rounded-md bg-[#b4895e] text-xs font-normal text-white">3</b>
                            Tid och portioner
                        </span>
                        <div class="grid grid-cols-2 gap-2.5">
                            <input v-model="cookingHours"
                                class="w-full rounded-[9px] bg-[#dededc] px-3.5 py-2.5 text-xs outline-none transition focus:bg-[#e5e4e1] focus:ring-2 focus:ring-[#b4895e]/40 sm:text-sm"
                                type="number" min="0" max="72" placeholder="Timmar" @input="handleHoursInput" />
                            <input v-model="cookingMinutes"
                                class="w-full rounded-[9px] bg-[#dededc] px-3.5 py-2.5 text-xs outline-none transition focus:bg-[#e5e4e1] focus:ring-2 focus:ring-[#b4895e]/40 sm:text-sm"
                                type="number" min="0" max="59" placeholder="Minuter" @input="handleMinutesInput" />
                        </div>
                        <input v-model="portions"
                            class="mt-2.5 w-full rounded-[9px] bg-[#dededc] px-3.5 py-2.5 text-xs outline-none transition focus:bg-[#e5e4e1] focus:ring-2 focus:ring-[#b4895e]/40 sm:text-sm"
                            type="number" min="1" max="100" placeholder="Portioner" @input="handlePortionsInput" />
                        <p v-if="submitted && errors.cookingtime" class="mt-1 text-xs text-[#b42318]">{{
                            errors.cookingtime }}</p>
                        <p v-if="submitted && errors.portions" class="mt-1 text-xs text-[#b42318]">{{ errors.portions }}
                        </p>
                    </div>
                </section>

                <!-- Kolumn 2 -->
                <section class="flex flex-col flex-1 gap-4 min-h-0">

                    <!-- Custom Dropdown för Svårighetsgrad -->
                    <div class="block shrink-0">
                        <span class="mb-1.5 flex items-center gap-2 text-sm font-semibold sm:text-base">
                            <b
                                class="grid h-6 w-6 place-items-center rounded-md bg-[#b4895e] text-xs font-normal text-white">4</b>
                            Svårighetsgrad
                        </span>

                        <button type="button" @click="isDifficultyOpen = !isDifficultyOpen"
                            class="flex w-full items-center justify-between rounded-[9px] bg-[#dededc] px-3.5 py-2.5 text-xs text-[#1a1a1a] outline-none transition-colors duration-200 focus:bg-[#e5e4e1] focus:ring-2 focus:ring-[#b4895e]/40 sm:text-sm">
                            <span>{{ selectedDifficultyLabel }}</span>
                            <svg class="h-4 w-4 text-[#6b6b6b] transition-transform duration-300"
                                :class="{ 'rotate-180': isDifficultyOpen }" fill="none" stroke="currentColor"
                                viewBox="0 0 24 24">
                                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2"
                                    d="M19 9l-7 7-7-7" />
                            </svg>
                        </button>

                        <!-- Dropdown-meny -->
                        <div class="grid transition-all duration-300 ease-in-out"
                            :class="isDifficultyOpen ? 'grid-rows-[1fr] opacity-100 mt-2' : 'grid-rows-[0fr] opacity-0 mt-0'">
                            <div class="overflow-hidden">
                                <div class="flex flex-col gap-1 rounded-[9px] bg-[#dededc] p-2">
                                    <button v-for="option in difficultyOptions" :key="option.value" type="button"
                                        @click="selectDifficulty(option.value)"
                                        class="w-full rounded-md px-3 py-2 text-left text-xs transition-colors duration-150 sm:text-sm"
                                        :class="difficulty === option.value
                                            ? 'bg-[#b4895e] font-medium text-white'
                                            : 'text-[#1a1a1a] hover:bg-[#e5e4e1]'
                                            ">
                                        {{ option.label }}
                                    </button>
                                </div>
                            </div>
                        </div>
                    </div>

                    <!-- Ingredienser -->
                    <label class="flex flex-col flex-1 min-h-0">
                        <span class="mb-1.5 flex items-center gap-2 text-sm font-semibold sm:text-base shrink-0">
                            <b
                                class="grid h-6 w-6 place-items-center rounded-md bg-[#b4895e] text-xs font-normal text-white">5</b>
                            Ingredienser
                        </span>
                        <textarea v-model="ingredients"
                            class="w-full flex-1 min-h-0 resize-none rounded-[9px] bg-[#dededc] p-3 text-xs outline-none transition focus:bg-[#e5e4e1] focus:ring-2 focus:ring-[#b4895e]/40 sm:text-sm"
                            placeholder="Lista vilka ingredienser som behövs för ditt recept, exempelvis:&#10;&#10;• Ris&#10;• Nötfärs&#10;• Paprika&#10;&#10;etc..."
                            required></textarea>
                    </label>
                </section>

                <!-- Kolumn 3 -->
                <section class="flex flex-col flex-1 gap-4 min-h-0">
                    <label class="flex flex-col flex-1 min-h-0">
                        <span class="mb-1.5 flex items-center gap-2 text-sm font-semibold sm:text-base shrink-0">
                            <b
                                class="grid h-6 w-6 place-items-center rounded-md bg-[#b4895e] text-xs font-normal text-white">6</b>
                            Steg för steg
                        </span>
                        <textarea v-model="instructions"
                            class="w-full flex-1 min-h-0 resize-none rounded-[9px] bg-[#dededc] p-3 text-xs outline-none transition focus:bg-[#e5e4e1] focus:ring-2 focus:ring-[#b4895e]/40 sm:text-sm"
                            placeholder="Gå igenom steg för steg hur förberedelse och tillagning går till i receptet, exempelvis:&#10;&#10;1. Skölj riset tills vattnet blir klart&#10;2. Skär paprikan i tunna strimlor&#10;3. Börja bryn köttfärsen i en het panna&#10;&#10;etc..."
                            required></textarea>
                    </label>

                    <!-- Knappar -->
                    <div class="shrink-0 pt-1">
                        <p v-if="submitted && !canSave" class="mb-2 text-xs text-red-700">
                            Fyll i alla obligatoriska fält innan receptet sparas.
                        </p>

                        <div class="flex flex-col-reverse gap-2.5 sm:flex-row sm:justify-end">
                            <button type="button"
                                class="rounded-[9px] border border-[#d0cfcc] px-5 py-2.5 text-xs font-semibold text-[#6b6b6b] transition hover:bg-black/5 sm:text-sm"
                                @click="cancel">
                                Avbryt
                            </button>
                            <button type="submit"
                                class="rounded-[9px] bg-[#b89a72] px-5 py-2.5 text-xs font-semibold text-white transition hover:bg-[#a7875f] sm:text-sm">
                                Spara recept
                            </button>
                        </div>
                    </div>
                </section>

            </div>
        </form>
    </main>
</template>