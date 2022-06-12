import { RcFile } from 'antd/lib/upload/interface';
import { SetStateAction } from 'react';

interface IValue<T> {
  value: T;
  error: boolean;
}
interface Settings {
  files: IValue<RcFile[]>;
  isLoading: boolean;
  orderOfService: IValue<string>;
  selectedDate: IValue<string>;
  sermonDiscussionQns: IValue<string>;
  fileResults?: FileResult[];
}

type SetSettings = React.Dispatch<SetStateAction<Settings>>;

interface Result {
  title: string;
  comments: string;
  status: string;
}

interface FileResult {
  filename: string;
  results: Result[];
}

export type { Settings, SetSettings, Result, FileResult };
