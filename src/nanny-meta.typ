/*
 * Merged metadata for the nanny / childcare resume.
 * Import this instead of loading metadata.toml directly so that both
 * the base acting-resume metadata and the nanny-specific overrides are
 * combined in one place.
 */

#import "./utils/merge.typ": mergeDicts

#let nanny-metadata = mergeDicts(
  toml("../metadata/metadata.toml"),
  toml("../metadata/nanny-metadata.toml"),
)
