import theatreSource from '$canonical/theatre.toml?raw';
import variantSource from '../../../../variants.toml?raw';
import { portfolioContent } from '$content';

// Module-level ingestion: parse and normalize once, not per page or browser tick.
// Vite tracks canonical raw imports; no duplicated production JSON/Markdown.
export const content = portfolioContent(theatreSource, variantSource);
