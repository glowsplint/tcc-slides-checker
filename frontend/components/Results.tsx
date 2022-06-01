import React from 'react';
import styles from '../styles/Results.module.css';
import { Card, Typography } from 'antd';
import { Result } from '../types';
import { useSettings } from '../contexts/settings';
import {
  CheckCircleOutlined,
  ExclamationCircleOutlined,
  WarningOutlined,
} from "@ant-design/icons";


const { Text } = Typography;

const CardTitle = ({
  result,
  icon,
  className,
}: {
  result: Result;
  icon: React.ReactElement;
  className: string;
}) => {
  return (
    <>
      {icon}
      <Text strong className={className}>
        {" "}
        {result.title}
      </Text>
    </>
  );
};

const WarningCard = ({ result }: { result: Result }) => {
  return (
    <Card
      type="inner"
      headStyle={{ backgroundColor: "#fbb360" }}
      title={
        <CardTitle
          icon={<WarningOutlined style={{ color: "#77450D" }} />}
          result={result}
          className={styles.black}
        />
      }
    >
      {result.comments}
    </Card>
  );
};

const ErrorCard = ({ result }: { result: Result }) => {
  return (
    <Card
      headStyle={{ backgroundColor: "#cd4246" }}
      type="inner"
      title={
        <CardTitle
          icon={<ExclamationCircleOutlined style={{ color: "#FA999C" }} />}
          result={result}
          className={styles.white}
        />
      }
    >
      {result.comments}
    </Card>
  );
};

const PassCard = ({ result }: { result: Result }) => {
  return (
    <Card
      headStyle={{ backgroundColor: "#238551" }}
      type="inner"
      title={
        <CardTitle
          icon={<CheckCircleOutlined style={{ color: "#72CA9B" }} />}
          result={result}
          className={styles.white}
        />
      }
    >
      {result.comments}
    </Card>
  );
};

const Results = () => {
  const { settings } = useSettings();
  return (
    <>
      {settings.results?.map((result, index) => {
        switch (result.status) {
          case "Warning":
            return <WarningCard result={result} key={index} />;
          case "Error":
            return <ErrorCard result={result} key={index} />;
          case "Passing":
            return <PassCard result={result} key={index} />;
        }
      })}
    </>
  );
};

export default Results;
