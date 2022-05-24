import Form from '../components/Form';
import Head from 'next/head';
import React from 'react';
import Results from '../components/Results';
import styles from '../styles/Home.module.css';
import { Button, Space, Typography } from 'antd';
import { CaretLeftOutlined } from '@ant-design/icons';
import { useSettings } from '../contexts/settings';

import type { NextPage } from "next";

const { Title, Text } = Typography;

const BackButton = () => {
  const { setSettings } = useSettings();
  const onClick = () => {
    setSettings((previous) => {
      const next = { ...previous };
      delete next.results;
      return next;
    });
  };
  return <Button icon={<CaretLeftOutlined />} onClick={onClick} />;
};

const Home: NextPage = () => {
  const { settings } = useSettings();
  return (
    <div className={styles.container}>
      <Head>
        <title>TCC Slides Checker</title>
        <meta name="description" content="The Crossing Church Slides Checker" />
        <link rel="icon" href="/favicon.ico" />
      </Head>

      <main className={styles.main}>
        <Space direction="vertical">
          <Space className={styles.title}>
            <Title>TCC Slides Checker</Title>
            <Text type="secondary">{process.env.NEXT_PUBLIC_APP_VERSION}</Text>
            {settings.results ? <BackButton /> : null}
          </Space>
          {settings.results ? null : <Form />}
          {settings.results ? <Results /> : null}
        </Space>
      </main>
    </div>
  );
};

export default Home;
