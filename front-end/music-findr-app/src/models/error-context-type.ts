export interface ErrorContextType {
  error: Error | null;
  setError: (error: Error) => void;
}
