import React, { forwardRef } from "react";
import { Input, Button, type InputRef } from "antd";
import { SearchOutlined, CloseOutlined } from "@ant-design/icons";

interface SearchInputProps {
  value?: string;
  onChange?: (e: React.ChangeEvent<HTMLInputElement>) => void;
  onSearch: () => void;
  onClear?: () => void;
}

const SearchQueryInput = forwardRef<InputRef, SearchInputProps>(
  ({ value, onChange, onSearch, onClear }, ref) => {
    const handleClear = () => {
      if (onClear) {
        onClear();
      }
    };

    return (
      <div className="relative w-full max-w-4xl mx-auto">
        <Input
          ref={ref}
          name="search-query-text-input"
          value={value}
          onChange={onChange}
          placeholder="Find music ..."
          className="search-input w-full"
          size="large"
          onPressEnter={onSearch}
          suffix={
            <div className="flex items-center gap-1">
              {value?.trim() && (
                <Button
                  data-testid="clear-button"
                  type="text"
                  icon={<CloseOutlined />}
                  onClick={handleClear}
                  size="small"
                />
              )}
              <Button
                type="primary"
                icon={<SearchOutlined />}
                onClick={onSearch}
                size="small"
              />
            </div>
          }
        />
      </div>
    );
  }
);

export default SearchQueryInput;
