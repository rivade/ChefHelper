<script setup lang="ts">
import { computed, ref } from "vue";

const emit = defineEmits<{
	cancel: [];
	saved: [recipe: RecipePayload];
}>();

type RecipePayload = {
	author: string;
	title: string;
	description: string;
	ingredients: string;
	instructions: string;
	cookingtime: [number, number];
	portions: number;
	difficulty: number;
};

const author = ref("");
const title = ref("");
const description = ref("");
const cookingHours = ref("Timar");
const cookingMinutes = ref("Minuter");
const portions = ref("Portioner");
const difficulty = ref(1);
const ingredients = ref("");
const instructions = ref("");
const submitted = ref(false);

const numericValues = computed(() => ({
	cookingHours: Number(cookingHours.value),
	cookingMinutes: Number(cookingMinutes.value),
	portions: Number(portions.value),
}));

const errors = computed(() => ({
	author: author.value.trim() ? "" : "Författare krävs.",
	title: title.value.trim() ? "" : "Namn krävs.",
	description: description.value.trim() ? "" : "Beskrivning krävs.",
	ingredients: ingredients.value.trim() ? "" : "Ingredienser krävs.",
	instructions: instructions.value.trim() ? "" : "Instruktioner krävs.",
	cookingtime:
		!Number.isInteger(numericValues.value.cookingHours) ||
		numericValues.value.cookingHours < 0 ||
		numericValues.value.cookingHours > 72
			? "Timmar måste vara mellan 0 och 72."
			: !Number.isInteger(numericValues.value.cookingMinutes) ||
				numericValues.value.cookingMinutes < 0 ||
				numericValues.value.cookingMinutes > 59
				? "Minuter måste vara mellan 0 och 59."
				: "",
	portions: numericValues.value.portions > 0 ? "" : "Portioner måste vara större än 0.",
	difficulty:
		difficulty.value >= 1 && difficulty.value <= 5
			? ""
			: "Svårighetsgrad måste vara mellan 1 och 5.",
}));

const canSave = computed(() =>
	Object.values(errors.value).every((error) => !error),
);

function saveRecipe() {
	submitted.value = true;

	if (!canSave.value) return;

	emit("saved", {
		author: author.value.trim(),
		title: title.value.trim(),
		description: description.value.trim(),
		ingredients: ingredients.value.trim(),
		instructions: instructions.value.trim(),
		cookingtime: [numericValues.value.cookingHours, numericValues.value.cookingMinutes],
		portions: numericValues.value.portions,
		difficulty: difficulty.value,
	});
}

function cancel() {
	emit("cancel");
}
</script>

