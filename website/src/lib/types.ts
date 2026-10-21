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
  photo?: string;
  photo_alt?: string;
}
export interface CurrentShow extends Show {
  status: 'rehearsing' | 'performing';
  rehearsal_start: string;
  performance_start: string;
  closing_night: string;
}
