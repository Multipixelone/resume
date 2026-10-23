// Selected from the existing portfolio, not a complete preservation inventory.
// Alt text describes the inspected pictures without guessing production/photographer credits.
// Add caption/credit/creditUrl only from Finn's verified media handoff.
// Fixed photo captions: `show` is a metadata/theatre.toml id (title and role come from there),
// `blurb` is Finn's own words about the performance. Leave either empty to skip it.
// A `show` also gives that production a page at /shows/<show>/ with all of its photos,
// linked from its theatre credit and from the homepage print.
// Each `placement` is a fixed slot in the homepage spread (site.css), so use each one once.
// Leave `placement` off to add a photo to its show's page only.
export const performancePhotos = [
  {
    file: "finn_photo_reel_2.jpg",
    width: 4996,
    height: 3468,
    alt: "Three performers dancing with one arm raised, the center performer in an orange sweater.",
    placement: "wide",
    show: "song-dance-revue",
    blurb: "",
  },
  {
    file: "2X9A9381-X4.jpg",
    width: 1638,
    height: 2048,
    alt: "A performer in a tall red-and-white striped hat and cat makeup, reaching forward with both hands.",
    placement: "tall",
    show: "seussical",
    blurb: "",
  },
  {
    file: "composer_singing.jpg",
    width: 1280,
    height: 960,
    alt: "Performers singing together, with the center performer holding a notebook against a burgundy sweater.",
    placement: "small",
    show: "composer-project-revue",
    blurb: "",
  },
  {
    file: "2X9A9285-4K.jpg",
    width: 1420,
    height: 1136,
    alt: "A performer in a tall red-and-white striped hat and cat makeup steps forward mid-dance, with four ensemble members in orange vests and safari helmets behind.",
    placement: "wide-right",
    show: "seussical",
    blurb: "",
  },
  {
    file: "20250529_Molloy_University_Legally_Blonde_JRV_3462-X3.jpg",
    width: 655,
    height: 893,
    alt: "A curly-haired performer in a gray sweater smiles and holds a backpack strap, while a seated performer looks up from a chair.",
    placement: "tall-left",
    show: "legally-blonde",
    blurb: "",
  },
  {
    file: "_DSC2342-X3.jpg",
    width: 739,
    height: 721,
    alt: "Two performers in fedoras, one in a pinstripe suit, lean in over a seated performer in a red velvet jacket at a small wooden desk.",
    placement: "small-right",
    show: "kiss-me-kate",
    blurb: "",
  },
];

// `show` (a theatre.toml id) also embeds the video on that show's page. Set it only
// when the recording is from that production.
export const recordings = [
  { id: "ucVBjbfxrHA", title: "She Loves Me" },
  { id: "DYrR7xup_Js", title: "I Love to Sing-a & Love Me, Love Me Not" },
  { id: "-QPog0QsJ9s", title: "No One Has to Know" },
  { id: "ZP38u-e76BY", title: "Circus McGurkus", show: "seussical" },
  { id: "nwI8Dr8u1OM", title: "How Lucky You Are", show: "seussical" },
];
