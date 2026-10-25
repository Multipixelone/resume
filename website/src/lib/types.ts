export interface Show {
  id: string;
  title: string;
  character: string;
  company: string;
  director: string;
  on_resume: boolean;
  resume_order: number;
  year?: number;
  rehearsal_start?: string;
  performance_start?: string;
  closing_night?: string;
  ticket_url?: string;
  livestream?: boolean;
  photo?: string;
  photo_alt?: string;
}
export interface PhotoNote {
  title?: string;
  role?: string;
  blurb?: string;
}
export interface Photo {
  file: string;
  width: number;
  height: number;
  alt: string;
  /** Homepage spread slot; reel-only photos have none. */
  placement?: string;
  caption?: string;
  credit?: string;
  creditUrl?: string;
  note?: PhotoNote;
  /** Site path of the photo's show page. */
  reel?: string;
  /** What that show page holds, for the homepage caption. */
  reelCount?: { photos: number; videos: number };
}
export interface ShowVideo {
  id: string;
  title: string;
}
/** A reel clip's caption labels, from its canonical show. */
export interface RecordingCredit {
  title: string;
  character: string;
  year?: number;
  /** Site path of the show's page, when it has one. */
  path?: string;
}
export interface Recording extends ShowVideo {
  /** The clip to watch first. */
  start: boolean;
  show?: RecordingCredit;
}
export interface ShowReel {
  id: string;
  title: string;
  character: string;
  company: string;
  director: string;
  on_resume: boolean;
  path: string;
  photos: Photo[];
  videos: ShowVideo[];
}
export interface CurrentShow extends Show {
  status: 'rehearsing' | 'performing';
  rehearsal_start: string;
  performance_start: string;
  closing_night: string;
}
