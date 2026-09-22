<script setup lang="ts">
import { ref } from "vue";
import Recipes from "@/components/dashboard/Recipes.vue";
import NavBar from "@/components/dashboard/Navbar.vue";

const search = ref("");
</script>

<template>
  <div
    class="min-h-[calc(100vh-74px)] bg-[#dfa06094] font-['Roboto'] text-[#1a1a1a]"
  >
    <div
      class="grid min-h-[calc(100vh-74px)] grid-cols-1 lg:grid-cols-[218px_1fr]"
    >
      <NavBar />

      <main class="min-w-0 p-4 sm:p-5 lg:p-[34px_30px_48px]">
        <section
          class="mb-8 hidden flex-col gap-3 sm:relative sm:mb-10 sm:flex sm:h-[34px] sm:flex-row sm:items-center sm:justify-center"
        >
          <button
            type="button"
            class="h-[34px] w-full rounded-lg bg-black text-sm font-semibold text-white transition duration-200 hover:bg-[#2d2d2d] sm:absolute sm:left-0 sm:w-24 sm:hover:-translate-y-0.5"
          >
            ☷ Filter
          </button>

          <label
            class="flex h-[34px] w-full items-center gap-3 rounded-lg bg-white px-3 transition duration-200 focus-within:ring-4 focus-within:ring-white/40 sm:max-w-[306px]"
          >
            <span class="text-xl">⌕</span>

            <input
              v-model="search"
              type="search"
              placeholder="Sök recept"
              class="w-full min-w-0 bg-transparent text-sm outline-none"
            />
          </label>
        </section>

        <Recipes :search="search" />
      </main>
    </div>
  </div>
</template>