import React from 'react';
import Results from '../components/Results';
import { Button } from 'antd';
import { CaretLeftOutlined } from '@ant-design/icons';
import { NextPage } from 'next';
import { useRouter } from 'next/router';

const BackButton = () => {
  const router = useRouter();
  const onClick = () => {
    router.push("/");
  };
  return <Button icon={<CaretLeftOutlined />} onClick={onClick} />;
};

const ResultsPage: NextPage = () => {
  return (
    <>
      <BackButton />
      <Results />
    </>
  );
};
export default ResultsPage;
