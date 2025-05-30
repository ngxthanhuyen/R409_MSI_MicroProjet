import React, { useState } from "react";
import axios from "axios";

const DeleteUserForm = () => {
  const [userId, setUserId] = useState("");

  const handleSubmit = async (e) => {
    e.preventDefault();
    try {
      await axios.delete(`http://localhost:8000/users/${userId}`);
      alert("Utilisateur supprimé avec succès !");
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
      <h2 style={{ marginBottom: "1rem" }}>Supprimer un Utilisateur</h2>
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
          backgroundColor: "#dc3545",
          color: "#fff",
          border: "none",
          borderRadius: "4px",
          cursor: "pointer"
        }}>
          Supprimer
        </button>
      </form>
    </div>
  );
};

export default DeleteUserForm;

