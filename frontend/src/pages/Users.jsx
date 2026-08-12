import { useEffect, useState } from "react";
import { getUsers } from "../api";

function Users() {
  const [users, setUsers] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);
  const [search, setSearch] = useState("");

  useEffect(() => {
    async function loadUsers() {
      try {
        const data = await getUsers();

        console.log("Users data received:", data);

        // Supports both:
        // { users: [...] }
        // and a direct [...]
        const userList = Array.isArray(data)
          ? data
          : data.users || [];

        setUsers(userList);
      } catch (err) {
        console.error("Users loading error:", err);
        setError(err.message);
      } finally {
        setLoading(false);
      }
    }

    loadUsers();
  }, []);

  const filteredUsers = users.filter((user) => {
    const searchText = search.toLowerCase();

    return (
      user.username?.toLowerCase().includes(searchText) ||
      user.display_name?.toLowerCase().includes(searchText)
    );
  });

  if (loading) {
    return (
      <div className="page-loading">
        Loading users...
      </div>
    );
  }

  if (error) {
    return (
      <div className="page-error">
        Failed to load users: {error}
      </div>
    );
  }

  return (
    <div className="users-page">

      <div className="page-header">
        <div>
          <h1>Users</h1>

          <p>
            Registered social-media accounts and account activity.
          </p>
        </div>
      </div>


      <div className="users-toolbar">

        <input
          type="text"
          placeholder="Search username or display name..."
          value={search}
          onChange={(event) => setSearch(event.target.value)}
        />

        <div className="users-count">
          Showing {filteredUsers.length} of {users.length} users
        </div>

      </div>


      <div className="users-panel">

        <div className="table-container">

          <table className="data-table">

            <thead>
              <tr>
                <th>Username</th>
                <th>Display Name</th>
                <th>Bio</th>
                <th>Account Created</th>
              </tr>
            </thead>

            <tbody>

              {filteredUsers.map((user) => (
                <tr key={user.id}>

                  <td>
                    <strong>
                      @{user.username}
                    </strong>
                  </td>

                  <td>
                    {user.display_name}
                  </td>

                  <td>
                    {user.bio || "—"}
                  </td>

                  <td>
                    {user.account_created_at
                      ? new Date(
                          user.account_created_at
                        ).toLocaleDateString()
                      : "—"}
                  </td>

                </tr>
              ))}

              {filteredUsers.length === 0 && (
                <tr>
                  <td
                    colSpan="4"
                    className="empty-table"
                  >
                    No users found.
                  </td>
                </tr>
              )}

            </tbody>

          </table>

        </div>

      </div>

    </div>
  );
}

export default Users;