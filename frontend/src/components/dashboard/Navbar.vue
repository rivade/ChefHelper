<script setup lang="ts">
import { ref } from "vue";

const emit = defineEmits<{
	createRecipe: [];
	backToRecipes: [];
}>();

const isMenuOpen = ref(true);
const activePage = ref("Dashboard");

function selectPage(page: string) {
	activePage.value = page;
}
</script>

<template>
	<aside
		class="sticky top-[72px] z-20 flex h-20 flex-col justify-between overflow-hidden bg-white p-3 transition-[height] duration-300 ease-in-out will-change-[height] sm:p-4 lg:h-[calc(100vh-74px)] lg:min-h-[calc(100vh-74px)] lg:overflow-visible lg:p-[30px_12px_18px]"
		:class="isMenuOpen ? 'h-[460px] sm:h-[500px]' : 'h-20'">
		<button type="button"
			class="flex h-12 w-full flex-col items-center justify-center gap-1 rounded-lg text-sm font-medium text-[#1a1a1a] transition hover:bg-[#f0efe9] lg:hidden"
			:aria-expanded="isMenuOpen" aria-controls="dashboard-navigation" @click="isMenuOpen = !isMenuOpen">
			<span>{{ activePage }}</span>
			<span class="h-px w-[150px] bg-[#1a1a1a]"></span>
		</button>

		<div id="dashboard-navigation"
			class="flex flex-1 flex-col items-center gap-3 overflow-hidden text-center transition-[max-height,opacity,transform] duration-300 ease-in-out lg:gap-0 lg:overflow-visible"
			:class="isMenuOpen ? 'max-h-[calc(100vh-130px)] translate-y-0 opacity-100 lg:max-h-none lg:opacity-100' : 'max-h-0 -translate-y-5 opacity-0 lg:max-h-none lg:translate-y-0 lg:opacity-100'">
			<button type="button"
				class="group mt-2 flex items-center justify-center gap-3 rounded-lg border-b-0 px-4 py-3 text-sm transition duration-200 hover:bg-[#f0efe9] lg:mt-0 lg:rounded-t-lg lg:rounded-b-none lg:border-b-2"
				:class="activePage === 'Hitta recept' ? 'lg:border-[#1a1a1a] text-black' : 'border-transparent text-[#6b6b6b]'"
				@click="selectPage('Hitta recept'); emit('backToRecipes')">
				<span class="text-xl text-black transition duration-200 group-hover:text-[#c08153]">
					⌕
				</span>
				<span>Hitta recept</span>
			</button>

			<nav class="flex w-full flex-1 flex-col items-center justify-evenly gap-1 lg:gap-0">
				<RouterLink to="/dashboard"
					class="group flex items-center justify-center gap-3 rounded-lg border-b-0 px-4 py-3 text-sm transition duration-200 hover:bg-[#f0efe9] hover:text-black lg:rounded-t-lg lg:rounded-b-none lg:border-b-2"
					:class="activePage === 'Favoriter' ? 'lg:border-[#1a1a1a] text-black' : 'border-transparent text-[#6b6b6b]'"
					@click="selectPage('Favoriter')">
					<span class="text-xl text-black transition duration-200 group-hover:text-[#c08153]">
						♡
					</span>
					<span>Favoriter</span>
				</RouterLink>

				<RouterLink to="/dashboard"
					class="group flex items-center justify-center gap-3 rounded-lg border-b-0 px-4 py-3 text-sm transition duration-200 hover:bg-[#f0efe9] hover:text-black lg:rounded-t-lg lg:rounded-b-none lg:border-b-2"
					:class="activePage === 'Mina recept' ? 'lg:border-[#1a1a1a] text-black' : 'border-transparent text-[#6b6b6b]'"
					@click="selectPage('Mina recept')">
					<span class="text-xl text-black transition duration-200 group-hover:text-[#c08153]">
						▤
					</span>
					<span>Mina recept</span>
				</RouterLink>

				<button
					class="group flex items-center justify-center gap-2 rounded-lg border-b-0 bg-[#e8e6e1] px-8 py-3 text-sm font-semibold transition duration-200 hover:bg-[#dcd9d2] hover:text-[#c08153] lg:gap-3 lg:rounded-t-lg lg:rounded-b-none lg:border-b-2 lg:bg-transparent lg:px-4 lg:font-normal lg:hover:bg-[#f0efe9]"
					:class="activePage === 'Skapa Recept' ? 'lg:border-[#1a1a1a] text-black' : 'border-transparent text-black'"
					type="button" @click="selectPage('Skapa Recept'); isMenuOpen = false; emit('createRecipe')">
					<span class="text-xl">＋</span>
					<span>Skapa Recept</span>
				</button>
			</nav>
		</div>

		<div class="shrink-0 items-center justify-center gap-2 pt-4 text-center lg:self-stretch lg:justify-start lg:pl-1 lg:text-left"
			:class="isMenuOpen ? 'flex' : 'hidden lg:flex'">
			<div
				class="grid h-[30px] w-[30px] shrink-0 place-items-center rounded-full bg-[#e8e4dc] text-xs font-semibold">
				T
			</div>

			<div>
				<strong class="block text-[13px] font-medium">Theo</strong>
				<small class="block text-[11px] text-[#9a9a9a]">Kock</small>
			</div>
		</div>
	</aside>
</template>