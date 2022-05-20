import Head from 'next/head';
import moment from 'moment';
import React from 'react';
import styles from '../styles/Home.module.css';
import { InboxOutlined, UploadOutlined } from '@ant-design/icons';
import { RcFile } from 'antd/lib/upload';
import { SetSettings, UploadedFile } from '../types';
import { useSettings } from '../contexts/settings';
import {
  Button,
  DatePicker,
  Input,
  Space,
  Typography,
  Upload,
  message,
} from "antd";

import type { NextPage } from "next";

const { Title } = Typography;
const { TextArea } = Input;
const { Dragger } = Upload;

/* Constants */
const DEVELOPMENT_MODE = process.env.NEXT_PUBLIC_DEVELOPMENT_MODE === "True";

const getFormData = (
  fileList: UploadedFile[],
  isGenerateFinalValues: boolean
): FormData => {
  /**
   * Creates a new FormData object and adds the File objects and parameters into it
   * If you need to pass data to the backend, you should add it here.
   */
  let formData = new FormData();
  fileList.forEach((uploadedFile) =>
    formData.append("files", uploadedFile.file, uploadedFile.file.name)
  );
  formData.append("is_generate_final_values", isGenerateFinalValues.toString());
  return formData;
};

/* Logic */
const makePOSTRequest = async ({
  formData,
  backendPath,
}: {
  formData: FormData;
  backendPath: string;
}) => {
  /**
   * Initiates the POST request to the appropriate backend
   */

  // backendPath is a string that starts with /
  console.assert(backendPath.startsWith("/"));

  let path = backendPath;
  if (DEVELOPMENT_MODE) {
    path = `http://localhost:5000${backendPath}`;
  }

  return fetch(path, {
    method: "POST",
    body: formData,
  });
};

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

/* Components */
const OrderOfServiceInput = () => {
  // TODO: Replace this with a table element
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

const props = (setSettings: SetSettings) => {
  return {
    name: "file",
    maxCount: 1,
    multiple: true,
    beforeUpload: (file: File) => {
      const isPPTX =
        file.type ===
        "application/vnd.openxmlformats-officedocument.presentationml.presentation";
      if (!isPPTX) {
        message.error(`${file.name} is not a .pptx file`);
      }
      setSettings((previous) => {
        return { ...previous, file };
      });
      // Prevent upload
      return false;
    },
  };
};

const FileUploadInput = () => {
  const { setSettings } = useSettings();
  return (
    <Dragger {...props(setSettings)}>
      <p className="ant-upload-drag-icon">
        <InboxOutlined />
      </p>
      <p className="ant-upload-text">
        Click or drag file here to upload Service Slides.
      </p>
      <p className="ant-upload-hint">File must have a .pptx extension.</p>
    </Dragger>
  );
};

const UploadButton = () => {
  return (
    <Button type="primary" icon={<UploadOutlined />}>
      Upload
    </Button>
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
          <Space className={styles.title}>
            <Title>TCC Slides Checker</Title>
          </Space>
          <FileUploadInput />
          <DateSelector />
          <OrderOfServiceInput />
          <SermonDiscussionQuestionsInput />
          <UploadButton />
        </Space>
      </main>
    </div>
  );
};

export default Home;
