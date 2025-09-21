// components/UserProfile.tsx
import { useUser } from '../hooks/useUser';

export const QuerySearch = ({ userQuery }: { userQuery: string }) => {
  const { data, isLoading, isError } = useQuerySearch(userQuery);

  if (isLoading) return <p>Loading user...</p>;
  if (isError) return <p>Failed to load user data.</p>;

  return (
    <div>
      <h2>Find music</h2>
      <p>Search page</p>
    </div>
  );
};
