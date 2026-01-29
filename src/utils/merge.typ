/*
* Utility functions for merging dictionaries
*/

/// Recursively merge two dictionaries
/// Values from `override` will take precedence over values in `base`
/// Nested dictionaries are merged recursively rather than replaced entirely
///
/// - base: The base dictionary to start with
/// - override: The dictionary containing override values
/// - returns: A new dictionary with merged values
#let mergeDicts(base, override) = {
  let result = base
  for (key, value) in override {
    if key in result and type(result.at(key)) == "dictionary" and type(value) == "dictionary" {
      // Recursively merge nested dictionaries
      result.insert(key, mergeDicts(result.at(key), value))
    } else {
      // Override base value with new value
      result.insert(key, value)
    }
  }
  result
}
