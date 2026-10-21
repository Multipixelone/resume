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
  placement: string;
  caption?: string;
  credit?: string;
  creditUrl?: string;
  note?: PhotoNote;
}
export interface CurrentShow extends Show {
  status: 'rehearsing' | 'performing';
  rehearsal_start: string;
  performance_start: string;
  closing_night: string;
}
