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

const WarningCard = ({ result, key }: { result: Result; key: number }) => {
  return (
    <Card
      key={key}
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

const ErrorCard = ({ result, key }: { result: Result; key: number }) => {
  return (
    <Card
      key={key}
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

const PassCard = ({ result, key }: { result: Result; key: number }) => {
  return (
    <Card
      key={key}
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
        let component: React.ReactElement = <></>;
        switch (result.status) {
          case "Warning":
            component = <WarningCard result={result} key={index} />;
            break;
          case "Error":
            component = <ErrorCard result={result} key={index} />;
            break;
          case "Passing":
            component = <PassCard result={result} key={index} />;
            break;
        }
        return <>{component}</>;
      })}
    </>
  );
};

export default Results;
