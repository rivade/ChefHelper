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
    author: string;
    instructions?: string;
    isFavorite?: boolean;
};