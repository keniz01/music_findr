import React from "react";
import { Spin } from "antd";

interface SearchResultsProps {
  isLoading: boolean;
  data: string | null | undefined;
}

const SearchResults: React.FC<SearchResultsProps> = ({ isLoading, data }) => {
  if (isLoading) {
    return (
      <div
        id="search-query-results"
        data-testid="search-query-results"
        className="flex justify-center items-center min-h-screen animate-fade-in"
      >
        <div className="scale-[1.5] transition-transform duration-300 ease-in-out">
          <Spin />
        </div>
      </div>
    );
  }

  if (!data) return null;

  return (
    <div className="mt-4">
      <div>{data || "No results found."}</div>
    </div>
  );
};

export default SearchResults;
