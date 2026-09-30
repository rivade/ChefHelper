<script setup lang="ts">
import { computed, ref, reactive, onUnmounted } from "vue";

export type RecipePayload = {
    title: string; description: string; ingredients: string; instructions: string;
    cookingtime: [number, number]; portions: number; difficulty: number; image?: string; imagePosition?: string;
};

const emit = defineEmits<{ cancel: []; saved: [recipe: RecipePayload, isPrivate: boolean] }>();

const inputStyle = "w-full rounded-[9px] bg-[#dededc] px-3.5 py-2.5 text-xs text-[#1a1a1a] outline-none transition focus:bg-[#e5e4e1] focus:ring-2 focus:ring-[#b4895e]/40 sm:text-sm placeholder:text-[#8f8f8e]";
const areaStyle = "w-full flex-1 min-h-0 resize-none rounded-[9px] bg-[#dededc] p-3 text-xs text-[#1a1a1a] outline-none transition focus:bg-[#e5e4e1] focus:ring-2 focus:ring-[#b4895e]/40 sm:text-sm placeholder:text-[#8f8f8e]";
const badgeStyle = "grid h-6 w-6 shrink-0 place-items-center rounded-md bg-[#b4895e] text-xs font-semibold text-white";

const form = reactive({ title: "", description: "", cookingHours: "", cookingMinutes: "", portions: "", difficulty: 1, ingredients: "", instructions: "" });
const submitted = ref(false), isDifficultyOpen = ref(false), showUploadModal = ref(false), isDraggingFile = ref(false), isDraggingFocus = ref(false);
const selectedImage = ref(""), imagePosition = ref("50% 50%"), focusPoint = ref({ x: 50, y: 50 });
const selectedFile = ref<File | null>(null);
const fileInputRef = ref<HTMLInputElement | null>(null), imageContainerRef = ref<HTMLElement | null>(null);

const difficultyOptions = [{ value: 1, label: "1 - Lätt" }, { value: 2, label: "2 - Medel" }, { value: 3, label: "3 - Komplex" }];
const selectedDifficultyLabel = computed(() => difficultyOptions.find((o) => o.value === form.difficulty)?.label ?? "1 - Lätt");

const hours = computed(() => form.cookingHours === "" ? 0 : Number(form.cookingHours));
const minutes = computed(() => form.cookingMinutes === "" ? 0 : Number(form.cookingMinutes));
const portionsNum = computed(() => form.portions === "" ? NaN : Number(form.portions));

const errors = computed(() => ({
    title: form.title.trim() ? "" : "Namn krävs.",
    description: form.description.trim() ? "" : "Beskrivning krävs.",
    ingredients: form.ingredients.trim() ? "" : "Ingredienser krävs.",
    instructions: form.instructions.trim() ? "" : "Instruktioner krävs.",
    cookingtime: !Number.isInteger(hours.value) || hours.value < 0 || hours.value > 72 ? "Timmar måste vara mellan 0 och 72."
        : !Number.isInteger(minutes.value) || minutes.value < 0 || minutes.value > 59 ? "Minuter måste vara mellan 0 och 59."
            : hours.value === 0 && minutes.value === 0 ? "Minst timmar eller minuter måste anges." : "",
    portions: !isNaN(portionsNum.value) && portionsNum.value > 0 && portionsNum.value <= 100 ? "" : "Portioner måste vara mellan 1 och 100.",
}));

const canSave = computed(() => Object.values(errors.value).every((err) => !err));

const preventInvalidNumberKeys = (e: KeyboardEvent) => ["e", "E", "+", "-", ".", ","].includes(e.key) && e.preventDefault();

const clamp = (field: "cookingHours" | "cookingMinutes" | "portions", max: number) => {
    if (form[field] === "") return;
    const cleanVal = String(form[field]).replace(/\D/g, "");
    form[field] = cleanVal === "" ? "" : String(Math.min(Number(cleanVal), max));
};

const handleFormSubmit = () => { submitted.value = true; if (canSave.value) showUploadModal.value = true; };

const processFile = (file?: File) => {
    if (!file) return;
    if (file.type.startsWith("image/")) {
        if (selectedImage.value) URL.revokeObjectURL(selectedImage.value);
        selectedImage.value = URL.createObjectURL(file);
        selectedFile.value = file;
        imagePosition.value = "50% 50%";
        focusPoint.value = { x: 50, y: 50 };
    } else alert("Vänligen välj en giltig bildfil.");
};

const handleFileSelect = (e: Event) => processFile((e.target as HTMLInputElement).files?.[0]);
const handleDrop = (e: DragEvent) => { isDraggingFile.value = false; processFile(e.dataTransfer?.files?.[0]); };

