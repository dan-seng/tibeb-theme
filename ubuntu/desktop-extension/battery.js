// Pure rendering logic, shared with the threshold tests.
export function batterySvg(percentage, charging) {
    const level = Math.max(0, Math.min(100, Number(percentage) || 0));
    const height = 15 * level / 100;
    const fill = level < 15 ? '#df675b' : '#d5ac42';
    return `<svg xmlns="http://www.w3.org/2000/svg" width="24" height="24" viewBox="0 0 24 24">
      <defs><clipPath id="cup"><path d="M5 5h14l-2 13q-.3 2-3 2h-4q-2.7 0-3-2z"/></clipPath></defs>
      <rect x="5" y="${20-height}" width="14" height="${height}" fill="${fill}" clip-path="url(#cup)"/>
      <path d="M3 3h18l-3 16q-.5 3-4 3h-4q-3.5 0-4-3z" fill="none" stroke="#eee5cb" stroke-width="1.7"/>
      ${charging ? '<path d="m14 5-7 8h5l-2 7 8-10h-5z" fill="#fff4d4" stroke="#141a1a" stroke-width="1"/>' : ''}
    </svg>`;
}
