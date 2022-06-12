import React from 'react';
import styles from '../styles/Results.module.css';
import { Card, Typography } from 'antd';
import { Collapse } from 'antd';
import { NextPage } from 'next';
import { Result } from '../types';
import { Status } from '../enums';
import { useSettings } from '../contexts/settings';
import {
  CheckCircleOutlined,
  ExclamationCircleOutlined,
  WarningOutlined,
} from "@ant-design/icons";


const { Text } = Typography;
const { Panel } = Collapse;

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

const Results: NextPage = () => {
  const { settings } = useSettings();
  return (
    <Collapse>
      {settings.fileResults?.map((fileResult) => {
        return (
          <Panel header={fileResult.filename} key={fileResult.filename}>
            {fileResult.results.map((result, index) => {
              switch (Number(result.status)) {
                case Status.WARNING:
                  return <WarningCard result={result} key={index} />;
                case Status.ERROR:
                  return <ErrorCard result={result} key={index} />;
                case Status.PASS:
                  return <PassCard result={result} key={index} />;
              }
            })}
          </Panel>
        );
      })}
    </Collapse>
  );
};

export default Results;
