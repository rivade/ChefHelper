<script setup lang="ts">
import { computed } from "vue";
import type { Recipe } from "../../types/recipe.ts";

const props = defineProps<{ recipe: Recipe }>();
const emit = defineEmits<{ select: [recipe: Recipe] }>();
const fallbackImage = "https://images.unsplash.com/photo-1498837167922-ddd27525d352?w=600&auto=format&fit=crop";

const difficultyLabel = computed(() => {
	const value = String(props.recipe.difficulty).replace(/^\s*\d+\s*-\s*/, "").trim();
	if (value !== String(props.recipe.difficulty)) return value;
	if (value === "1") return "Lätt";
	if (value === "2") return "Medel";
	if (value === "3") return "Komplex";
	return value;
});

function handleImageError(event: Event) {
	(event.target as HTMLImageElement).src = fallbackImage;
}
</script>

<template>
	<article class="flex flex-col justify-between overflow-hidden rounded-xl bg-white p-4 shadow-sm transition hover:shadow-md">
		<div>
			<img
				:src="recipe.image || fallbackImage"
				:alt="recipe.title"
				:style="{ objectPosition: recipe.imagePosition || 'center center' }"
				@error="handleImageError"
				class="h-44 w-full rounded-lg object-cover"
			/>

			<div class="mt-3 flex items-center justify-between">
				<span class="rounded bg-[#b4895e]/15 px-2 py-0.5 text-xs font-medium text-[#8c6847]">
					{{ difficultyLabel }}
				</span>
				<span class="text-xs text-gray-500">{{ recipe.time }}</span>
			</div>

			<h2 class="mt-2 text-lg font-bold text-[#1a1a1a]">{{ recipe.title }}</h2>
			<p class="mt-1 line-clamp-2 text-xs text-gray-600">{{ recipe.description }}</p>
		</div>

		<div class="mt-4 flex items-center justify-between border-t border-[#deddd9] pt-3">
			<button
				type="button"
				class="rounded-lg bg-[#b89a72] px-3 py-2 text-sm font-semibold text-white transition hover:bg-[#a7875f] focus-visible:outline-2 focus-visible:outline-offset-2 focus-visible:outline-[#8c6847]"
				@click="emit('select', recipe)"
			>
				Visa recept
			</button>
		</div>
	</article>
</template>