import React, { useEffect, useState } from "react";
import { Form, Input, Typography, Spin } from "antd";
import StyledButton from "./styled-button";
import { useSearchQueryApi } from "../hooks/use-search-query-api";

const { Text } = Typography;

const QuerySearchForm: React.FC = () => {
  const [form] = Form.useForm();
  const [searchQuery, setSearchQuery] = useState<string>("");

  const { data, isLoading, isError, error, refetch } = useSearchQueryApi(searchQuery);

  const onFinish = (values: { searchQueryText: string }) => {
    const trimmedQuery = values.searchQueryText.trim();
    if (!trimmedQuery) return;

    setSearchQuery(trimmedQuery);
  };

  useEffect(() => {
    if (searchQuery) {
      refetch();
    }
  }, [searchQuery, refetch]);

  return (
    <div style={{ maxWidth: 500, margin: "0 auto", padding: 24 }}>
      <Form
        form={form}
        layout="vertical"
        onFinish={onFinish}
        id="query-search-form"
        initialValues={{ query: "" }}
      >
        <Form.Item
          name="searchQueryText"
          label="Search Query"
          rules={[
            { required: true, message: "Please input your query!" },
            { min: 1, message: "Query must be at least 3 characters" }
          ]}
        >
          <Input placeholder="Enter your search term" id="search-query-input" />
        </Form.Item>
        <Form.Item>
          <StyledButton
            type="primary"
            htmlType="submit"
            id="query-search-button"
            text="Search"
            disabled={isLoading}
          />
        </Form.Item>
      </Form>

      {isLoading && <Spin />}

      {data && !isLoading && (
        <div style={{ marginTop: 16 }}>
          <div>{data || "No results found."}</div>
        </div>
      )}

      {isError && (
        <div style={{ marginTop: 16 }}>
          <Text type="danger">Error fetching data</Text>
          {error instanceof Error && <div>{error.message}</div>}
        </div>
      )}
    </div>
  );
};

export default QuerySearchForm;
