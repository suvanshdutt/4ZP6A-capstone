import { writable, type Writable } from "svelte/store";

type Theme = {
  text_color: string;
  background_color: string;
  primary_color: string;
  secondary_color: string;
  accent_color: string;
  grey_text: string;
  heading_text: string;
};

export const light_theme: Theme = {
  text_color: "rgba(24, 23, 24, 0.8)",
  background_color: "#fbede9",
  primary_color: "#da3029", // da1111
  secondary_color: "#FDDDD7",
  accent_color: "#000000",
  grey_text: "rgba(125,122,125,100%)",
  heading_text: "#1e1e1e",
};

export const dark_theme: Theme = {
  text_color: "#ffffff",
  background_color: "#1e1e1e",
  primary_color: "#da3029",
  secondary_color: "#333333",
  accent_color: "#ffffff",
  grey_text: "rgba(200, 200, 200, 1)",
  heading_text: "#ffffff",
};


export const theme: Writable<Theme> = writable(light_theme);
