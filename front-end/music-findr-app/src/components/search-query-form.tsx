import React, { useEffect, useState } from "react";
import { Form, Typography, Spin } from "antd";
import { useSearchQueryApi } from "../hooks/use-search-query-api";
import SearchQueryInput from "./search-query-input";

const { Text } = Typography;

const SearchQueryForm: React.FC = () => {
  const [form] = Form.useForm();
  const [searchQuery, setSearchQuery] = useState<string>("");

  const { data, isLoading, isError, error, refetch } =
    useSearchQueryApi(searchQuery);

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
      >
        <Form.Item
          name="searchQueryText"
          rules={[{ required: true, message: "Please input your query!" }]}
        >
          <SearchQueryInput onSearch={() => form.submit()} />
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

export default SearchQueryForm;
