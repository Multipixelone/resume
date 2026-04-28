/*
 * Metadata loading + module include helpers used by every variant entry file.
 */

#import "./utils/merge.typ": mergeDicts

/// Merge the base metadata with an optional variant override.
/// Pass `none` or `""` for base-only.
#let makeMeta(overrideFile) = {
  let base = toml("../metadata/metadata.toml")
  if overrideFile == none or overrideFile == "" {
    base
  } else {
    mergeDicts(base, toml("../metadata/" + overrideFile))
  }
}

/// Include each `modules/<name>.typ` in order. Used for legacy include-style
/// modules (the function-style ones — experience, projects, skills — are
/// imported and called directly).
#let importModules(modules) = {
  for module in modules {
    include {
      "../modules/" + module + ".typ"
    }
  }
}
