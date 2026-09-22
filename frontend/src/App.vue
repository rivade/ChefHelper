<script setup lang="ts">
import { useRoute } from "vue-router";
import logo from "./assets/logo.svg";
const route = useRoute();
</script>

<template>
  <header class="h-[72px] bg-[#EFEFEB] p-3 font-['Roboto']">
    <nav class="flex h-full items-center justify-between">
      <RouterLink
        to="/"
        class="flex items-center gap-3 text-2xl font-extrabold"
      >
        <img :src="logo" alt="ChefHelper logo" class="h-12 w-12" />
        <span>ChefHelper</span>
      </RouterLink>

      <div class="flex items-center gap-6">
        <RouterLink
          v-if="route.path === '/'"
          to="/anonrecipebrowsing"
          class="font-semibold underline underline-offset-4"
          >Recept</RouterLink
        >
        <RouterLink to="/" class="font-semibold underline underline-offset-4"
          >Kontakt</RouterLink
        >
        <RouterLink to="/" class="font-semibold underline underline-offset-4"
          >Om oss</RouterLink
        >
      </div>
    </nav>
  </header>
  <RouterView />
</template>
