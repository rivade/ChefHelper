<script setup lang="ts">
import { ref, computed, onMounted, onUnmounted } from "vue";

export type ComplexityOption = "all" | "lätt" | "medel" | "komplex";

const props = withDefaults(
    defineProps<{
        modelValue?: ComplexityOption;
    }>(),
    {
        modelValue: "all",
    }
);

const emit = defineEmits<{
    (e: "update:modelValue", value: ComplexityOption): void;
}>();

const isOpen = ref(false);
const filterRef = ref<HTMLElement | null>(null);

const options: { label: string; value: ComplexityOption }[] = [
    { label: "Alla svårighetsgrader", value: "all" },
    { label: "Lätt", value: "lätt" },
    { label: "Medel", value: "medel" },
    { label: "Komplex", value: "komplex" },
];

const selectedLabel = computed(() => {
    return options.find((opt) => opt.value === props.modelValue)?.label ?? "Alla svårighetsgrader";
});

function selectOption(value: ComplexityOption) {
    emit("update:modelValue", value);
    isOpen.value = false;
}

function handleClickOutside(event: MouseEvent) {
    if (filterRef.value && !filterRef.value.contains(event.target as Node)) {
        isOpen.value = false;
    }
}

onMounted(() => {
    document.addEventListener("click", handleClickOutside);
});

onUnmounted(() => {
    document.removeEventListener("click", handleClickOutside);
});
</script>

<template>
    <div ref="filterRef" class="relative inline-block font-['Roboto'] text-[#1a1a1a]">
        <!-- Filter Toggle Button -->
        <button type="button" @click="isOpen = !isOpen"
            class="flex items-center gap-2.5 rounded-[9px] bg-[#dededc] px-4 py-2.5 text-xs font-semibold shadow-xs transition hover:bg-[#e5e4e1] focus:outline-none focus:ring-2 focus:ring-[#b89a72]/40 sm:text-sm">
            <svg class="h-4 w-4 text-[#5a5a5a]" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2"
                    d="M3 4a1 1 0 011-1h16a1 1 0 011 1v2.586a1 1 0 01-.293.707l-6.414 6.414a1 1 0 00-.293.707V17l-4 4v-6.586a1 1 0 00-.293-.707L3.293 7.293A1 1 0 013 6.586V4z" />
            </svg>

            <span>{{ selectedLabel }}</span>

            <!-- Active Filter Badge Counter -->
            <span v-if="props.modelValue !== 'all'" class="flex h-2 w-2 rounded-full bg-[#b89a72]"></span>

            <!-- Chevron Arrow -->
            <svg class="h-4 w-4 text-[#6b6b6b] transition-transform duration-200" :class="{ 'rotate-180': isOpen }"
                fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M19 9l-7 7-7-7" />
            </svg>
        </button>

        <!-- Dropdown Menu -->
        <Transition enter-active-class="transition duration-100 ease-out"
            enter-from-class="transform scale-95 opacity-0" enter-to-class="transform scale-100 opacity-100"
            leave-active-class="transition duration-75 ease-in" leave-from-class="transform scale-100 opacity-100"
            leave-to-class="transform scale-95 opacity-0">
            <div v-if="isOpen"
                class="absolute left-0 top-full z-20 mt-1.5 w-48 rounded-[9px] bg-[#dededc] p-1.5 shadow-lg border border-[#c2c2c0]">
                <button v-for="option in options" :key="option.value" type="button" @click="selectOption(option.value)"
                    class="flex w-full items-center justify-between rounded-md px-3 py-2 text-left text-xs transition-colors sm:text-sm"
                    :class="props.modelValue === option.value
                        ? 'bg-[#b89a72] font-semibold text-white'
                        : 'text-[#1a1a1a] hover:bg-[#e5e4e1]'
                        ">
                    <span>{{ option.label }}</span>
                    <svg v-if="props.modelValue === option.value" class="h-4 w-4 text-white" fill="none"
                        stroke="currentColor" viewBox="0 0 24 24">
                        <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2.5" d="M5 13l4 4L19 7" />
                    </svg>
                </button>
            </div>
        </Transition>
    </div>
</template>