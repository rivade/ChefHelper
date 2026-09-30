<script setup lang="ts">
import { useAuth0 } from "@auth0/auth0-vue";

const { loginWithRedirect } = useAuth0();

function signUp() {
	void loginWithRedirect({
		authorizationParams: { screen_hint: "signup" },
		appState: { target: "/dashboard" },
	});
}

function logIn() {
	void loginWithRedirect({ appState: { target: "/dashboard" } });
}
</script>

<template>
	<aside class="flex flex-col gap-4 rounded-lg border border-[#ded2c4] bg-[#eee7dd] p-4 sm:flex-row sm:items-center sm:justify-between sm:px-5">
		<p class="text-sm leading-6 text-[#39332d] sm:text-base">
			För fler funktioner, skapa ett konto eller logga in.
		</p>
		<div class="flex shrink-0 flex-wrap gap-2">
			<button
				type="button"
				class="rounded-lg bg-[#b4895e] px-4 py-2.5 text-sm font-semibold text-white transition hover:bg-[#9b744c] focus-visible:outline-2 focus-visible:outline-offset-2 focus-visible:outline-[#8c6847]"
				@click="signUp"
			>
				Skapa konto
			</button>
			<button
				type="button"
				class="rounded-lg border border-[#b9aa98] bg-white px-4 py-2.5 text-sm font-semibold text-[#292622] transition hover:bg-[#f8f6f2] focus-visible:outline-2 focus-visible:outline-offset-2 focus-visible:outline-[#8c6847]"
				@click="logIn"
			>
				Logga in
			</button>
		</div>
	</aside>
</template>