import plan from 'virtual:media-renditions';
import { sitePath } from '$lib/paths';

/** Site path of one width: the copies live at /media/w<width>/ (routes/media), the master at its own path. */
const renditionPath = (file: string, width: number, widths: number[]) =>
  width === widths.at(-1) ? `/media/${file}` : `/media/w${width}/${file}`;

/** `src`, `srcset` and `sizes` for a static/media master, so the browser fetches the copy its slot needs. */
export function responsive(file: string, sizes: string) {
  const widths = plan[file];
  if (!widths) throw new TypeError(`No master in static/media: ${file}`);
  const srcset = widths.map(width => `${sitePath(renditionPath(file, width, widths))} ${width}w`).join(', ');
  return { srcset, sizes, src: sitePath(`/media/${file}`) };
}

// Keep these slot equations in sync with site.css. Account for grid gaps and mats,
// not transformed bounding boxes (rotation does not change the image resolution).
const PHONE = '(max-width: 39.99em)';
const shell = 'min(100vw - 8rem, 75rem)';
const slots = (phone: string, tablet: string, desktop: string, large = desktop) => [
  `${PHONE} ${phone}`,
  `(max-width: 59.99em) ${tablet}`,
  `(max-width: 79.99em) ${desktop}`,
  large
].join(', ');
const spread = (span: number, fraction: number, mat = 0, overhang = false) => {
  const board = (width: string, gap: number, extra: number) =>
    `calc((${width} - ${11 * gap}rem) * ${span / 12} + ${(span - 1) * gap + extra - mat}rem)`;
  return slots(`calc((100vw - 3rem) * ${fraction} - ${mat}rem)`,
    board('100vw - 5rem', 1.5, overhang ? 1.25 : 0),
    board('100vw - 5rem', 2, overhang ? 2.75 : 0),
    board(shell, 2, overhang ? 2.75 : 0));
};
export const spreadSizes: Record<string, string> = {
  wide: spread(8, 1),
  tall: spread(4, .72, 1, true),
  small: spread(5, .88, .8),
  'wide-right': spread(6, 1),
  'tall-left': spread(4, .72, 1),
  'small-right': spread(4, .85, 1),
  'tall-bottom': spread(4, .72, 1)
};

/** Headshot or the smaller print attached to it; each has its own mat. */
export const portraitSizes = (phone = 1, board = 1) => {
  const mat = board === 1 ? .9 : .8 + .9 * board;
  const phoneMat = board === 1 ? .9 : .8 + .9 * phone;
  return slots(`calc(min((100vw - 2.5rem) * .73, 22rem) * ${phone} - ${phoneMat}rem)`,
    `calc(((100vw - 7rem) / 2.1 - 1rem) * ${board} - ${mat}rem)`,
    `calc(min((100vw - 9rem) / 2.13 - 2rem, 28rem) * ${board} - ${mat}rem)`,
    `calc(min((${shell} - 4rem) / 2.13 - 2rem, 28rem) * ${board} - ${mat}rem)`);
};

/** Show-page prints also respect the source width cap on .photo-layers. */
export function reelSizes(portrait: boolean, solo: boolean, sourceWidth: number) {
  const board = (width: string, phone = false) => {
    const available = solo ? `min(${width}, 44rem)` : phone ? width : `(${width} - clamp(2rem, 6vw, 5rem)) / 2`;
    return `calc(min((${available}) * ${portrait ? (phone ? .78 : .8) : 1}, ${sourceWidth}px) - 1rem)`;
  };
  return slots(board('100vw - 2.5rem', true), board('100vw - 5rem'), board('100vw - 5rem'), board(shell));
}

export const coverSizes = (width: number, height: number) => `${4.25 * width / height}rem`;

export const offstageSizes = [
  `${PHONE} calc((100vw - 2.5rem) * .85 - 1rem)`,
  '(max-width: 47.99em) calc((100vw - 5rem) * .85 - 1rem)',
  '(max-width: 79.99em) calc((100vw - 5rem - clamp(2rem, 5vw, 4.5rem)) * 5 / 12 - 1rem)',
  `calc((${shell} - clamp(2rem, 5vw, 4.5rem)) * 5 / 12 - 1rem)`
].join(', ');
