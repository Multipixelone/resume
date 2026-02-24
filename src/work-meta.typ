/*
 * Merged metadata for the work resume.
 * Import this instead of loading metadata.toml directly so that both
 * the base acting-resume metadata and the work-specific overrides are
 * combined in one place.
 */

#import "./utils/merge.typ": mergeDicts

#let work-metadata = mergeDicts(
  toml("../metadata/metadata.toml"),
  toml("../metadata/work-metadata.toml"),
)
