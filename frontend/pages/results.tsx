import Layout from '../components/Layout';
import Link from 'next/link';
import React from 'react';
import Results from '../components/Results';
import { Empty } from 'antd';
import { NextPage } from 'next';
import { useSettings } from '../contexts/settings';

const NoResults = () => {
  return (
    <Empty
      description={
        <span>
          There are no results to be displayed. Please return to the{" "}
          <Link href="/">
            <a>main page</a>
          </Link>
          .
        </span>
      }
    ></Empty>
  );
};

const ResultsPage: NextPage = () => {
  const { settings } = useSettings();
  return <Layout>{settings.fileResults ? <Results /> : <NoResults />}</Layout>;
};
export default ResultsPage;