const resetImage = () => {
    if (selectedImage.value) URL.revokeObjectURL(selectedImage.value);
    selectedImage.value = ""; imagePosition.value = "50% 50%"; focusPoint.value = { x: 50, y: 50 };
    selectedFile.value = null;
    if (fileInputRef.value) fileInputRef.value.value = "";
};

const updateFocusFromPointer = (e: PointerEvent) => {
    if (!imageContainerRef.value) return;
    const rect = imageContainerRef.value.getBoundingClientRect();
    const x = Math.max(0, Math.min(100, Math.round(((e.clientX - rect.left) / rect.width) * 100)));
    const y = Math.max(0, Math.min(100, Math.round(((e.clientY - rect.top) / rect.height) * 100)));
    focusPoint.value = { x, y };
    imagePosition.value = `${x}% ${y}%`;
};

const startFocusDrag = (e: PointerEvent) => {
    e.preventDefault(); isDraggingFocus.value = true; updateFocusFromPointer(e);
    window.addEventListener("pointermove", updateFocusFromPointer);
    window.addEventListener("pointerup", stopFocusDrag);
};

const stopFocusDrag = () => {
    isDraggingFocus.value = false;
    window.removeEventListener("pointermove", updateFocusFromPointer);
    window.removeEventListener("pointerup", stopFocusDrag);
};

onUnmounted(() => {
    stopFocusDrag();
    if (selectedImage.value) URL.revokeObjectURL(selectedImage.value);
});

const readImageAsDataUrl = (file: File) => new Promise<string>((resolve, reject) => {
    const reader = new FileReader();
    reader.onload = () => typeof reader.result === "string"
        ? resolve(reader.result)
        : reject(new Error("Could not read image file"));
    reader.onerror = () => reject(reader.error ?? new Error("Could not read image file"));
    reader.readAsDataURL(file);
});

const finalizeSave = async (savePrivate: boolean) => {
    try {
        const image = selectedFile.value ? await readImageAsDataUrl(selectedFile.value) : "";
        showUploadModal.value = false;
        emit("saved", {
            title: form.title.trim(), description: form.description.trim(), ingredients: form.ingredients.trim(), instructions: form.instructions.trim(),
            cookingtime: [hours.value, minutes.value], portions: portionsNum.value, difficulty: form.difficulty,
            image, imagePosition: imagePosition.value,
        }, savePrivate);
    } catch {
        alert("Kunde inte läsa bildfilen.");
    }
};
</script>

