<script setup lang="ts">
import { useRouter } from "vue-router";

const router = useRouter();
</script>

<template>
  <section class="flex min-h-[50vh] flex-col items-center px-5 pt-20 pb-20 text-center">
    <h1
      class="whitespace-nowrap bg-gradient-to-r from-[#E8A857] to-[#B5602F] bg-clip-text px-2 text-[clamp(5rem,16vw,9rem)] font-bold leading-[1.15] text-transparent"
      style="font-family: 'Caveat'"
    >
      ChefHelper
    </h1>

    <p class="mt-5 max-w-lg text-[1.85rem] text-[#6B6B6B]">Hitta och samla recept!</p>

    <div class="mt-12 flex items-center gap-5">
      <button
        type="button"
        class="rounded-[10px] bg-[#C3A078] px-10 py-4 text-lg font-semibold text-white shadow-[0_2px_8px_0_rgba(45,106,79,0.18)]"
        @click="router.push('/signup')"
      >
        Skapa konto
      </button>
      <button
        type="button"
        class="rounded-[10px] border border-[#DEDED8] bg-white px-10 py-4 text-lg font-semibold text-[#1A1A1A] shadow-[0_2px_8px_0_rgba(0,0,0,0.06)]"
        @click="router.push('/login')"
      >
        Logga in
      </button>
    </div>
  </section>
</template>

<style scoped>
button {
  transition: transform 0.2s ease;
  
  will-change: transform;
  backface-visibility: hidden;
}

button:hover {
  transform: scale(1.05);
  cursor: pointer;
}
</style>
