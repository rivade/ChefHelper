export type Recipe = {
    id: string;
    title: string;
    description: string;
    image: string;
    imagePosition?: string;
    difficulty: number | string;
    time: string;
    servings: string;
    ingredients: string;
    instructions?: string;
    isUserCreated?: boolean;
    isFavorite?: boolean;
};