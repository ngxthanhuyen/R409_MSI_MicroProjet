import React, { useState } from "react";
import axios from "axios";

function CreateUserForm() {
  const [formData, setFormData] = useState({
    login: "",
    password: "",
    name: "",
    guid: "",
    id: "",
    groups: ""
  });

  const handleChange = (e) => {
    const { name, value } = e.target;
    setFormData((prev) => ({ ...prev, [name]: value }));
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    const groupsArray = formData.groups
      .split(",")
      .map((g) => Number(g.trim()))
      .filter((n) => !isNaN(n));

    const payload = {
      login_name: formData.login,
      password: formData.password,
      groups: groupsArray,
      other_ids: {
        id: formData.id,
        guid: formData.guid,
        display_name: formData.name
      }
    };

    try {
      const response = await axios.post("http://localhost:8000/users", payload);
      alert(`Utilisateur créé avec l'ID : ${response.data.user_id}`);
    } catch (error) {
      console.error("Erreur :", error.response?.data || error.message);
      alert("Erreur lors de la création de l'utilisateur !");
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
      <h2 style={{ marginBottom: "1rem" }}>Créer un Utilisateur</h2>
      <form onSubmit={handleSubmit} style={{ display: "flex", flexDirection: "column", gap: "1rem" }}>
        <div>
          <label>Nom complet (display_name) :</label><br />
          <input type="text" name="name" value={formData.name} onChange={handleChange} required />
        </div>

        <div>
          <label>Login :</label><br />
          <input type="text" name="login" value={formData.login} onChange={handleChange} required />
        </div>

        <div>
          <label>Mot de passe :</label><br />
          <input type="password" name="password" value={formData.password} onChange={handleChange} required />
        </div>

        <div>
          <label>GUID :</label><br />
          <input type="text" name="guid" value={formData.guid} onChange={handleChange} required />
        </div>

        <div>
          <label>ID (other_ids.id) :</label><br />
          <input type="text" name="id" value={formData.id} onChange={handleChange} required />
        </div>

        <div>
          <label>Groupes (IDs séparés par des virgules) :</label><br />
          <input
            type="text"
            name="groups"
            value={formData.groups}
            onChange={handleChange}
            placeholder="ex: 1,2,3"
          />
        </div>

        <button type="submit" style={{
          padding: "0.5rem 1rem",
          backgroundColor: "#007bff",
          color: "#fff",
          border: "none",
          borderRadius: "4px",
          cursor: "pointer"
        }}>
          Créer
        </button>
      </form>
    </div>
  );
}

export default CreateUserForm;

