const BASE_URL = 'http://127.0.0.1:8000'; // Adresse de votre backend

const API = {
  nextjsPage: () => `${BASE_URL}/nextjs/page`, // Vue Next.js
  listDeclarations: () => `${BASE_URL}/api/declarations/`, // Liste des déclarations
  createDeclaration: () => `${BASE_URL}/api/declarations/create/`, // Création d'une déclaration
  validateDeclaration: (declarationId) => `${BASE_URL}/validate-declaration/${declarationId}/`, // Validation d'une déclaration
  listFactures: () => `${BASE_URL}/list-factures/`, // Liste des factures
  paidFacture: (factureId) => `${BASE_URL}/paid-facture/${factureId}/`, // Paiement d'une facture
  listUsers: () => `${BASE_URL}/users/`, // Liste des utilisateurs
  userDetails: (id) => `${BASE_URL}/users/${id}/`, // Détails d'un utilisateur
  createUser: () => `${BASE_URL}/users/create/`, // Création d'un utilisateur
  deleteUser: (id) => `${BASE_URL}/users/${id}/delete/`, // Suppression d'un utilisateur
  updateUser: (id) => `${BASE_URL}/users/${id}/put`, // Mise à jour d'un utilisateur
};

export default API;
