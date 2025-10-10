import React from "react";
import { Form, type FormInstance } from "antd";
import SearchQueryInput from "./search-query-input";

interface SearchFormProps {
  form: FormInstance;
  onFinish: (values: { searchQueryText: string }) => void;
}

const SearchForm: React.FC<SearchFormProps> = ({ form, onFinish }) => {
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
        <SearchQueryInput onSearch={() => form.submit()} />
      </Form.Item>
    </Form>
  );
};

export default SearchForm;
