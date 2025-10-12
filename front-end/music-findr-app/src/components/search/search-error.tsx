import React from "react";
import { Alert } from "antd";
import parseError from "../../utils/error-parser";

interface SearchErrorProps {
  error: unknown;
}

const SearchError: React.FC<SearchErrorProps> = ({ error }) => {
  const message = "Search Error";
  const errorType = "error";

  if (!(error instanceof Error)) {
    return (
      <Alert
        message={message}
        description="An unknown error occurred"
        type={errorType}
        showIcon
      />
    );
  }

  const friendlyMessage = parseError(error);

  return (
    <Alert
      message={message}
      description={friendlyMessage}
      type={errorType}
      showIcon
    />
  );
};

export default SearchError;
