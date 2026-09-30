import { ref } from "vue";
import { useAuth0 } from "@auth0/auth0-vue";
import type { Recipe } from "./types/recipe.ts";

export const publicRecipes = ref<Recipe[]>([]);
export const userRecipes = ref<Recipe[]>([]);

const API_URL = 'http://localhost:8001/api/recipes'

export async function loadPublicRecipes() {
    try {
        const response = await fetch(API_URL);
        if (!response.ok) {
            throw new Error(`Request failed: ${response.status}`);
        }

        const recipes: unknown = await response.json();
        if (!Array.isArray(recipes)) {
            throw new Error('Unexpected recipes response');
        }

        publicRecipes.value = recipes as Recipe[];
    } catch (error) {
        alert('Kunde inte ladda in recept');
    }
}

export function useRecipeHandler() {
    const { user, isAuthenticated } = useAuth0();

    function getUserId(): string {
        const userId = user.value?.sub;
        if (!isAuthenticated.value || !userId) {
            throw new Error('User is not authenticated');
        }
        return userId;
    }

    async function loadPrivateRecipes(): Promise<void> {
        try {
            const userId = encodeURIComponent(getUserId());
            const response = await fetch(`${API_URL}/private/${userId}`);
            if (!response.ok) {
                throw new Error(`Request failed: ${response.status}`);
            }

            const recipes: unknown = await response.json();
            if (!Array.isArray(recipes)) {
                throw new Error('Unexpected recipes response');
            }

            userRecipes.value = recipes as Recipe[];
        } catch {
            alert('Kunde inte ladda in dina recept');
        }
    }

    async function postRecipePublic(
        recipe: Omit<Recipe, "id" | "author">
    ): Promise<Recipe | null> {
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

            const savedRecipe = await response.json() as Recipe;
            publicRecipes.value = [...publicRecipes.value, savedRecipe];
            return savedRecipe;
        } catch {
            alert('Kunde inte spara recept');
            return null;
        }
    }

    async function postRecipePrivate(
        recipe: Omit<Recipe, "id" | "author">
    ): Promise<Recipe | null> {
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

            const savedRecipe = await response.json() as Recipe;
            userRecipes.value = [...userRecipes.value, savedRecipe];
            return savedRecipe;
        } catch {
            alert('Kunde inte spara recept');
            return null;
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

    async function deleteRecipe(id: string, isPrivate: boolean): Promise<boolean> {
        try {
            const recipeId = encodeURIComponent(id);
            const url = isPrivate
                ? `${API_URL}/private/${encodeURIComponent(getUserId())}/${recipeId}`
                : `${API_URL}/${recipeId}`;
            const response = await fetch(url, { method: 'DELETE' });

            if (!response.ok) {
                throw new Error(`Request failed: ${response.status}`);
            }

            if (isPrivate) {
                userRecipes.value = userRecipes.value.filter(recipe => recipe.id !== id);
            } else {
                publicRecipes.value = publicRecipes.value.filter(recipe => recipe.id !== id);
            }

            return true;
        } catch {
            alert('Kunde inte radera recept');
            return false;
        }
    }

    return { postRecipePublic, postRecipePrivate, updateRecipe, deleteRecipe, loadPrivateRecipes, getUserId };
}