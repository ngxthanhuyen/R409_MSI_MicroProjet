import React, { useState } from "react";
import axios from "axios";

const CreateFullUserForm = () => {
  const [formData, setFormData] = useState({
    login_name: "",
    password: "",
    other_ids: {
      id: "",
      guid: "",
      up_id: "",
      display_name: ""
    },
    groups: [
      {
        id: "",
        external_name: "",
        other_ids: {
          id: "",
          guid: "",
          up_id: "",
          display_name: ""
        }
      }
    ]
  });

  const handleChange = (e, groupIndex = null, groupField = null, isGroupOtherIds = false) => {
    const { name, value } = e.target;
    if (groupIndex !== null) {
      const newGroups = [...formData.groups];
      if (isGroupOtherIds) {
        newGroups[groupIndex].other_ids[groupField] = value;
      } else {
        newGroups[groupIndex][groupField] = value;
      }
      setFormData({ ...formData, groups: newGroups });
    } else if (name.startsWith("other_ids.")) {
      const key = name.split(".")[1];
      setFormData((prev) => ({
        ...prev,
        other_ids: {
          ...prev.other_ids,
          [key]: value
        }
      }));
    } else {
      setFormData((prev) => ({ ...prev, [name]: value }));
    }
  };

  const addGroup = () => {
    setFormData((prev) => ({
      ...prev,
      groups: [
        ...prev.groups,
        {
          id: "",
          external_name: "",
          other_ids: {
            id: "",
            guid: "",
            up_id: "",
            display_name: ""
          }
        }
      ]
    }));
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    try {
      const response = await axios.post("http://localhost:8000/users/full", formData);
      const userId = response.data.user_id;
      alert(`Utilisateur créé avec succès ! ID : ${userId}`);
    } catch (error) {
      console.error(error);
      alert("Erreur : " + JSON.stringify(error.response?.data?.detail, null, 2));
    }
  };

  return (
    <div style={{
      maxWidth: "600px",
      margin: "0 auto",
      padding: "2rem",
      border: "1px solid #ccc",
      borderRadius: "8px",
      backgroundColor: "#f9f9f9",
    }}>
      <h2 style={{ marginBottom: "1rem" }}>Créer un utilisateur complet</h2>
      <form onSubmit={handleSubmit} style={{ display: "flex", flexDirection: "column", gap: "1rem" }}>
        <div>
          <label>Login :</label><br />
          <input name="login_name" type="text" value={formData.login_name} onChange={handleChange} required />
        </div>

        <div>
          <label>Mot de passe :</label><br />
          <input name="password" type="password" value={formData.password} onChange={handleChange} required />
        </div>

        <div>
          <label>Nom affiché (display_name) :</label><br />
          <input name="other_ids.display_name" value={formData.other_ids.display_name} onChange={handleChange} />
        </div>

        <div>
          <label>GUID :</label><br />
          <input name="other_ids.guid" value={formData.other_ids.guid} onChange={handleChange} />
        </div>

        <div>
          <label>ID :</label><br />
          <input name="other_ids.id" value={formData.other_ids.id} onChange={handleChange} />
        </div>

        <div>
          <label>Up ID :</label><br />
          <input name="other_ids.up_id" value={formData.other_ids.up_id} onChange={handleChange} />
        </div>

        <h3>Groupes</h3>
        {formData.groups.map((group, index) => (
          <div key={index} style={{
            border: "1px solid #ddd",
            borderRadius: "6px",
            padding: "1rem",
            marginBottom: "1rem",
            backgroundColor: "#fff"
          }}>
            <div>
              <label>Group ID :</label><br />
              <input
                value={group.id}
                onChange={(e) => handleChange(e, index, "id")}
              />
            </div>

            <div>
              <label>Nom externe :</label><br />
              <input
                value={group.external_name}
                onChange={(e) => handleChange(e, index, "external_name")}
              />
            </div>

            <div>
              <label>Group Other ID :</label><br />
              <input
                value={group.other_ids.id}
                onChange={(e) => handleChange(e, index, "id", true)}
              />
            </div>

            <div>
              <label>Group GUID :</label><br />
              <input
                value={group.other_ids.guid}
                onChange={(e) => handleChange(e, index, "guid", true)}
              />
            </div>

            <div>
              <label>Group Up ID :</label><br />
              <input
                value={group.other_ids.up_id}
                onChange={(e) => handleChange(e, index, "up_id", true)}
              />
            </div>

            <div>
              <label>Group Display Name :</label><br />
              <input
                value={group.other_ids.display_name}
                onChange={(e) => handleChange(e, index, "display_name", true)}
              />
            </div>
          </div>
        ))}

        <button
          type="button"
          onClick={addGroup}
          style={{
            padding: "0.5rem 1rem",
            backgroundColor: "#28a745",
            color: "#fff",
            border: "none",
            borderRadius: "4px",
            cursor: "pointer"
          }}>
          Ajouter un groupe
        </button>

        <button
          type="submit"
          style={{
            padding: "0.5rem 1rem",
            backgroundColor: "#007bff",
            color: "#fff",
            border: "none",
            borderRadius: "4px",
            cursor: "pointer"
          }}>
          Créer l'utilisateur
        </button>
      </form>
    </div>
  );
};

export default CreateFullUserForm;

