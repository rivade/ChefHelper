<script setup lang="ts">
import { computed, onMounted, onUnmounted, ref } from "vue";
import { useAuth0 } from "@auth0/auth0-vue";

const { user, logout } = useAuth0();
const isOpen = ref(false);
const menuRef = ref<HTMLElement | null>(null);

const username = computed(
	() => user.value?.nickname || user.value?.name || user.value?.email || "Användare",
);

function closeOnOutsideClick(event: MouseEvent) {
	if (menuRef.value && !menuRef.value.contains(event.target as Node)) {
		isOpen.value = false;
	}
}

function closeOnEscape(event: KeyboardEvent) {
	if (event.key === "Escape") isOpen.value = false;
}

function signOut() {
	void logout({ logoutParams: { returnTo: `${window.location.origin}/` } });
}

onMounted(() => {
	document.addEventListener("click", closeOnOutsideClick);
	document.addEventListener("keydown", closeOnEscape);
});

onUnmounted(() => {
	document.removeEventListener("click", closeOnOutsideClick);
	document.removeEventListener("keydown", closeOnEscape);
});
</script>

<template>
	<div ref="menuRef" class="relative shrink-0 pt-4 lg:self-stretch lg:pl-1">
		<button
			type="button"
			class="flex min-h-12 w-full items-center justify-center gap-2 rounded-lg px-2 text-center transition hover:bg-[#f0efe9] focus-visible:outline-2 focus-visible:outline-offset-2 focus-visible:outline-[#c08153] lg:justify-start lg:text-left"
			:aria-expanded="isOpen"
			aria-haspopup="menu"
			@click="isOpen = !isOpen"
		>
			<span class="min-w-0">
				<strong class="block truncate text-[15px] font-medium leading-5">{{ username }}</strong>
				<small class="block text-[13px] font-medium leading-5 text-[#5f5a54]">Kock</small>
			</span>
		</button>

		<div
			v-if="isOpen"
			class="absolute bottom-full left-1/2 z-50 mb-2 w-48 -translate-x-1/2 rounded-lg border border-[#e8e4dc] bg-white p-1.5 shadow-lg lg:left-0 lg:translate-x-0"
			role="menu"
		>
			<button
				type="button"
				class="w-full rounded-md bg-[#c62828] px-3 py-2.5 text-left text-base font-medium text-white transition hover:bg-[#a61b1b] focus-visible:outline-2 focus-visible:outline-offset-2 focus-visible:outline-[#c62828]"
				role="menuitem"
				@click="signOut"
			>
				Logga ut
			</button>
		</div>
	</div>
</template>