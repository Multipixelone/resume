/*
 * Generic metadata merger.
 * Import this and call makeMeta("override-file.toml") to produce
 * a metadata dictionary that layers variant-specific overrides on
 * top of the base metadata.toml.
 */

#import "./utils/merge.typ": mergeDicts

#let makeMeta(overrideFile) = mergeDicts(
  toml("../metadata/metadata.toml"),
  toml("../metadata/" + overrideFile),
)
