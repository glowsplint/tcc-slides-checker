import { SetStateAction } from 'react';

interface Settings {
  files: File[];
  isLoading: boolean;
  orderOfService: string;
  selectedDate: string;
  sermonDiscussionQuestions: string;
}

type SetSettings = React.Dispatch<SetStateAction<Settings>>;

export type { Settings, SetSettings };
