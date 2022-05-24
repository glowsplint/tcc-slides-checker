import { SetStateAction } from 'react';

interface ValueAndError<T> {
  value: T;
  error: boolean;
}
interface Settings {
  files: ValueAndError<File[]>;
  isLoading: boolean;
  orderOfService: ValueAndError<string>;
  selectedDate: ValueAndError<string>;
  sermonDiscussionQns: ValueAndError<string>;
}

type SetSettings = React.Dispatch<SetStateAction<Settings>>;

interface SlidesResponse {
  result: {
    title: string;
    comments: string;
    status: string;
  };
}

export type { Settings, SetSettings, SlidesResponse };
