import React, { useState } from 'react';
import { Form, Input, Typography, Spin } from 'antd';
import { useUserQuerySearchApi } from '../hooks/use-user-query-search-api';
import StyledButton from './styled-button';

const { Text } = Typography;

const QuerySearchForm: React.FC = () => {
  const [searchQuery, setSearchQuery] = useState<string>('');
  const [form] = Form.useForm();

  const { data, isLoading, isError } = useUserQuerySearchApi(searchQuery);

  const onFinish = (values: { query: string }) => {
    setSearchQuery(values.query.trim());
  };

  return (
    <div style={{ maxWidth: 500, margin: '0 auto', padding: 24 }}>
      <Form form={form} layout="vertical" onFinish={onFinish} id="query-search-form">
        <Form.Item
          name="query"
          label="Search Query"
          id="query-search-input"
          rules={[{ required: true, message: 'Please input your query!', whitespace: true, min: 3 }]}
        >
          <Input placeholder="Enter your search term" />
        </Form.Item>
        <Form.Item>
          <StyledButton
            type="primary"
            htmlType="submit"
            id="query-search-button"
            text="Search"
            onClick={function (): void { }}
          />
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

export default QuerySearchForm;