<template>
    <main class="flex h-full w-full flex-col overflow-hidden bg-[#f1f1f0] p-4 font-['Roboto'] text-[#1a1a1a] sm:p-6">
        <form class="mx-auto flex h-full w-full max-w-[1272px] flex-1 flex-col min-h-0"
            @submit.prevent="handleFormSubmit">
            <div class="shrink-0 mb-4 border-b border-[#deddd9] pb-3">
                <h1 class="text-2xl font-bold text-[#1a1a1a]">Skapa recept</h1>
            </div>

            <div class="grid flex-1 grid-cols-1 gap-5 lg:grid-cols-3 lg:gap-6 min-h-0">
                <!-- Column 1 -->
                <section class="flex flex-col flex-1 gap-4 min-h-0">
                    <label class="block shrink-0">
                        <span class="mb-1.5 flex items-center gap-2 text-sm font-bold text-[#1a1a1a]">
                            <span :class="badgeStyle">1</span> Namn
                        </span>
                        <input v-model="form.title" :class="inputStyle" placeholder="Ge ditt recept ett namn!"
                            required />
                        <p v-if="submitted && errors.title" class="mt-1 text-xs text-[#b42318]">{{ errors.title }}</p>
                    </label>

                    <label class="flex flex-col flex-1 min-h-0">
                        <span class="mb-1.5 flex items-center gap-2 text-sm font-bold text-[#1a1a1a] shrink-0">
                            <span :class="badgeStyle">2</span> Beskrivning
                        </span>
                        <textarea v-model="form.description" :class="areaStyle"
                            placeholder="Skriv en kort beskrivning om vad det är för recept..." required></textarea>
                        <p v-if="submitted && errors.description" class="mt-1 text-xs text-[#b42318]">{{
                            errors.description }}</p>
                    </label>

                    <div class="shrink-0">
                        <span class="mb-1.5 flex items-center gap-2 text-sm font-bold text-[#1a1a1a]">
                            <span :class="badgeStyle">3</span> Tid och portioner
                        </span>
                        <div class="grid grid-cols-2 gap-2.5">
                            <input v-model="form.cookingHours" :class="inputStyle" type="number" min="0" max="72"
                                placeholder="Timmar" @keydown="preventInvalidNumberKeys"
                                @input="clamp('cookingHours', 72)" />
                            <input v-model="form.cookingMinutes" :class="inputStyle" type="number" min="0" max="59"
                                placeholder="Minuter" @keydown="preventInvalidNumberKeys"
                                @input="clamp('cookingMinutes', 59)" />
                        </div>
                        <input v-model="form.portions" :class="[inputStyle, 'mt-2.5']" type="number" min="1" max="100"
                            placeholder="Portioner" @keydown="preventInvalidNumberKeys"
                            @input="clamp('portions', 100)" />
                        <p v-if="submitted && errors.cookingtime" class="mt-1 text-xs text-[#b42318]">{{
                            errors.cookingtime }}</p>
                        <p v-if="submitted && errors.portions" class="mt-1 text-xs text-[#b42318]">{{ errors.portions }}
                        </p>
                    </div>
                </section>

                <!-- Column 2 -->
                <section class="flex flex-col flex-1 gap-4 min-h-0">
                    <div class="block shrink-0">
                        <span class="mb-1.5 flex items-center gap-2 text-sm font-bold text-[#1a1a1a]">
                            <span :class="badgeStyle">4</span> Svårighetsgrad
                        </span>
                        <div class="relative">
                            <button type="button" @click="isDifficultyOpen = !isDifficultyOpen"
                                class="flex w-full items-center justify-between rounded-[9px] bg-[#dededc] px-3.5 py-2.5 text-xs text-[#1a1a1a] outline-none transition-colors focus:bg-[#e5e4e1] focus:ring-2 focus:ring-[#b4895e]/40 sm:text-sm">
                                <span>{{ selectedDifficultyLabel }}</span>
                                <svg class="h-4 w-4 text-[#6b6b6b] transition-transform duration-200"
                                    :class="{ 'rotate-180': isDifficultyOpen }" fill="none" stroke="currentColor"
                                    viewBox="0 0 24 24">
                                    <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2"
                                        d="M19 9l-7 7-7-7" />
                                </svg>
                            </button>
                            <div v-if="isDifficultyOpen"
                                class="absolute left-0 right-0 top-full z-10 mt-1 rounded-[9px] bg-[#dededc] p-1.5 shadow-lg">
                                <button v-for="option in difficultyOptions" :key="option.value" type="button"
                                    @click="form.difficulty = option.value; isDifficultyOpen = false;"
                                    class="w-full rounded-md px-3 py-2 text-left text-xs transition-colors sm:text-sm"
                                    :class="form.difficulty === option.value ? 'bg-[#b4895e] font-semibold text-white' : 'text-[#1a1a1a] hover:bg-[#e5e4e1]'">
                                    {{ option.label }}
                                </button>
                            </div>
                        </div>
                    </div>

                    <label class="flex flex-col flex-1 min-h-0">
                        <span class="mb-1.5 flex items-center gap-2 text-sm font-bold text-[#1a1a1a] shrink-0">
                            <span :class="badgeStyle">5</span> Ingredienser
                        </span>
                        <textarea v-model="form.ingredients" :class="areaStyle"
                            :placeholder="'Lista vilka ingredienser som behövs för ditt recept, exempelvis:\n\n• Ris\n• Nötfärs\n• Paprika\n\netc...'"
                            required></textarea>
                        <p v-if="submitted && errors.ingredients" class="mt-1 text-xs text-[#b42318]">{{
                            errors.ingredients }}</p>
                    </label>
                </section>

                <!-- Column 3 -->
                <section class="flex flex-col flex-1 gap-4 min-h-0 justify-between">
                    <label class="flex flex-col flex-1 min-h-0">
                        <span class="mb-1.5 flex items-center gap-2 text-sm font-bold text-[#1a1a1a] shrink-0">
                            <span :class="badgeStyle">6</span> Steg för steg
                        </span>
                        <textarea v-model="form.instructions" :class="areaStyle"
                            :placeholder="'Gå igenom steg för steg hur förberedelse och tillagning går till i receptet, exempelvis:\n\n1. Skölj riset tills vattnet blir klart\n2. Skär paprikan i tunna strimlor\n3. Börja bryn köttfärsen i en het panna\n\netc...'"
                            required></textarea>
                        <p v-if="submitted && errors.instructions" class="mt-1 text-xs text-[#b42318]">{{
                            errors.instructions }}</p>
                    </label>

                    <div class="shrink-0 pt-2 flex flex-col items-end gap-2">
                        <p v-if="submitted && !canSave" class="text-xs text-[#b42318]">Fyll i alla obligatoriska fält
                            innan du sparar.</p>
                        <div class="flex items-center gap-3">
                            <button type="button" @click="emit('cancel')"
                                class="rounded-[9px] border border-[#d0cfcc] bg-[#dededc] px-6 py-2.5 text-xs font-bold text-[#5a5a5a] transition hover:bg-[#d4d4d2] sm:text-sm">
                                Avbryt
                            </button>
                            <button type="submit"
                                class="rounded-[9px] bg-[#b89a72] px-6 py-2.5 text-xs font-bold text-white transition hover:bg-[#a7875f] sm:text-sm shadow-xs">
                                Spara recept
                            </button>
                        </div>
                    </div>
                </section>
            </div>
        </form>

        <!-- Upload Image Modal -->
        <Teleport to="body">
            <div v-if="showUploadModal"
                class="fixed inset-0 z-50 flex items-center justify-center bg-black/60 p-4 backdrop-blur-xs select-none">
                <div class="w-full max-w-[380px] overflow-hidden rounded-[28px] bg-[#e3e3e1] shadow-2xl flex flex-col">
                    <input type="file" ref="fileInputRef" accept="image/*" class="hidden" @change="handleFileSelect" />

                    <!-- Dropzone -->
                    <div v-if="!selectedImage" @click="fileInputRef?.click()" @dragover.prevent="isDraggingFile = true"
                        @dragleave.prevent="isDraggingFile = false" @drop.prevent="handleDrop"
                        class="relative flex h-[210px] w-full cursor-pointer flex-col items-center justify-center bg-[#8f8f8e] p-6 text-center transition hover:bg-[#838382]"
                        :class="{ 'border-4 border-dashed border-[#b89a72] bg-[#7a7a79]': isDraggingFile }">
                        <div class="flex flex-col items-center justify-center">
                            <div class="mb-3 text-5xl">📷</div>
                            <p class="max-w-[240px] text-lg font-medium leading-snug text-[#2d2d2d]">Tryck här för att
                                ladda upp en bild</p>
                        </div>
                    </div>

                    <!-- Preview & Focus Point Selector -->
                    <div v-else class="relative bg-[#8f8f8e] p-3">
                        <div class="mb-2 flex items-center justify-between px-1">
                            <span class="text-[11px] font-medium text-white/90">👆 Dra för att justera fokuspunkt</span>
                            <button type="button" @click="resetImage"
                                class="rounded-md border border-white/20 bg-white/90 px-2.5 py-1 text-xs font-semibold text-[#1a1a1a] shadow-xs transition hover:bg-white">
                                📷 Byt bild
                            </button>
                        </div>

                        <div ref="imageContainerRef" @pointerdown="startFocusDrag"
                            class="relative h-[190px] w-full touch-none overflow-hidden rounded-xl bg-black/10 shadow-inner"
                            :class="isDraggingFocus ? 'cursor-grabbing' : 'cursor-grab'">
                            <img :src="selectedImage" alt="Vald bild"
                                class="h-full w-full object-cover pointer-events-none"
                                :style="{ objectPosition: imagePosition }" />
                            <div class="pointer-events-none absolute h-7 w-7 -translate-x-1/2 -translate-y-1/2 rounded-full border-2 border-white bg-[#b89a72]/80 shadow-md backdrop-blur-xs flex items-center justify-center transition-transform duration-75"
                                :class="{ 'scale-125 bg-[#b89a72]': isDraggingFocus }"
                                :style="{ left: `${focusPoint.x}%`, top: `${focusPoint.y}%` }">
                                <div class="h-2 w-2 rounded-full bg-white"></div>
                            </div>
                        </div>
                    </div>

                    <!-- Footer -->
                    <div class="flex flex-col items-center px-6 py-6 text-center bg-[#e3e3e1]">
                        <h2 class="text-2xl font-black text-[#000000] tracking-tight mb-2">Nu är du snart klar!</h2>
                        <p class="text-sm font-normal text-[#2d2d2d] leading-relaxed max-w-[290px] mb-6">
                            Innan du sparar ditt smarriga recept, kan du välja att lägga till en bild på maten. Det gör
                            du här ovan.
                        </p>
                        <div class="flex w-full items-center justify-center gap-4">
                            <button type="button" @click="finalizeSave(false)"
                                class="flex-1 rounded-2xl bg-[#b59873] py-3.5 text-center text-base font-bold text-white shadow-md transition hover:bg-[#a48662] active:scale-95">
                                Lägg upp
                            </button>
                            <button type="button" @click="finalizeSave(true)"
                                class="flex-1 rounded-2xl bg-[#9c9c9c] py-3.5 text-center text-base font-bold text-white shadow-md transition hover:bg-[#8b8b8b] active:scale-95">
                                Spara privat
                            </button>
                        </div>
                    </div>
                </div>
            </div>
        </Teleport>
    </main>
</template>