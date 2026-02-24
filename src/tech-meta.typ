/*
 * Merged metadata for the tech resume.
 * Import this instead of loading metadata.toml directly so that both
 * the base resume metadata and the tech-specific overrides are
 * combined in one place.
 */

#import "./utils/merge.typ": mergeDicts

#let tech-metadata = mergeDicts(
  toml("../metadata/metadata.toml"),
  toml("../metadata/tech-metadata.toml"),
)
