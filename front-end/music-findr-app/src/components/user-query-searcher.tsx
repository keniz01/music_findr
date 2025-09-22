// src/components/SearchForm.tsx
import React, { useState } from 'react';
import { Form, Input, Button, Typography, Spin } from 'antd';
import { useUserQuerySearchApi } from '../hooks/use-user-query-search-api';

const { Text } = Typography;

const UserQuerySearcher: React.FC = () => {
  const [searchQuery, setSearchQuery] = useState<string>('');
  const [form] = Form.useForm();

  const { data, isLoading, isError } = useUserQuerySearchApi(searchQuery);

  const onFinish = (values: { query: string }) => {
    setSearchQuery(values.query.trim());
  };

  return (
    <div style={{ maxWidth: 500, margin: '0 auto', padding: 24 }}>
      <Form form={form} layout="vertical" onFinish={onFinish}>
        <Form.Item
          name="query"
          label="Search Query"
          rules={[{ required: true, message: 'Please input your query!' }]}
        >
          <Input placeholder="Enter your search term" />
        </Form.Item>
        <Form.Item>
          <Button type="primary" htmlType="submit" loading={isLoading}>
            Search
          </Button>
        </Form.Item>
      </Form>

      {isLoading && <Spin />}

      {data && (
        <div style={{ marginTop: 16 }}>
          <Text strong>Result:</Text>
          <div>{data}</div>
        </div>
      )}

      {isError && (
        <div style={{ marginTop: 16 }}>
          <Text type="danger">Error fetching data</Text>
        </div>
      )}
    </div>
  );
};

export default UserQuerySearcher;
