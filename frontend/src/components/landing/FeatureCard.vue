<script setup lang="ts">
defineProps<{
  title: string;
  description: string;
}>();
</script>

<template>
  <div
    class="w-full max-w-[340px] rounded-[16px] border border-[#EFEFEB] bg-white p-6 shadow-[0_2px_12px_0_rgba(0,0,0,0.04)]"
  >
    <div
      class="flex h-12 w-12 items-center justify-center rounded-[10px] bg-[#FAF5D2]"
    >
      <slot name="icon" />
    </div>

    <h3 class="mt-6 text-lg font-bold text-[#1A1A1A]">{{ title }}</h3>
    <p class="mt-4 text-base leading-[1.55] text-[#6B6B6B]">{{ description }}</p>
  </div>
</template>
