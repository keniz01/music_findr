const parseError = (error: unknown): string => {
  if (!(error instanceof Error)) return "An unknown error occurred.";

  const msg = error.message;

  if (msg.includes("UndefinedTableError") && msg.includes("schema_embeddings")) {
    return "We're having trouble accessing the data source. Please try again later.";
  }

  if (msg.includes("Network Error")) {
    return "Unable to connect. Please check your internet connection.";
  }

  return "Something went wrong. Please try again.";
};

export default parseError;
