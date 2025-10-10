import React from "react";
import { Alert } from "antd";
import parseError from "../../utils/error-parser"

interface SearchErrorProps {
  error: unknown;
}

const SearchError: React.FC<SearchErrorProps> = ({ error }) => {
  if (!(error instanceof Error)) return null;

  const friendlyMessage = parseError(error);

  return (
    <Alert
      message="Oops! Something went wrong"
      description={friendlyMessage}
      type="error"
      showIcon
    />
  );
};

export default SearchError;
