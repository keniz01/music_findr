import React, { forwardRef } from "react";
import { Input, type InputRef } from "antd";
import { SearchOutlined } from "@ant-design/icons";

interface SearchInputProps {
  value?: string;
  onChange?: (e: React.ChangeEvent<HTMLInputElement>) => void;
  onSearch: () => void;
}

const SearchQueryInput = forwardRef<InputRef, SearchInputProps>(
  ({ value, onChange, onSearch }, ref) => {
    return (
      <Input.Search
        ref={ref}
        name="search-query-text-input"
        value={value}
        onChange={onChange}
        placeholder="Search..."
        enterButton={<SearchOutlined />}
        className="search-input w-full max-w-xl"
        size="large"
        onSearch={onSearch}
      />
    );
  },
);

export default SearchQueryInput;
