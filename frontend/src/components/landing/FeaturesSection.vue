<script setup lang="ts">
import { computed, onMounted, onUnmounted, ref } from "vue";
import FeatureCard from "./FeatureCard.vue";
import SearchIcon from "./icons/SearchIcon.vue";
import BookmarkIcon from "./icons/BookmarkIcon.vue";
import ShareIcon from "./icons/ShareIcon.vue";

const isMobileView = ref(false);
const mobileQuery = window.matchMedia("(max-width: 767px)");
const activeCardIndex = ref(0);
let rotationTimer: ReturnType<typeof window.setInterval> | undefined;

const featureCards = [
  {
    title: "Hitta recept",
    description: "Sök bland recept från hela världen och filtrera efter dina preferenser.",
    icon: SearchIcon,
  },
  {
    title: "Spara favoriter",
    description: "Samla dina favoritrecept på ett ställe och kom åt dem när som helst.",
    icon: BookmarkIcon,
  },
  {
    title: "Dela med vänner",
    description: "Dela dina egna recept och inspirera andra matälskare i gemenskapen.",
    icon: ShareIcon,
  },
];

const carouselTrackStyle = computed(() => ({
  transform: `translateX(calc(-50% + var(--carousel-step) - ${activeCardIndex.value} * var(--carousel-step)))`,
}));

function updateMobileView(isMobile: boolean) {
  isMobileView.value = isMobile;

  if (isMobile) {
    startAutoRotation();
  } else {
    stopAutoRotation();
  }
}

function startAutoRotation() {
  stopAutoRotation();
  rotationTimer = window.setInterval(showNextCard, 4000);
}

function stopAutoRotation() {
  if (rotationTimer) {
    window.clearInterval(rotationTimer);
    rotationTimer = undefined;
  }
}

function showNextCard() {
  activeCardIndex.value = (activeCardIndex.value + 1) % featureCards.length;
}

onMounted(() => {
  updateMobileView(mobileQuery.matches);
  mobileQuery.addEventListener("change", handleViewportChange);
});

onUnmounted(() => {
  stopAutoRotation();
  mobileQuery.removeEventListener("change", handleViewportChange);
});

function handleViewportChange(event: MediaQueryListEvent) {
  updateMobileView(event.matches);
}
</script>

<template>
  <section v-if="isMobileView">
    <div class="carousel-viewport px-5 pt-12 pb-5" aria-live="polite">
      <div class="carousel-track" :style="carouselTrackStyle">
        <div
          v-for="(card, index) in featureCards"
          :key="card.title"
          class="carousel-card"
          :class="{ 'carousel-card-active': index === activeCardIndex }"
          :aria-hidden="index !== activeCardIndex"
        >
          <FeatureCard :title="card.title" :description="card.description">
            <template #icon>
              <component :is="card.icon" />
            </template>
          </FeatureCard>
        </div>
      </div>
    </div>
  </section>

  <section v-else class="flex flex-wrap justify-center gap-5 px-5 pt-12 pb-5">
    <FeatureCard
      v-for="card in featureCards"
      :key="card.title"
      :title="card.title"
      :description="card.description"
    >
      <template #icon>
        <component :is="card.icon" />
      </template>
    </FeatureCard>
  </section>
</template>

<style scoped>
.carousel-viewport {
  --carousel-card-width: min(340px, 78vw);
  --carousel-gap: 1rem;
  --carousel-step: calc(var(--carousel-card-width) + var(--carousel-gap));
  width: 100%;
  overflow: hidden;
}

.carousel-track {
  position: relative;
  left: 50%;
  display: flex;
  gap: var(--carousel-gap);
  width: max-content;
  transition: transform 0.7s ease-in-out;
}

.carousel-card {
  flex: 0 0 var(--carousel-card-width);
  opacity: 0.5;
  transform: scale(0.9);
  transition: opacity 0.7s ease, transform 0.7s ease;
}

.carousel-card-active {
  opacity: 1;
  transform: scale(1);
}
</style>
