import Form from '../components/Form';
import Layout from '../components/Layout';
import React from 'react';
import type { NextPage } from "next";

const HomePage: NextPage = () => {
  return (
    <Layout>
      <Form />
    </Layout>
  );
};

export default HomePage;
