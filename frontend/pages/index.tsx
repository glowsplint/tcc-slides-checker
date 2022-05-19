import Head from 'next/head';
import moment from 'moment';
import React from 'react';
import styles from '../styles/Home.module.css';
import { DatePicker, Space } from 'antd';
import { Input } from 'antd';
import { Typography } from 'antd';
import { useSettings } from '../contexts/settings';

import type { NextPage } from "next";

const { Title } = Typography;
const { TextArea } = Input;

const disabledDate = (date: moment.MomentInput) => {
  // Can only select sundays
  return moment(date).day() !== 0;
};

const DateSelector = () => {
  const { setSettings } = useSettings();

  const onChange = (date: moment.MomentInput, dateString: string) => {
    setSettings((previous) => {
      return { ...previous, selectedDate: dateString };
    });
  };

  return (
    <DatePicker
      disabledDate={disabledDate}
      placeholder="Select date of Sunday service."
      onChange={onChange}
    />
  );
};

const OrderOfServiceInput = () => {
  const { setSettings } = useSettings();

  const onPaste = (event: React.ClipboardEvent) => {
    event.clipboardData.items[0].getAsString((contents) => {
      setSettings((previous) => {
        return { ...previous, orderOfService: contents };
      });
    });
  };

  return (
    <TextArea
      placeholder="Paste order of service here from the Rosters 2022 (Staff & Admins) sheet."
      autoSize={{ minRows: 2 }}
      onPaste={onPaste}
    />
  );
};

const SermonDiscussionQuestionsInput = () => {
  const { setSettings } = useSettings();

  const onChange = (event: React.ChangeEvent) => {
    setSettings((previous) => {
      return {
        ...previous,
        sermonDiscussionQuestions: (event.target as HTMLTextAreaElement).value,
      };
    });
  };
  return (
    <TextArea
      placeholder="Paste sermon discussion questions here."
      autoSize
      onChange={onChange}
    />
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
        <Space direction="vertical">
          <Title>TCC Slides Checker</Title>
          <DateSelector />
          <OrderOfServiceInput />
          <SermonDiscussionQuestionsInput />
        </Space>
      </main>
    </div>
  );
};

export default Home;
