{
  python3,
  writeShellApplication,
}:
let
  python = python3.withPackages (p: [
    p.reportlab
    p.pymupdf
    p.pillow
    p.fonttools
    p.brotli
    p.zxing-cpp
  ]);
in
writeShellApplication {
  name = "business-cards";
  runtimeInputs = [ python ];
  # Run against an explicit working checkout. In particular, the proprietary
  # Sabon file is a runtime argument, never a derivation input or store copy.
  text = ''
    root=.
    args=("$@")
    while [ "$#" -gt 0 ]; do
      case "$1" in
        --root)
          if [ "$#" -lt 2 ]; then
            echo "--root requires a checkout path" >&2
            exit 2
          fi
          root="$2"
          shift 2
          ;;
        --root=*) root="''${1#--root=}"; shift ;;
        *) shift ;;
      esac
    done
    python3 ${../scripts/check_card_profiles.py} --root "$root"
    exec python3 "$root/scripts/business_cards.py" "''${args[@]}"
  '';
}
