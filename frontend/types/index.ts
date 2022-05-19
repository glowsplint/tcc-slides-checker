import { SetStateAction } from 'react';

interface Settings {
  isLoading: boolean;
  selectedDate?: string;
  orderOfService?: string;
}

type SetSettings = React.Dispatch<SetStateAction<Settings>>;

export type { Settings, SetSettings };
