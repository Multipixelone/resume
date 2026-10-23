export interface Show {
  id: string;
  title: string;
  character: string;
  company: string;
  director: string;
  on_resume: boolean;
  resume_order: number;
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
}
export interface ShowVideo {
  id: string;
  title: string;
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