<template>
	<main class="bg-[#f1f1f0] font-['Roboto'] text-[#1a1a1a]">
		<form class="mx-auto max-w-[1272px] px-3 py-3 sm:px-6 sm:py-5 lg:px-3" @submit.prevent="saveRecipe">
			<div class="mb-4 flex items-center justify-between border-b border-[#deddd9] pb-3 lg:mb-5">
				<h1 class="text-2xl font-bold sm:text-3xl">Skapa recept</h1>
			</div>

			<div class="grid gap-5 lg:grid-cols-3 lg:gap-10">
				<section class="space-y-6">
					<label class="block">
						<span class="form-title"><b>1</b> Namn</span>
						<input v-model="title" class="form-control" placeholder="Ge ditt recept ett namn!" required />
					</label>

					

					<label class="block">
						<span class="form-title"><b>2</b> Beskrivning</span>
						<textarea v-model="description" class="form-control min-h-[140px] resize-none overflow-y-auto lg:h-[150px]" placeholder="Skriv en kort beskrivning om vad det är för recept..." required></textarea>
					</label>

					<div class="pt-1">
						<span class="form-title"><b>3</b> Tid och portioner</span>
						<div class="grid grid-cols-2 gap-3">
							<input v-model="cookingHours" class="form-control" type="number" min="0" max="72" placeholder="Timmar" />
							<input v-model="cookingMinutes" class="form-control" type="number" min="0" max="59" placeholder="Minuter" />
						</div>
						<input v-model="portions" class="form-control mt-3" type="number" min="1" placeholder="Portioner" />
						<p v-if="submitted && errors.cookingtime" class="field-error">{{ errors.cookingtime }}</p>
						<p v-if="submitted && errors.portions" class="field-error">{{ errors.portions }}</p>
					</div>
				</section>

				<section class="space-y-6">
					<label class="block">
						<span class="form-title"><b>4</b> Svårighetsgrad</span>
						<select v-model.number="difficulty" class="form-control cursor-pointer">
							<option :value="1">1 - Lätt</option>
							<option :value="2">2</option>
							<option :value="3">3 - Medel</option>
							<option :value="4">4</option>
							<option :value="5">5 - Komplex</option>
						</select>
					</label>

					<label class="block">
						<span class="form-title"><b>5</b> Ingredienser</span>
						<textarea v-model="ingredients" class="form-control min-h-[260px] resize-none overflow-y-auto lg:h-[331px]" placeholder="Lista vilka ingredienser som behövs för ditt recept, exempelvis:&#10;&#10;• Ris&#10;• Nötfärs&#10;• Paprika&#10;&#10;etc..." required></textarea>
					</label>
				</section>

				<section class="flex flex-col pt-2">
					<label class="block">
						<span class="form-title"><b>6</b> Steg för steg</span>
						<textarea v-model="instructions" class="form-control min-h-[300px] resize-none overflow-y-auto lg:h-[380px]" placeholder="Gå igenom steg för steg hur förberedelse och tillagning går till i receptet, exempelvis:&#10;&#10;1. Skölj riset tills vattnet blir klart&#10;2. Skär paprikan i tunna strimlor&#10;3. Börja bryn köttfärsen i en het panna&#10;&#10;etc..." required></textarea>
					</label>

					<p v-if="submitted && !canSave" class="mt-3 text-sm text-red-700">
						Fyll i alla obligatoriska fält innan receptet sparas.
					</p>

					<div class="mt-4 flex flex-col-reverse gap-3 sm:flex-row sm:justify-end">
						<button type="button" class="secondary-button" @click="cancel">Avbryt</button>
						<button type="submit" class="primary-button">Spara recept</button>
					</div>
				</section>
			</div>
		</form>
	</main>
</template>

<style scoped>
.form-title {
	display: flex;
	align-items: center;
	gap: 10px;
	margin-bottom: 16px;
	font-size: 21px;
	font-weight: 600;
}

.form-title b {
	display: grid;
	width: 28px;
	height: 28px;
	place-items: center;
	border-radius: 8px;
	background: #b4895e;
	color: white;
	font-size: 16px;
}

.form-control {
	display: block;
	width: 100%;
	border: 0;
	border-radius: 9px;
	background: #dededc;
	padding: 12px 14px;
	color: #1a1a1a;
	font: inherit;
	font-size: 14px;
	outline: 0;
	transition: box-shadow 0.2s ease, background 0.2s ease;
}

.form-control::placeholder {
	color: #888782;
}

.form-control:focus {
	background: #e5e4e1;
	box-shadow: 0 0 0 3px #b4895e66;
}

.field-error {
	margin-top: 6px;
	color: #b42318;
	font-size: 12px;
}

.secondary-button,
.primary-button {
	min-height: 42px;
	border-radius: 9px;
	padding: 0 24px;
	font: inherit;
	font-size: 14px;
	font-weight: 600;
	cursor: pointer;
	transition: transform 0.2s ease, background 0.2s ease;
}

.secondary-button {
	border: 1px solid #d0cfcc;
	background: transparent;
	color: #6b6b6b;
}

.primary-button {
	border: 0;
	background: #b89a72;
	color: white;
}

.secondary-button:hover,
.primary-button:hover {
	transform: translateY(-2px);
}

.primary-button:hover {
	background: #a7875f;
}

@media (max-width: 639px) {
	.form-title {
		font-size: 15px;
	}

	.form-title b {
		width: 22px;
		height: 22px;
		border-radius: 6px;
		font-size: 12px;
	}

	.form-control {
		font-size: 11px;
	}
}
</style>
