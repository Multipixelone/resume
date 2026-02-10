/*
* Functions for the CV template
*/

#import "@preview/fontawesome:0.6.0": *
#import "./utils/styles.typ": latinFontList, latinHeaderFont, awesomeColors, regularColors, setAccentColor, hBar
#import "./utils/lang.typ": isNonLatin

/// Insert the header section of the CV.
///
/// - metadata (array): the metadata read from the TOML file.
/// - headerFont (array): the font of the header.
/// - regularColors (array): the regular colors of the CV.
/// - awesomeColors (array): the awesome colors of the CV.
/// -> content
#let _cvHeader(
  metadata,
  profilePhoto,
  headerFont,
  regularColors,
  awesomeColors,
) = {
  // Parameters
  let hasPhoto = metadata.layout.header.display_profile_photo
  let align = eval(metadata.layout.header.header_align)
  let personalInfo = metadata.personal.info
  let firstName = metadata.personal.first_name
  let lastName = metadata.personal.last_name
  let pronouns = metadata.personal.pronouns
  let headerQuote = metadata.lang.at(metadata.language).header_quote
  let displayProfilePhoto = metadata.layout.header.display_profile_photo
  // let profilePhoto = metadata.layout.header.profile_photo_path
  let accentColor = setAccentColor(awesomeColors, metadata)
  let nonLatinName = ""
  let nonLatin = isNonLatin(metadata.language)
  if nonLatin {
    nonLatinName = metadata.lang.non_latin.name
  }

  // Styles
  let headerFirstNameStyle(str) = {
    text(
      font: headerFont,
      size: 32pt,
      fill: regularColors.darkgray,
      str,
    )
  }
  let headerLastNameStyle(str) = {
    text(font: headerFont, size: 32pt, str)
  }
  let headerPronounStyle(str) = {
    text(size: 14pt, fill: accentColor, str)
  }
  let headerInfoStyle(str) = {
    text(size: 10pt, fill: accentColor, str)
  }
  let headerQuoteStyle(str) = {
    text(size: 10pt, weight: "medium", style: "italic", fill: accentColor, str)
  }

  // Components
  let makeHeaderInfo() = {
    let personalInfoIcons = (
      phone: fa-phone(solid: true),
      email: fa-envelope(solid: true),
      linkedin: fa-linkedin(solid: true),
      homepage: fa-house-laptop(solid: true),
      github: fa-square-github(solid: true),
      gitlab: fa-gitlab(solid: true),
      orcid: fa-orcid(solid: true),
      researchgate: fa-researchgate(solid: true),
      location: fa-location-dot(solid: true),
      height: fa-ruler(solid: true),
      eyes: fa-eye(solid: true),
      hair: fa-location-dot(solid: true),
      vocal-part: fa-microphone(solid: true),
      union: fa-landmark(solid: true),
      extraInfo: "",
    )
    let n = 1
    for (k, v) in personalInfo {
      // A dirty trick to add linebreaks with "linebreak" as key in personalInfo
      if k == "linebreak" {
        n = 0
        linebreak()
        continue
      }
      if k.contains("custom") {
        let img = v.at("image", default: "")
        let awesomeIcon = v.at("awesomeIcon", default: "")
        let text = v.at("text", default: "")
        let link_value = v.at("link", default: "")
        let iconStyle = v.at("style", default: "solid")
        let icon = ""
        if img != "" {
          icon = img.with(width: 10pt)
        } else {
          icon = fa-icon(awesomeIcon, style: iconStyle)
        }
        box({
          icon
          h(5pt)
          link(link_value)[#text]
        })
      } else if v != "" {
        box({
          // Adds icons
          personalInfoIcons.at(k)
          h(5pt)
          // Adds hyperlinks
          if k == "email" {
            link("mailto:" + v)[#v]
          } else if k == "linkedin" {
            link("https://www.linkedin.com/in/" + v)[#v]
          } else if k == "github" {
            link("https://github.com/" + v)[#v]
          } else if k == "gitlab" {
            link("https://gitlab.com/" + v)[#v]
          } else if k == "homepage" {
            link("https://" + v)[#v]
          } else if k == "orcid" {
            link("https://orcid.org/" + v)[#v]
          } else if k == "researchgate" {
            link("https://www.researchgate.net/profile/" + v)[#v]
          } else {
            v
          }
        })
      }
      // Adds hBar
      if n != personalInfo.len() {
        hBar()
      }
      n = n + 1
    }
  }

  let makeHeaderNameSection() = table(
    columns: 1fr,
    inset: 0pt,
    stroke: none,
    row-gutter: 6mm,
    if nonLatin {
      headerFirstNameStyle(nonLatinName)
    } else [#headerFirstNameStyle(firstName) #h(5pt) #headerLastNameStyle(lastName) #h(5pt) #headerPronounStyle(pronouns)],
    [#headerInfoStyle(makeHeaderInfo())],
    [#headerQuoteStyle(headerQuote)],
  )

  let makeHeaderPhotoSection() = {
    set image(height: 2.2cm)
    if displayProfilePhoto {
      // box(profilePhoto, radius: 50%, clip: true)
      figure(
        profilePhoto,
        caption: [_Artistic Website_],
        gap: 0em,
        supplement: none,
      )
    } else {
      v(2.2cm)
    }
  }

  let makeHeader(leftComp, rightComp, columns, align) = table(
    columns: columns,
    inset: 0pt,
    stroke: none,
    column-gutter: 15pt,
    align: align + horizon,
    {
      leftComp
    },
    {
      rightComp
    },
  )

  if hasPhoto {
    makeHeader(
      makeHeaderNameSection(),
      makeHeaderPhotoSection(),
      (auto, 12%),
      align,
    )
  } else {
    makeHeader(
      makeHeaderNameSection(),
      makeHeaderPhotoSection(),
      (auto, 0%),
      align,
    )
  }
}

/// Insert the footer section of the CV.
///
/// - metadata (array): the metadata read from the TOML file.
/// -> content
#let _cvFooter(metadata) = {
  // Parameters
  let firstName = metadata.personal.first_name
  let lastName = metadata.personal.last_name
  let footerText = metadata.lang.at(metadata.language).cv_footer
  let commit = sys.inputs.at("commit", default: "unknown")
  let version = sys.inputs.at("version", default: none)
  let date = if version != none {
  let parts = version.split("-")
  datetime(year: int(parts.at(0)), month: int(parts.at(1)), day: int(parts.at(2)))
  } else {
    datetime.today()
  }
  let buildDate = date.display("[month repr:short] [day], [year]")

  // Styles
  let footerStyle(str) = {
    text(size: 8pt, fill: rgb("#999999"), smallcaps(str))
  }
  let commitStyle(str) = {
    text(size: 6pt, fill: rgb("#CCCCCC"), family: "IBM Plex Mono", str)
  }

  return table(
    columns: (1fr, auto),
    inset: -5pt,
    stroke: none,
    footerStyle([#firstName #lastName #footerText]),
    [#footerStyle([Last Updated #buildDate ·]) #h(3pt) #commitStyle([#commit])],
  )

}

/// Add the title of a section.
///
/// NOTE: If the language is non-Latin, the title highlight will not be sliced.
///
/// - title (str): The title of the section.
/// - highlighted (bool): Whether the first n letters will be highlighted in accent color.
/// - letters (int): The number of first letters of the title to highlight.
/// - metadata (array): (optional) the metadata read from the TOML file.
/// - awesomeColors (array): (optional) the awesome colors of the CV.
/// -> content
#let cvSection(
  title,
  highlighted: false,
  letters: 3,
  metadata: metadata,
  awesomeColors: awesomeColors,
) = {
  let lang = metadata.language
  let nonLatin = isNonLatin(lang)
  let beforeSectionSkip = eval(
    metadata.layout.at("before_section_skip", default: 1pt),
  )
  let accentColor = setAccentColor(awesomeColors, metadata)
  let highlightText = title.slice(0, letters)
  let normalText = title.slice(letters)
  let sectionTitleStyle(str, color: black) = {
    text(size: 16pt, weight: "regular", fill: color, upper(str))
  }

  v(beforeSectionSkip)
  if nonLatin {
    sectionTitleStyle(title, color: accentColor)
  } else {
    if highlighted {
      sectionTitleStyle(highlightText, color: accentColor)
      sectionTitleStyle(normalText, color: black)
    } else {
      sectionTitleStyle(title, color: black)
    }
  }
  h(2pt)
  box(width: 1fr, line(stroke: 0.9pt, length: 100%))
}

/// Add an entry to the CV.
///
/// - title (str): The title of the entry.
/// - society (str): The society of the entr (company, university, etc.).
/// - date (str): The date of the entry.
/// - location (str): The location of the entry.
/// - description (array): The description of the entry. It can be a string or an array of strings.
/// - logo (image): The logo of the society. If empty, no logo will be displayed.
/// - tags (array): The tags of the entry.
/// - metadata (array): (optional) the metadata read from the TOML file.
/// - awesomeColors (array): (optional) the awesome colors of the CV.
/// -> content
#let cvEntry(
  title: "Title",
  society: "Society",
  date: "Date",
  location: "Location",
  description: "Description",
  logo: "",
  tags: (),
  metadata: metadata,
  awesomeColors: awesomeColors,
) = {
  let accentColor = setAccentColor(awesomeColors, metadata)
  let beforeEntrySkip = eval(
    metadata.layout.at("before_entry_skip", default: 1pt),
  )
  let beforeEntryDescriptionSkip = eval(
    metadata.layout.at("before_entry_description_skip", default: 1pt),
  )

  let entryA1Style(str) = {
    text(size: 10pt, weight: "bold", str)
  }
  let entryA2Style(str) = {
    align(
      right,
      text(weight: "medium", fill: accentColor, style: "oblique", str),
    )
  }
  let entryB1Style(str) = {
    text(size: 8pt, fill: accentColor, weight: "medium", smallcaps(str))
  }
  let entryB2Style(str) = {
    align(
      right,
      text(size: 8pt, weight: "medium", fill: gray, style: "oblique", str),
    )
  }
  let entryDescriptionStyle(str) = {
    text(
      fill: regularColors.lightgray,
      {
        v(beforeEntryDescriptionSkip)
        str
      },
    )
  }
  let entryTagStyle(str) = {
    align(center, text(size: 8pt, weight: "regular", str))
  }
  let entryTagListStyle(tags) = {
    for tag in tags {
      box(
        inset: (x: 0.25em),
        outset: (y: 0.25em),
        fill: regularColors.subtlegray,
        radius: 3pt,
        entryTagStyle(tag),
      )
      h(5pt)
    }
  }

  let ifSocietyFirst(condition, field1, field2) = {
    return if condition {
      field1
    } else {
      field2
    }
  }
  let ifLogo(path, ifTrue, ifFalse) = {
    return if metadata.layout.entry.display_logo {
      if path == "" {
        ifFalse
      } else {
        ifTrue
      }
    } else {
      ifFalse
    }
  }
  let setLogoLength(path) = {
    return if path == "" {
      0%
    } else {
      4%
    }
  }
  let setLogoContent(path) = {
    return if logo == "" [] else {
      set image(width: 100%)
      logo
    }
  }

  v(beforeEntrySkip)
  table(
    columns: (ifLogo(logo, 3.5%, 0%), 1fr),
    inset: 0pt,
    stroke: none,
    align: horizon,
    column-gutter: ifLogo(logo, 6pt, 0pt),
    setLogoContent(logo),
    table(
      columns: (1fr, auto),
      inset: 0pt,
      stroke: none,
      row-gutter: 6pt,
      align: auto,
      {
        entryA1Style(
          ifSocietyFirst(
            metadata.layout.entry.display_entry_society_first,
            society,
            title,
          ),
        )
      },
      {
        entryA2Style(
          ifSocietyFirst(
            metadata.layout.entry.display_entry_society_first,
            location,
            date,
          ),
        )
      },

      {
        entryB1Style(
          ifSocietyFirst(
            metadata.layout.entry.display_entry_society_first,
            title,
            society,
          ),
        )
      },
      {
        entryB2Style(
          ifSocietyFirst(
            metadata.layout.entry.display_entry_society_first,
            date,
            location,
          ),
        )
      },
    ),
  )
  // entryDescriptionStyle(description)
  entryTagListStyle(tags)
}

/// Add a skill to the CV.
///
/// - type (str): The type of the skill. It is displayed on the left side.
/// - info (str | content): The information about the skill. It is displayed on the right side. Items can be seperated by `#hbar()`.
/// -> content
#let cvSkill(type: "Type", info: "Info") = {
  let skillTypeStyle(str) = {
    align(right, text(size: 10pt, weight: "bold", str))
  }
  let skillInfoStyle(str) = {
    text(str)
  }

  table(
    columns: (16%, 1fr),
    inset: 0pt,
    column-gutter: 10pt,
    stroke: none,
    skillTypeStyle(type), skillInfoStyle(info),
  )
  v(-6pt)
}

#let cvTraining(type: "Type", info: "Info", instructors: "Instructors") = {
  let skillTypeStyle(str) = {
    align(right, text(size: 10pt, weight: "bold", str))
  }
  let skillInfoStyle(str) = {
    text(str)
  }
  let skillInstructorStyle(str) = {
    text(style: "italic", fill: regularColors.darkgray, str)
  }

  table(
    columns: (12%, 30%, 1fr),
    inset: 0pt,
    column-gutter: 12pt,
    stroke: none,
    skillTypeStyle(type), skillInfoStyle(info), skillInstructorStyle(instructors)
  )
  v(-6pt)
}

#let cvPerformanceOld(title: "Title", character: "Character", company: "Company", director: "Director") = {
  let skillTypeStyle(str) = {
    align(left, text(size: 10pt, str))
  }
  let skillInfoStyle(str) = {
    text(str)
  }

  table(
    columns: (0.25fr, 0.1fr, 0.3fr, 0.15fr),
    inset: 0pt,
    column-gutter: 10pt,
    stroke: none,
    skillTypeStyle(title), skillInfoStyle(character), skillInfoStyle(company), skillInfoStyle(director)
  )
  v(-7pt)
}

#let cvPerformance(metadata) = {
  let skillTypeStyle(str) = {
    align(left, text(size: 10pt, str))
  }
  let shows = metadata.shows

  table(
    // columns: (1fr,) * 4,
    columns: (28%, 25%, 30%, 20%),
    inset: 3.5pt,
    column-gutter: 0pt,
    stroke: none,
    ..for (c) in shows {
      let title = c.at(1).title
      let character = c.at(1).character
      let company = c.at(1).company
      let director = c.at(1).director
      (skillTypeStyle(title), skillTypeStyle(character), skillTypeStyle(company), skillTypeStyle(director))
    }
  )
}
/// Add a Honor to the CV.
///
/// - date (str): The date of the honor.
/// - title (str): The title of the honor.
/// - issuer (str): The issuer of the honor.
/// - url (str): The URL of the honor.
/// - location (str): The location of the honor.
/// - awesomeColors (array): (optional) The awesome colors of the CV.
/// - metadata (array): (optional) The metadata read from the TOML file.
/// -> content
#let cvHonor(
  date: "1990",
  title: "Title",
  issuer: "",
  url: "",
  location: "",
  awesomeColors: awesomeColors,
  metadata: metadata,
) = {
  let accentColor = setAccentColor(awesomeColors, metadata)

  let honorDateStyle(str) = {
    align(right, text(str))
  }
  let honorTitleStyle(str) = {
    text(weight: "bold", str)
  }
  let honorIssuerStyle(str) = {
    text(str)
  }
  let honorLocationStyle(str) = {
    align(
      right,
      text(weight: "medium", fill: accentColor, style: "oblique", str),
    )
  }

  table(
    columns: (16%, 1fr, 15%),
    inset: 0pt,
    column-gutter: 10pt,
    align: horizon,
    stroke: none,
    honorDateStyle(date),
    if issuer == "" {
      honorTitleStyle(title)
    } else if url != "" {
      [
        #honorTitleStyle(link(url)[#title]), #honorIssuerStyle(issuer)
      ]
    } else {
      [
        #honorTitleStyle(title), #honorIssuerStyle(issuer)
      ]
    },
    honorLocationStyle(location),
  )
  v(-6pt)
}

/// Add the publications to the CV by reading a bib file.
///
/// - bib (bibliography): The `bibliography` object with the path to the bib file.
/// - keyList (list): The list of keys to include in the publication list.
/// - refStyle (str): The reference style of the publication list.
/// - refFull (bool): Whether to show the full reference or not.
/// -> content
#let cvPublication(bib: "", keyList: list(), refStyle: "apa", refFull: true) = {
  let publicationStyle(str) = {
    text(str)
  }
  show bibliography: it => publicationStyle(it)
  set bibliography(title: none, style: refStyle, full: refFull)
  bib
}

