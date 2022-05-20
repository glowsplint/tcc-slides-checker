import { SetStateAction } from 'react';
import { UploadFileStatus } from 'antd/lib/upload/interface';

interface UploadedFile {
  file: File;
  name: string;
}
interface Settings {
  isLoading: boolean;
  selectedDate?: string;
  orderOfService?: string;
}

type SetSettings = React.Dispatch<SetStateAction<Settings>>;

export type { Settings, SetSettings, UploadedFile };
