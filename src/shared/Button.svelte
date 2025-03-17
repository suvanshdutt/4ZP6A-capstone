<script lang="ts">
    import { theme } from "../stores/theme";

    // Parameters possible to pass
    export let inverse: boolean = false;
    export let fontSize: number = 20;
</script>


<button on:click
        on:mouseover={() => inverse = !inverse}
        on:mouseout={() => inverse = !inverse}
        on:blur
        on:focus
        class:inverse = {inverse}
        style="--primary_color: {$theme.primary_color};
               --text_color:{$theme.text_color};
               --secondary_color:{$theme.secondary_color};
               --font_size:{fontSize}px;
               --grey:{$theme.grey_text};"
        {...$$restProps}
        >
    <slot></slot>
</button>

<style>
    button{
        /* Fonts */
        font-family: "Roboto Mono", monospace;
        font-size: var(--font_size);
        font-weight: bold;
        /* Colors */
        background-color: var(--primary_color);
        color: white; /* This needs to be white hardcoded. Other options need to be discussed */
        /* Layout */
        text-wrap: nowrap;
        padding: 13px 26px;
        border: black solid 1px;
        border-radius: 16px;
        transition: 0.4s;
        cursor: pointer;
    }
    .inverse{
        border: var(--primary_color) solid 1px;
        background-color: var(--secondary_color);
        color: var(--primary_color);
    }
    button:hover {
        box-shadow: 7px 5px 56px -14px var(--primary_color);
    }
    button:active {
        transform: scale(0.90);
        box-shadow: 7px 5px 56px -10px var(--primary_color);
    }
</style>