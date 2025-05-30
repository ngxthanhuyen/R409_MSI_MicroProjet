import React, { useState } from "react";
import axios from "axios";

const UpdateUserForm = () => {
  const [userId, setUserId] = useState("");
  const [formData, setFormData] = useState({
    login_name: "",
    password: "",
    other_ids: {
      id: "",
      guid: "",
      up_id: "",
      display_name: ""
    }
  });

  const handleChange = (e) => {
    const { name, value } = e.target;
    if (name.startsWith("other_ids.")) {
      const key = name.split(".")[1];
      setFormData((prev) => ({
        ...prev,
        other_ids: {
          ...prev.other_ids,
          [key]: value
        }
      }));
    } else if (name === "userId") {
      setUserId(value);
    } else {
      setFormData((prev) => ({ ...prev, [name]: value }));
    }
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    try {
      const url = `http://localhost:8000/users/${userId}`;
      const response = await axios.put(url, formData);
      alert("Utilisateur mis à jour avec succès !");
    } catch (err) {
      console.error(err);
      alert("Erreur : " + (err.response?.data?.detail || "Erreur inconnue"));
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
      <h2 style={{ marginBottom: "1rem" }}>Mettre à jour un Utilisateur</h2>
      <form onSubmit={handleSubmit} style={{ display: "flex", flexDirection: "column", gap: "1rem" }}>
        <div>
          <label>ID de l'utilisateur à modifier :</label><br />
          <input type="text" name="userId" value={userId} onChange={handleChange} required />
        </div>

        <div>
          <label>Login :</label><br />
          <input type="text" name="login_name" value={formData.login_name} onChange={handleChange} required />
        </div>

        <div>
          <label>Mot de passe :</label><br />
          <input type="password" name="password" value={formData.password} onChange={handleChange} required />
        </div>

        <div>
          <label>Nom affiché :</label><br />
          <input type="text" name="other_ids.display_name" value={formData.other_ids.display_name} onChange={handleChange} />
        </div>

        <div>
          <label>GUID :</label><br />
          <input type="text" name="other_ids.guid" value={formData.other_ids.guid} onChange={handleChange} />
        </div>

        <div>
          <label>ID :</label><br />
          <input type="text" name="other_ids.id" value={formData.other_ids.id} onChange={handleChange} />
        </div>

        <div>
          <label>Up ID (optionnel) :</label><br />
          <input type="text" name="other_ids.up_id" value={formData.other_ids.up_id} onChange={handleChange} />
        </div>

        <button type="submit" style={{
          padding: "0.5rem 1rem",
          backgroundColor: "#007bff",
          color: "#fff",
          border: "none",
          borderRadius: "4px",
          cursor: "pointer"
        }}>
          Mettre à jour
        </button>
      </form>
    </div>
  );
};

export default UpdateUserForm;
