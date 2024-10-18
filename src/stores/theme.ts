import { writable, type Writable } from "svelte/store";

type Theme = {
  text_color: string;
  background_color: string;
  primary_color: string;
  secondary_color: string;
  accent_color: string;
  grey_text: string;
};

export const _theme: Theme = {
  text_color: "#000000",
  background_color: "#fbede9",
  primary_color: "#da3029",
  secondary_color: "#FDDDD7",
  accent_color: "#000000",
  grey_text: "rgba(125,122,125,100%)",
};

export const theme: Writable<Theme> = writable(_theme);
