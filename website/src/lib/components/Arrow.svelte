<script lang="ts">
  // The one link arrow. Text glyphs (↗ ↓ ↙) took each link's font, size and weight,
  // so no two matched; this is a single path at a fixed size (see .arrow in site.css),
  // rotated inside the SVG so CSS transforms stay free for hover motion.
  // The direction says where the link goes: next (→) stays on the site, out (↗) leaves it,
  // down (↓) saves a file or jumps down the page, back (←) returns.
  type Direction = 'next' | 'out' | 'down' | 'back';
  let { dir = 'next' }: { dir?: Direction } = $props();
  const turn: Record<Direction, number> = { next: 45, out: 0, down: 135, back: 225 };
</script>

<svg class="icon arrow" data-dir={dir} viewBox="0 0 24 24" aria-hidden="true" focusable="false"><path transform={`rotate(${turn[dir]} 12 12)`} d="M6 18 18 6M8 6h10v10"/></svg>
