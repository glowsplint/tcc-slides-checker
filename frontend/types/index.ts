import { RcFile } from 'antd/lib/upload/interface';
import { SetStateAction } from 'react';

interface ValueAndError<T> {
  value: T;
  error: boolean;
}
interface Settings {
  files: ValueAndError<RcFile[]>;
  isLoading: boolean;
  orderOfService: ValueAndError<string>;
  selectedDate: ValueAndError<string>;
  sermonDiscussionQns: ValueAndError<string>;
  results?: Result[];
}

type SetSettings = React.Dispatch<SetStateAction<Settings>>;

interface Result {
  title: string;
  comments: string;
  status: string;
}

interface SlidesResponse {
  results: Result[];
}

export type { Settings, SetSettings, Result, SlidesResponse };
