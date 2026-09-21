<script setup lang="ts">
import HeroSection from "../components/landing/HeroSection.vue";
import FeaturesSection from "../components/landing/FeaturesSection.vue";
import LandingFooter from "../components/landing/LandingFooter.vue";
</script>

<template>
  <main class="flex min-h-[calc(100vh-72px)] flex-col justify-between bg-[#F9F9F9]">
    <div>
      <HeroSection />
      <FeaturesSection />
    </div>
    <LandingFooter />
  </main>
</template>