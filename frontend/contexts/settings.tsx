import React, { useState } from 'react';
import { SetSettings, Settings } from '../types';

const slidesSettings: Settings = {
  files: [],
  isLoading: false,
  orderOfService: "",
  selectedDate: "",
  sermonDiscussionQuestions: "",
};

const SettingsContext = React.createContext<{
  settings: Settings;
  setSettings: SetSettings;
}>({
  settings: slidesSettings,
  setSettings: () => {},
});

const SettingsProvider = ({ children }: { children: React.ReactNode }) => {
  const [settings, setSettings] = useState(slidesSettings);

  return (
    <SettingsContext.Provider value={{ settings, setSettings }}>
      {children}
    </SettingsContext.Provider>
  );
};

const useSettings = () => {
  return React.useContext(SettingsContext);
};

export { SettingsProvider, useSettings };
