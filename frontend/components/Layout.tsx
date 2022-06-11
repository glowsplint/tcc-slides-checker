import Head from 'next/head';
import React from 'react';
import styles from '../styles/Layout.module.css';
import { Space, Typography } from 'antd';


const { Title, Text } = Typography;

const Layout = ({ children }: { children: React.ReactNode }) => {
  return (
    <main className={styles.main}>
      <div className={styles.container}>
        <Head>
          <title>TCC Slides Checker</title>
          <meta
            name="description"
            content="The Crossing Church Slides Checker"
          />
          <link rel="icon" href="/favicon.ico" />
        </Head>

        <Space direction="vertical">
          <Space className={styles.title}>
            <Title>TCC Slides Checker</Title>
            <Text type="secondary">{process.env.NEXT_PUBLIC_APP_VERSION}</Text>
          </Space>
          {children}
        </Space>
      </div>
    </main>
  );
};

export default Layout;
