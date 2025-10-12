import React from "react";
import { Form, type FormInstance } from "antd";
import SearchQueryInput from "./search-query-input";

interface SearchFormProps {
  form: FormInstance;
  onFinish: (values: { searchQueryText: string }) => void;
  onClear?: () => void;
}

const SearchForm: React.FC<SearchFormProps> = ({ form, onFinish, onClear }) => {
  return (
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
        <SearchQueryInput onSearch={() => form.submit()} onClear={onClear} />
      </Form.Item>
    </Form>
  );
};

export default SearchForm;
