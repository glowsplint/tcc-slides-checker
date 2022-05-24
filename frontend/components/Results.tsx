import React from 'react';
import { Card, Typography } from 'antd';
import { Result } from '../types';
import { useSettings } from '../contexts/settings';
import {
  CheckCircleOutlined,
  ExclamationCircleOutlined,
  WarningOutlined,
} from "@ant-design/icons";


const { Text } = Typography;

const WarningCard = ({ result }: { result: Result }) => {
  return (
    <>
      <WarningOutlined />
      <Text strong> {result.title}</Text>
    </>
  );
};

const ErrorCard = ({ result }: { result: Result }) => {
  return (
    <>
      <ExclamationCircleOutlined />
      <Text strong> {result.title}</Text>
    </>
  );
};

const PassCard = ({ result }: { result: Result }) => {
  return (
    <>
      <CheckCircleOutlined />
      <Text strong> {result.title}</Text>
    </>
  );
};

const Results = () => {
  const { settings } = useSettings();
  return (
    <>
      {settings.results?.map((result, index) => {
        let header: React.ReactElement = <></>;
        switch (result.status) {
          case "Warning":
            header = <WarningCard result={result} />;
            break;
          case "Error":
            header = <ErrorCard result={result} />;
            break;
          case "Pass":
            header = <PassCard result={result} />;
            break;
        }
        return (
          <Card title={header} key={index}>
            {result.comments}
          </Card>
        );
      })}
    </>
  );
};

export default Results;
