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
  duration?: number;
  poster?: string;
  film?: { character: string; company: string; director: string };
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
/** Header facts from the resume's base metadata; a field hidden on the PDF is absent. */
export interface ResumeVitals {
  voicePart?: string;
  height?: string;
}
export interface Degree {
  title: string;
  school: string;
  location: string;
  date: string;
}
export interface TrainingTechnique {
  technique: string;
  instructors: string[];
}
/** Consecutive training rows that share a discipline. */
export interface TrainingDiscipline {
  discipline: string;
  techniques: TrainingTechnique[];
}
export interface CurrentShow extends Show {
  status: 'rehearsing' | 'performing';
  rehearsal_start: string;
  performance_start: string;
  closing_night: string;
}
/** A registered resume (or the composite) as the site offers it. */
export interface Download {
  id: string;
  title: string;
  subtitle: string;
  field: string;
  hidden: boolean;
  pdf: string;
  preview: string;
  /** Name the browser saves it under, from the title. */
  filename: string;
}
