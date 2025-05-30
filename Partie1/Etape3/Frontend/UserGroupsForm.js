import React, { useState } from "react";
import axios from "axios";

const UserGroupsForm = () => {
  const [userId, setUserId] = useState("");
  const [groups, setGroups] = useState([]);

  const handleSubmit = async (e) => {
    e.preventDefault();
    try {
      const res = await axios.get(`http://localhost:8000/users/${userId}/groups`);
      setGroups(res.data.groups);
    } catch (error) {
      console.error(error);
      alert("Erreur : " + (error.response?.data?.detail || "Erreur inconnue"));
    }
  };

  return (
    <div style={{
      maxWidth: "400px",
      margin: "0 auto",
      padding: "1.5rem",
      border: "1px solid #ccc",
      borderRadius: "8px",
      backgroundColor: "#f9f9f9",
    }}>
      <h2 style={{ marginBottom: "1rem" }}>Afficher les Groupes d’un Utilisateur</h2>
      <form onSubmit={handleSubmit} style={{ display: "flex", flexDirection: "column", gap: "1rem" }}>
        <div>
          <label>ID de l'utilisateur :</label><br />
          <input
            type="text"
            value={userId}
            onChange={(e) => setUserId(e.target.value)}
            required
          />
        </div>
        <button type="submit" style={{
          padding: "0.5rem 1rem",
          backgroundColor: "#28a745",
          color: "#fff",
          border: "none",
          borderRadius: "4px",
          cursor: "pointer"
        }}>
          Afficher les groupes
        </button>
      </form>

      {groups.length > 0 && (
        <div style={{ marginTop: "1rem" }}>
          <h3>Groupes :</h3>
          <ul>
            {groups.map((group, idx) => (
              <li key={idx}>{group}</li>
            ))}
          </ul>
        </div>
      )}
    </div>
  );
};

export default UserGroupsForm;

