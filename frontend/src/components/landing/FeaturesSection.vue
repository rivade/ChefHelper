<script setup lang="ts">
import FeatureCard from "./FeatureCard.vue";
import SearchIcon from "./icons/SearchIcon.vue";
import BookmarkIcon from "./icons/BookmarkIcon.vue";
import ShareIcon from "./icons/ShareIcon.vue";
</script>

<!--TODO:
Implementera en version av detta specifikt för mobilvy, så det blir en karusell där cardsen roterar istället för flexbox
-->


<template>
  <section
    class="flex flex-wrap justify-center gap-5 px-5 pt-12 pb-5"
  >
    <FeatureCard
      title="Hitta recept"
      description="Sök bland recept från hela världen och filtrera efter dina preferenser."
    >
      <template #icon>
        <SearchIcon />
      </template>
    </FeatureCard>

    <FeatureCard
      title="Spara favoriter"
      description="Samla dina favoritrecept på ett ställe och kom åt dem när som helst."
    >
      <template #icon>
        <BookmarkIcon />
      </template>
    </FeatureCard>

    <FeatureCard
      title="Dela med vänner"
      description="Dela dina egna recept och inspirera andra matälskare i gemenskapen."
    >
      <template #icon>
        <ShareIcon />
      </template>
    </FeatureCard>
  </section>
</template>
