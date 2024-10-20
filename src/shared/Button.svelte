<script lang="ts">
    import { theme } from "../stores/theme";
    import { onMount } from 'svelte';

    export let inverse: boolean = false;
    export let fontSize: number = 20;

    let button: HTMLButtonElement;
    let x = 0;
    let y = 0;

    // Add variables for gradient colors
    // you can change the alpha channels to play around with the gradient
    $: gradientStart = inverse ? `rgba(218,48,41,0.8)` : `rgba(253,221,215,0.8)`; // primary and secondary in rgba with different alpha channel
    $: gradientEnd = inverse ? `rgba(253,221,215,0.1)` : `rgba(218,48,41,0.1)`; // secondary and primary in rgba with different alpha channel

    onMount(() => {
        button.addEventListener('mousemove', handleMouseMove);
    });

    function handleMouseMove(e: MouseEvent) {
        const rect = button.getBoundingClientRect();
        x = e.clientX - rect.left;
        y = e.clientY - rect.top;
    }
</script>

<button
    bind:this={button}
    on:click
    on:mouseover={() => inverse = !inverse}
    on:mouseout={() => inverse = !inverse}
    on:blur
    on:focus
    class:inverse
    style="--primary_color: {$theme.primary_color};
           --text_color:{$theme.text_color};
           --secondary_color:{$theme.secondary_color};
           --font_size:{fontSize}px;
           --grey:{$theme.grey_text};
           --x:{x}px;
           --y:{y}px;
           --gradient-start: {gradientStart};
           --gradient-end: {gradientEnd};"
>
    <slot></slot>
</button>

<style>
    button {
        position: relative;
        font-family: "Roboto Mono", monospace;
        font-size: var(--font_size);
        font-weight: bold;
        background-color: var(--primary_color);
        color: var(--secondary_color);
        text-wrap: nowrap;
        padding: 13px 26px;
        border: black solid 1px;
        border-radius: 16px;
        cursor: pointer;
        overflow: hidden;
    }

    button::before {
        content: '';
        position: absolute;
        /* you can change the percents to play around with the gradient*/
        background: radial-gradient(circle, var(--gradient-start) 0%, var(--gradient-end) 70%);
        transform: translate(-50%, -50%);
        transition: width 0.5s, height 0.5s opacity 0.5s;;
        left: var(--x);
        top: var(--y);
        pointer-events: none;
    }

    button:hover::before {
        /* size of circle */
        /* you can change the size to play around with the gradient*/
        width: 100px;
        height: 100px;
    }

    .inverse {
        border: var(--primary_color) solid 1px;
        background-color: var(--secondary_color);
        color: var(--primary_color);
    }

    button:hover {
        box-shadow: var(--grey) 3px 3px 10px;
    }
</style>