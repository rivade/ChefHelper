import { ref } from "vue";
import { useAuth0 } from "@auth0/auth0-vue";
import type { Recipe } from "./types/recipe.ts";

export const publicRecipes = ref<Recipe[]>([]);
export const userRecipes = ref<Recipe[]>([]);

const API_URL = 'http://localhost:8001/api/recipes'
const FAVORITES_URL = 'http://localhost:8001/api/favorites'

type FavoriteInfo = {
    recipeId: string;
    userId: string;
    isFavorite: boolean;
};

export async function loadPublicRecipes(options: { silent?: boolean } = {}): Promise<boolean> {
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
        return true;
    } catch {
        if (!options.silent) alert('Kunde inte ladda in recept');
        return false;
    }
}

export function useRecipeHandler() {
    const { getAccessTokenSilently } = useAuth0();

    async function authHeaders(json = false): Promise<Record<string, string>> {
        const token = await getAccessTokenSilently();
        return {
            Authorization: `Bearer ${token}`,
            ...(json ? { 'Content-Type': 'application/json' } : {}),
        };
    }

    async function loadPrivateRecipes(): Promise<void> {
        try {
            const response = await fetch(`${API_URL}/private`, {
                headers: await authHeaders(),
            });
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
            const response = await fetch(API_URL, {
                method: 'POST',
                headers: await authHeaders(true),
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
            const response = await fetch(`${API_URL}/private`, {
                method: 'POST',
                headers: await authHeaders(true),
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

    async function updateRecipe(id: string, newRecipe: Recipe, isPrivate: boolean): Promise<boolean> {
        try {
            const recipeId = encodeURIComponent(id);
            const url = isPrivate
                ? `${API_URL}/private/${recipeId}`
                : `${API_URL}/${recipeId}`;

            // Rensa metadata om det finns innan vi skickar till backend
            const { id: _id, author: _author, isFavorite: _fav, ...payload } = newRecipe as Record<string, unknown>;

            const response = await fetch(url, {
                method: 'PATCH',
                headers: await authHeaders(true),
                body: JSON.stringify(payload)
            });

            if (!response.ok) {
                throw new Error(`Request failed: ${response.status}`);
            }

            // Uppdatera rätt reaktiv lista i frontend (exakt som vid radering)
            if (isPrivate) {
                userRecipes.value = userRecipes.value.map(recipe =>
                    recipe.id === id ? newRecipe : recipe
                );
            } else {
                publicRecipes.value = publicRecipes.value.map(recipe =>
                    recipe.id === id ? newRecipe : recipe
                );
            }

            return true;
        } catch {
            alert('Kunde inte spara ändring');
            return false;
        }
    }

    async function deleteRecipe(id: string, isPrivate: boolean): Promise<boolean> {
        try {
            const recipeId = encodeURIComponent(id);
            const url = isPrivate
                ? `${API_URL}/private/${recipeId}`
                : `${API_URL}/${recipeId}`;
            const response = await fetch(url, {
                method: 'DELETE',
                headers: await authHeaders(),
            });

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

    async function loadFavorites(): Promise<void> {
        try {
            const response = await fetch(FAVORITES_URL, {
                headers: await authHeaders(),
            });
            if (!response.ok) {
                throw new Error(`Request failed: ${response.status}`);
            }

            const favorites: unknown = await response.json();
            if (!Array.isArray(favorites)) {
                throw new Error('Unexpected favorites response');
            }

            const favoriteIds = new Set((favorites as Recipe[]).map(r => r.id));
            publicRecipes.value = publicRecipes.value.map(r => ({ ...r, isFavorite: favoriteIds.has(r.id) }));
            userRecipes.value = userRecipes.value.map(r => ({ ...r, isFavorite: favoriteIds.has(r.id) }));
        } catch {
            // User may not be authenticated yet or has no favorites; ignore silently.
        }
    }

    async function toggleFavorite(id: string): Promise<void> {
        try {
            const recipeId = encodeURIComponent(id);
            const recipe = publicRecipes.value.find(r => r.id === id) ?? userRecipes.value.find(r => r.id === id);
            const method = recipe?.isFavorite ? 'DELETE' : 'POST';

            const response = await fetch(`${FAVORITES_URL}/${recipeId}`, {
                method,
                headers: await authHeaders(),
            });
            if (!response.ok) {
                throw new Error(`Request failed: ${response.status}`);
            }

            const info = await response.json() as FavoriteInfo;
            publicRecipes.value = publicRecipes.value.map(r => r.id === id ? { ...r, isFavorite: info.isFavorite } : r);
            userRecipes.value = userRecipes.value.map(r => r.id === id ? { ...r, isFavorite: info.isFavorite } : r);
        } catch {
            alert('Kunde inte uppdatera favorit');
        }
    }

    return {
        postRecipePublic,
        postRecipePrivate,
        updateRecipe,
        deleteRecipe,
        loadPrivateRecipes,
        loadFavorites,
        toggleFavorite,
    };
}