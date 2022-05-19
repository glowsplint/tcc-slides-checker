import { SettingsProvider } from '../contexts/settings';
import '../styles/globals.css';
import 'antd/dist/antd.css';

import type { AppProps } from "next/app";

function MyApp({ Component, pageProps }: AppProps) {
  return (
    <SettingsProvider>
      <Component {...pageProps} />
    </SettingsProvider>
  );
}

export default MyApp;
