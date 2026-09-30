<script setup lang="ts">
import type { Recipe } from "../../types/recipe.ts";

defineProps<{ recipe: Recipe }>();
defineEmits<{ back: [] }>();

const fallbackImage = "https://images.unsplash.com/photo-1498837167922-ddd27525d352?w=800&auto=format&fit=crop";

function handleImageError(event: Event) {
	(event.target as HTMLImageElement).src = fallbackImage;
}

function getDifficultyLabel(difficulty: Recipe["difficulty"]): string {
	const value = String(difficulty).replace(/^\s*\d+\s*-\s*/, "").trim();
	if (value !== String(difficulty)) return value;
	if (value === "1") return "Lätt";
	if (value === "2") return "Medel";
	if (value === "3") return "Komplex";
	return value;
}
</script>

<template>
	<article class="mx-auto max-w-[1000px] rounded-xl bg-white p-5 shadow-sm sm:p-8">
		<div class="mb-6 border-b border-[#deddd9] pb-4">
			<button
				type="button"
				class="rounded-lg border border-[#d0cfcc] px-4 py-2 text-sm font-semibold text-[#555] transition hover:bg-black/5 focus-visible:outline-2 focus-visible:outline-offset-2 focus-visible:outline-[#8c6847]"
				@click="$emit('back')"
			>
				← Tillbaka till recepten
			</button>
		</div>

		<div class="grid grid-cols-1 gap-6 md:grid-cols-2">
			<img
				:src="recipe.image || fallbackImage"
				:alt="recipe.title"
				:style="{ objectPosition: recipe.imagePosition || 'center center' }"
				@error="handleImageError"
				class="h-64 w-full rounded-lg object-cover sm:h-80"
			/>

			<div class="flex flex-col justify-between">
				<div>
					<span class="inline-block rounded-md bg-[#b4895e]/15 px-2.5 py-1 text-xs font-medium text-[#8c6847]">
						{{ getDifficultyLabel(recipe.difficulty) }}
					</span>
					<h1 class="mt-2 text-2xl font-bold sm:text-3xl">{{ recipe.title }}</h1>
					<p class="mt-3 text-sm leading-relaxed text-gray-600">{{ recipe.description }}</p>
				</div>

				<div class="mt-6 flex flex-wrap gap-4 rounded-lg bg-[#f1f1f0] p-4 text-sm font-medium text-gray-700">
					<p><strong>Tid:</strong> {{ recipe.time }}</p>
					<p><strong>Portioner:</strong> {{ recipe.servings }}</p>
				</div>
			</div>
		</div>

		<div class="mt-8 grid grid-cols-1 gap-8 border-t border-[#deddd9] pt-8 md:grid-cols-2">
			<section>
				<h2 class="mb-4 text-lg font-bold">Ingredienser</h2>
				<p class="whitespace-pre-line text-sm leading-relaxed text-gray-700">{{ recipe.ingredients }}</p>
			</section>
			<section>
				<h2 class="mb-4 text-lg font-bold">Instruktioner</h2>
				<p v-if="recipe.instructions" class="whitespace-pre-line text-sm leading-relaxed text-gray-700">
					{{ recipe.instructions }}
				</p>
				<p v-else class="text-sm italic text-gray-500">Inga instruktioner angivna för detta recept.</p>
			</section>
		</div>
	</article>
</template>