/// Build date from sys.inputs.version (set by Nix as YYYY-MM-DD), or today.
#let buildDate() = {
  let version = sys.inputs.at("version", default: none)
  if version != none and version != "" {
    let parts = version.split("-")
    datetime(
      year: int(parts.at(0)),
      month: int(parts.at(1)),
      day: int(parts.at(2)),
    )
  } else {
    datetime.today()
  }
}
