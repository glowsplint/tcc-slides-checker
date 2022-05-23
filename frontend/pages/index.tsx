import Head from 'next/head';
import moment from 'moment';
import React from 'react';
import styles from '../styles/Home.module.css';
import { InboxOutlined, UploadOutlined } from '@ant-design/icons';
import { RcFile } from 'antd/lib/upload';
import { SetSettings, Settings } from '../types';
import { SettingsProvider, useSettings } from '../contexts/settings';
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

const getFormData = (settings: Settings): FormData => {
  /**
   * Creates a new FormData object and adds the File objects and parameters into it
   */
  let formData = new FormData();
  settings.files.value.forEach((file) =>
    formData.append("files", file, file.name)
  );
  formData.append(
    "selected_date",
    settings.selectedDate.value?.toString() as string
  );
  formData.append(
    "req_order_of_service",
    settings.orderOfService.value?.toString() as string
  );
  formData.append(
    "sermon_discussion_qns",
    settings.sermonDiscussionQns.value?.toString() as string
  );
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

const setIsLoading = (setSettings: SetSettings, bool: boolean) => {
  setSettings((prevSettings) => {
    return { ...prevSettings, isLoading: bool };
  });
};

const showInvalidUploadError = () => {
  message.error("You must upload files below and fill in all inputs!");
};

const showInputErrors = (setSettings: SetSettings) => {
  setSettings((previous) => {
    const isFilesError = previous.files.value.length === 0;
    const isSelectedDateError = previous.selectedDate.value.length === 0;
    const isOrderOfServiceError = previous.orderOfService.value.length === 0;
    const isSermonDiscussionQnsError =
      previous.sermonDiscussionQns.value.length === 0;
    return {
      ...previous,
      files: { ...previous.files, error: isFilesError },
      selectedDate: { ...previous.selectedDate, error: isSelectedDateError },
      orderOfService: {
        ...previous.orderOfService,
        error: isOrderOfServiceError,
      },
      sermonDiscussionQns: {
        ...previous.sermonDiscussionQns,
        error: isSermonDiscussionQnsError,
      },
    };
  });
};

const getResponse = (settings: Settings) => {
  /**
   * Sends POST request with input Excel files
   */
  const formData = getFormData(settings);
  const response = makePOSTRequest({
    formData,
    backendPath: "/api/upload/",
  });
  return response;
};

const disabledDate = (date: moment.MomentInput) => {
  // Can only select sundays
  return moment(date).day() !== 0;
};

const DateSelector = () => {
  const { settings, setSettings } = useSettings();

  const onChange = (date: moment.MomentInput, dateString: string) => {
    setSettings((previous) => {
      return { ...previous, selectedDate: { value: dateString, error: false } };
    });
  };

  return (
    <DatePicker
      disabledDate={disabledDate}
      placeholder="Select date of Sunday service."
      onChange={onChange}
      status={settings.selectedDate.error ? "error" : ""}
    />
  );
};

/* Components */
const OrderOfServiceInput = () => {
  // TODO: Replace this with a table element
  const { settings, setSettings } = useSettings();

  const onChange: React.ChangeEventHandler<HTMLTextAreaElement> = (event) => {
    setSettings((previous) => {
      return {
        ...previous,
        orderOfService: { value: event.target.value, error: false },
      };
    });
  };

  return (
    <TextArea
      placeholder="Paste order of service here from the Rosters 2022 (Staff & Admins) sheet."
      autoSize={{ minRows: 2 }}
      onChange={onChange}
      status={settings.orderOfService.error ? "error" : ""}
    />
  );
};

const SermonDiscussionQnsInput = () => {
  const { settings, setSettings } = useSettings();

  const onChange = (event: React.ChangeEvent) => {
    setSettings((previous) => {
      return {
        ...previous,
        sermonDiscussionQns: {
          value: (event.target as HTMLTextAreaElement).value,
          error: false,
        },
      };
    });
  };
  return (
    <TextArea
      placeholder="Paste sermon discussion questions here."
      autoSize
      onChange={onChange}
      status={settings.sermonDiscussionQns.error ? "error" : ""}
    />
  );
};

const props = (setSettings: SetSettings) => {
  return {
    name: "file",
    maxCount: 1,
    multiple: true,
    accept:
      "application/vnd.openxmlformats-officedocument.presentationml.presentation",
    beforeUpload: (file: File, fileList: RcFile[]) => {
      setSettings((previous) => {
        return { ...previous, files: { value: [file], error: false } };
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
  const { settings, setSettings } = useSettings();
  const onClickUpload: React.MouseEventHandler = async () => {
    /**
     * Sends the POST request, extracts the output files from the response,
     * and sets the output files into context
     */
    const isInvalidUpload =
      settings.files.value.length === 0 ||
      settings.selectedDate.value.length === 0 ||
      settings.orderOfService.value.length === 0 ||
      settings.sermonDiscussionQns.value.length === 0;

    if (isInvalidUpload) {
      showInvalidUploadError();
      showInputErrors(setSettings);
      return;
    }
    setIsLoading(setSettings, true);
    const response = getResponse(settings);
    console.log(response);
    setIsLoading(setSettings, false);
  };
  return (
    <Button type="primary" icon={<UploadOutlined />} onClick={onClickUpload}>
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
          <SermonDiscussionQnsInput />
          <UploadButton />
        </Space>
      </main>
    </div>
  );
};

export default Home;
