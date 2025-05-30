import React from "react";
import CreateUser from "./CreateUser";
import AssignGroups from "./AssignGroups";
import CreateFullUserForm from "./CreateFullUserForm";
import RemoveGroups from "./RemoveGroups";
import UpdateUserForm from "./UpdateUser";
import DeleteUserForm from "./DeleteUser";
import UserGroupsForm from "./UserGroups";

function App() {
  return (
    <div style={{ textAlign: "center", padding: "2rem", fontFamily: "Arial" }}>
      <h1 style={{ marginBottom: "2rem", color: "#333" }}>
        Gestion des Utilisateurs Odoo
      </h1>

      <section style={{ marginBottom: "4rem" }}>
        <h2>Création Utilisateur Simple</h2>
        <CreateUser />
      </section>

      <section style={{ marginBottom: "4rem" }}>
        <h2>Création Utilisateur Complet</h2>
        <CreateFullUserForm />
      </section>

      <section style={{ marginBottom: "4rem" }}>
        <h2>Mettre à Jour un Utilisateur</h2>
        <UpdateUserForm />
      </section>

      <section style={{ marginBottom: "4rem" }}>
        <h2>Supprimer un Utilisateur</h2>
        <DeleteUserForm />
      </section>

      <section style={{ marginBottom: "4rem" }}>
        <h2>Groupes de l’Utilisateur</h2>
        <UserGroups />
      </section>

      <section style={{ marginBottom: "4rem" }}>
        <h2>Attribuer des Groupes</h2>
        <AssignGroups />
      </section>

      <section>
        <h2>Retirer des Groupes</h2>
        <RemoveGroups />
      </section>
    </div>
  );
}

export default App;
