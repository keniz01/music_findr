import React, { useEffect, useState } from "react";
import { Form } from "antd";
import { useSearchQueryApi } from "../../hooks/use-search-query-api";
import SearchError from "./search-error";
import SearchForm from "./search-form";
import SearchResults from "./search-result";
import ChatHistory from "./chat-history";

interface ChatMessage {
  id: string;
  query: string;
  response: string;
  timestamp: Date;
}

const SearchQueryForm: React.FC = () => {
  const [form] = Form.useForm();
  const [searchQuery, setSearchQuery] = useState<string>("");
  const [chatMessages, setChatMessages] = useState<ChatMessage[]>([]);
  const [hasInteracted, setHasInteracted] = useState<boolean>(false);

  const { data, isLoading, isError, error, refetch } =
    useSearchQueryApi(searchQuery);

  const onFinish = (values: { searchQueryText: string }) => {
    const trimmedQuery = values.searchQueryText.trim();
    if (!trimmedQuery) return;
    setSearchQuery(trimmedQuery);
    setHasInteracted(true);
  };

  const onClear = () => {
    form.setFieldsValue({ searchQueryText: "" });
    setSearchQuery("");
  };

  useEffect(() => {
    if (searchQuery) {
      refetch();
    }
  }, [searchQuery, refetch]);

  useEffect(() => {
    if (searchQuery && data) {
      const newMessage: ChatMessage = {
        id: Date.now().toString(),
        query: searchQuery,
        response: data,
        timestamp: new Date()
      };
      setChatMessages((prev) => [...prev, newMessage]);
    }
  }, [searchQuery, data]);

  const isInitialState = !hasInteracted && chatMessages.length === 0;

  return (
    <div
      className={`text-center w-3/4 max-w-4xl mx-auto transition-all duration-300 ${
        isInitialState
          ? "flex items-center justify-center min-h-screen px-4"
          : "flex flex-col h-full px-4"
      }`}
    >
      {!isInitialState && (
        <div className="flex-1 overflow-y-auto max-h-[calc(100vh-200px)] mb-4 m-h-[100vh]">
          <ChatHistory messages={chatMessages} />
        </div>
      )}

      <div
        className={`${isInitialState ? "w-full max-w-md mx-auto" : "w-full"} transition-all duration-300 flex-shrink-0`}
      >
        <SearchForm form={form} onFinish={onFinish} onClear={onClear} />

        {isError && (
          <div className="mt-4 text-left">
            <SearchError error={error} />
          </div>
        )}

        {isLoading && (
          <div className="mt-4">
            <SearchResults isLoading={isLoading} data={null} />
          </div>
        )}
      </div>
    </div>
  );
};

export default SearchQueryForm;
