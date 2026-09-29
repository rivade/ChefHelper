import { ref } from "vue";
import { useAuth0 } from "@auth0/auth0-vue";
import type { Recipe } from "./types/recipe.ts";

export const publicRecipes = ref<Recipe[]>([]);
export const userRecipes = ref<Recipe[]>([]);
export const favoriteRecipes = ref<Recipe[]>([]);

const API_URL = 'http://localhost:8001/api/recipes'

export function useRecipeHandler() {
    const { user, isAuthenticated } = useAuth0();

    function getUserId(): string {
        const userId = user.value?.sub;
        if (!isAuthenticated.value || !userId) {
            throw new Error('User is not authenticated');
        }
        return userId;
    }

    async function postRecipePublic(recipe: Recipe) {
        try {
            const userId = encodeURIComponent(getUserId());
            const response = await fetch(`${API_URL}/${userId}`, {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json'
                },
                body: JSON.stringify(recipe)
            });

            if (!response.ok) {
                throw new Error(`Request failed: ${response.status}`);
            }

            publicRecipes.value = [...publicRecipes.value, recipe];
        } catch {
            alert('Kunde inte spara recept');
        }
    }

    async function postRecipePrivate(recipe: Recipe) {
        try {
            const userId = encodeURIComponent(getUserId());
            const response = await fetch(`${API_URL}/private/${userId}`, {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json'
                },
                body: JSON.stringify(recipe)
            });

            if (!response.ok) {
                throw new Error(`Request failed: ${response.status}`);
            }

            userRecipes.value = [...userRecipes.value, recipe];
        } catch {
            alert('Kunde inte spara recept');
        }
    }

    async function updateRecipe(id: string, newRecipe: Recipe, isPrivate: boolean) {
        try {
            const recipe = userRecipes.value.find(p => p.id === id);
            if (!recipe) return;

            const userId = encodeURIComponent(getUserId());
            const recipeId = encodeURIComponent(id);
            const url = isPrivate
                ? `${API_URL}/private/${userId}/${recipeId}`
                : `${API_URL}/${userId}/${recipeId}`;

            const response = await fetch(url, {
                method: 'PATCH',
                headers: {
                    'Content-Type': 'application/json'
                },
                body: JSON.stringify(newRecipe)
            });

            if (!response.ok) {
                throw new Error(`Request failed: ${response.status}`);
            }

            userRecipes.value = userRecipes.value.map(existing =>
                existing.id === id ? newRecipe : existing
            );
        } catch {
            alert('Kunde inte spara ändring');
        }
    }

    return { postRecipePublic, postRecipePrivate, updateRecipe };
}