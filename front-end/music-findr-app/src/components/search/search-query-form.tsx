import React, { useEffect, useState } from "react";
import { Form } from "antd";
import { useSearchQueryApi } from "../../hooks/use-search-query-api";
import SearchError from "./search-error";
import SearchForm from "./search-form";
import SearchResults from "./search-result";

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
    <div className="max-w-md mx-[5%] p-6">
      <SearchForm form={form} onFinish={onFinish} />

      {isError ? (
        <SearchError error={error} />
      ) : (
        <SearchResults isLoading={isLoading} data={data} />
      )}
    </div>
  );
};

export default SearchQueryForm;
