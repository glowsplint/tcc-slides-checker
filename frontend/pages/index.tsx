import Head from 'next/head';
import React, { useRef } from 'react';
import styles from '../styles/Home.module.css';
import { Column, EditableCell, Table2 } from '@blueprintjs/table';
import { HotkeysProvider } from '@blueprintjs/core';

import type { NextPage } from "next";

const Grid = () => {
  const onKeyDown = (event: React.KeyboardEvent) => {
    if (event.ctrlKey && event.key == "v") {
      navigator.clipboard.readText().then((text) => console.log(text));
    }
  };

  const cellRenderer = () => {
    return (
      <EditableCell
        onKeyDown={(event: React.KeyboardEvent) => onKeyDown}
        interactive
      />
    );
  };

  return (
    <div id="grid">
      <HotkeysProvider>
        <Table2 numRows={11}>
          <Column cellRenderer={cellRenderer} name="Item" />
          <Column cellRenderer={cellRenderer} name="Mins" />
          <Column cellRenderer={cellRenderer} name="Things to note" />
        </Table2>
      </HotkeysProvider>
    </div>
  );
};

const Home: NextPage = () => {
  return (
    <div className={styles.container}>
      <Head>
        <title>TCC Slides Checker</title>
        <meta name="description" content="The Crossing Church Slides Checker" />
        <link rel="icon" href="/favicon.ico" />
      </Head>

      <main className={styles.main}>
        <Grid />
      </main>
    </div>
  );
};

export default Home;
