import { writable } from "svelte/store";

type Theme = {
    text_color: string;
    background_color: string;
    primary_color: string;
    secondary_color: string;
    accent_color: string;
};

export const _theme: Theme = {
    text_color: "#000000",
    background_color: "#fbede9",
    primary_color: "#da3029",
    secondary_color: "#e9766e",
    accent_color: "#000000",
};

export const theme: Writable<Theme> = writable(_theme);
