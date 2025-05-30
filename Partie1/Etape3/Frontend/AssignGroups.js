import React, { useState } from "react";
import axios from "axios";

const AssignGroups = () => {
  const [userId, setUserId] = useState("");
  const [groupIds, setGroupIds] = useState("");
  const [responseMessage, setResponseMessage] = useState("");

  const handleSubmit = async (e) => {
    e.preventDefault();
    const groupsArray = groupIds.split(",").map((id) => parseInt(id.trim(), 10));

    try {
      const response = await axios.post(
        `http://localhost:8000/users/${userId}/roles`,
        { groups: groupsArray },
        { headers: { "Content-Type": "application/json" } }
      );
      setResponseMessage(`Groupes attribués avec succès : ${response.data.groups.join(", ")}`);
    } catch (error) {
      console.error("Erreur :", error);
      setResponseMessage(`Erreur : ${error.response?.data?.detail || error.message}`);
    }
  };

  return (
    <div style={{
      maxWidth: "400px",
      margin: "2rem auto",
      padding: "1.5rem",
      border: "1px solid #ccc",
      borderRadius: "8px",
      backgroundColor: "#f9f9f9",
    }}>
      <h2 style={{ marginBottom: "1rem" }}>Attribuer des groupes</h2>
      <form onSubmit={handleSubmit} style={{ display: "flex", flexDirection: "column", gap: "1rem" }}>
        <div>
          <label>ID de l'utilisateur :</label><br />
          <input
            type="number"
            value={userId}
            onChange={(e) => setUserId(e.target.value)}
            required
            style={{ width: "100%", padding: "8px" }}
          />
        </div>

        <div>
          <label>IDs des groupes (séparés par des virgules) :</label><br />
          <input
            type="text"
            value={groupIds}
            onChange={(e) => setGroupIds(e.target.value)}
            placeholder="Ex: 1,2,3"
            required
            style={{ width: "100%", padding: "8px" }}
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
          Attribuer les groupes
        </button>

        {responseMessage && (
          <div style={{ marginTop: "1rem", color: responseMessage.includes("Erreur") ? "red" : "green" }}>
            {responseMessage}
          </div>
        )}
      </form>
    </div>
  );
};

export default AssignGroups;

